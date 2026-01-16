"""
Chat Endpoints
WebSocket and REST endpoints for AI TA chat.
"""

from pathlib import Path
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.ai_engine.agents.ta_agent import get_ta_response, get_vectorstore


router = APIRouter()

# Path to knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent.parent.parent / "knowledge_base"


class ChatRequest(BaseModel):
    message: str
    code: str
    lab_id: Optional[str] = None


class SourceInfo(BaseModel):
    name: str
    path: str = ""
    snippet: str = ""


class ChatResponse(BaseModel):
    response: str
    sources: List[SourceInfo] = []


class KnowledgeFileResponse(BaseModel):
    name: str
    content: str
    category: str = ""


@router.post("/ask", response_model=ChatResponse)
async def ask_ta(request: ChatRequest):
    """
    Ask the AI TA a question about your code.
    Uses RAG to retrieve relevant context from lab materials.
    """
    try:
        vectorstore = get_vectorstore()
        response = await get_ta_response(
            vectorstore=vectorstore,
            question=request.message,
            student_code=request.code
        )
        
        # Convert sources to SourceInfo objects
        sources = []
        for src in response.get("sources", []):
            if isinstance(src, dict):
                sources.append(SourceInfo(
                    name=src.get("name", "unknown"),
                    path=src.get("path", ""),
                    snippet=src.get("snippet", "")
                ))
        
        return ChatResponse(
            response=response["answer"],
            sources=sources
        )
    
    except Exception as e:
        return ChatResponse(
            response=f"I'm having trouble connecting right now. Error: {str(e)}",
            sources=[]
        )


@router.get("/knowledge/{filename}", response_model=KnowledgeFileResponse)
async def get_knowledge_file(filename: str):
    """
    Get the full content of a knowledge base file.
    Used by the frontend to display source references in a modal.
    """
    # Search for the file in all subdirectories
    for category_dir in KNOWLEDGE_BASE_PATH.iterdir():
        if category_dir.is_dir():
            file_path = category_dir / filename
            if file_path.exists() and file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    return KnowledgeFileResponse(
                        name=filename,
                        content=content,
                        category=category_dir.name
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
    raise HTTPException(status_code=404, detail=f"File '{filename}' not found in knowledge base")


@router.get("/knowledge")
async def list_knowledge_files():
    """
    List all available knowledge base files.
    """
    files = []
    for category_dir in KNOWLEDGE_BASE_PATH.iterdir():
        if category_dir.is_dir():
            for file_path in category_dir.glob("*.md"):
                files.append({
                    "name": file_path.name,
                    "category": category_dir.name,
                    "path": str(file_path)
                })
            for file_path in category_dir.glob("*.txt"):
                files.append({
                    "name": file_path.name,
                    "category": category_dir.name,
                    "path": str(file_path)
                })
    return {"files": files}


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with the TA.
    Enables streaming responses.
    """
    await websocket.accept()
    
    try:
        vectorstore = get_vectorstore()
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message = data.get("message", "")
            code = data.get("code", "")
            
            # Send typing indicator
            await websocket.send_json({"type": "typing", "status": True})
            
            try:
                # Get TA response
                response = await get_ta_response(
                    vectorstore=vectorstore,
                    question=message,
                    student_code=code
                )
                
                # Send response
                await websocket.send_json({
                    "type": "message",
                    "response": response["answer"],
                    "sources": response.get("sources", [])
                })
            
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
            
            finally:
                # Clear typing indicator
                await websocket.send_json({"type": "typing", "status": False})
    
    except WebSocketDisconnect:
        print("Client disconnected from chat")


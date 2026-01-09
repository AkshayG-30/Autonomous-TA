"""
Chat Endpoints
WebSocket and REST endpoints for AI TA chat.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional

from app.ai_engine.agents.ta_agent import get_ta_response, get_vectorstore


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    code: str
    lab_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: list = []


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
        
        return ChatResponse(
            response=response["answer"],
            sources=response.get("sources", [])
        )
    
    except Exception as e:
        return ChatResponse(
            response=f"I'm having trouble connecting right now. Error: {str(e)}",
            sources=[]
        )


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

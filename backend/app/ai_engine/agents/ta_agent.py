"""
TA Agent - RAG-powered Teaching Assistant
Uses ChromaDB for context retrieval and Groq API for responses.
"""

import os
from pathlib import Path
from groq import Groq

from app.core.config import settings
from app.ai_engine.rag.ingest import get_vectorstore as get_rag_vectorstore


# Load the Socratic TA prompt
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_system_prompt():
    """Load the system prompt from file."""
    prompt_file = PROMPTS_DIR / "socratic_ta.txt"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "You are a helpful teaching assistant for a programming course. Guide students using the Socratic method - ask leading questions rather than giving direct answers."


def get_vectorstore():
    """Get the ChromaDB vectorstore for RAG retrieval."""
    try:
        return get_rag_vectorstore()
    except Exception as e:
        print(f"Warning: Could not load vectorstore: {e}")
        return None


def retrieve_context(vectorstore, question: str, student_code: str, k: int = 3) -> tuple:
    """Retrieve relevant context from the knowledge base using RAG.
    
    Returns:
        tuple: (context_string, list of source dicts with name, path, and snippet)
    """
    if vectorstore is None:
        return "No knowledge base available.", []
    
    try:
        # Combine question and code for better context matching
        query = f"{question}\n\nStudent code: {student_code[:500]}"
        
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(query, k=k)
        
        if not docs:
            return "No relevant context found in knowledge base.", []
        
        # Format the context and collect sources
        context_parts = []
        sources = []
        seen_sources = set()  # Avoid duplicates
        
        for i, doc in enumerate(docs, 1):
            source_path = doc.metadata.get("source", "")
            source_name = Path(source_path).name if source_path else "unknown"
            
            context_parts.append(f"[Source: {source_name}]\n{doc.page_content}")
            
            # Add unique sources to the list
            if source_name not in seen_sources:
                seen_sources.add(source_name)
                sources.append({
                    "name": source_name,
                    "path": source_path,
                    "snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
        
        return "\n\n---\n\n".join(context_parts), sources
        
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return "Error retrieving context from knowledge base.", []


# Initialize client
def get_groq_client():
    """Get Groq client instance."""
    api_key = settings.groq_api_key
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please create a .env file in the backend folder with your Groq API key.")
    return Groq(api_key=api_key)


async def get_ta_response(vectorstore, question: str, student_code: str) -> dict:
    """
    Get a response from the TA agent using RAG + Groq API.
    
    Args:
        vectorstore: ChromaDB vectorstore for context retrieval
        question: The student's question
        student_code: The student's current code
    
    Returns:
        dict with 'answer' and 'sources' keys
    """
    try:
        client = get_groq_client()
    except ValueError as e:
        return {
            "answer": str(e),
            "sources": []
        }
    
    system_prompt = load_system_prompt()
    
    # Retrieve relevant context using RAG
    context, sources = retrieve_context(vectorstore, question, student_code)
    
    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""
## Relevant Course Materials
{context}

## Student's Code
```python
{student_code}
```

## Student's Question
{question}

Please respond as a helpful teaching assistant. Use the Socratic method: guide the student to discover the answer themselves through questions, hints, and explanations. Reference the course materials when relevant.
"""}
            ],
            model=settings.groq_model,
            temperature=0.3,
            max_tokens=1024
        )
        
        answer = chat_completion.choices[0].message.content
        
        return {
            "answer": answer,
            "sources": sources  # Return the actual source files with details
        }
    
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
            return {
                "answer": "API key error. Please check your GROQ_API_KEY in the .env file.",
                "sources": []
            }
        return {
            "answer": f"I'm having trouble responding right now. Error: {error_msg}",
            "sources": []
        }


# Synchronous version
def get_ta_response_sync(vectorstore, question: str, student_code: str) -> dict:
    """Synchronous version of get_ta_response."""
    import asyncio
    return asyncio.run(get_ta_response(vectorstore, question, student_code))


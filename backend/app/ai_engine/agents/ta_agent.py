"""
TA Agent - Simplified Version
Uses direct Groq API calls instead of LangChain for Python 3.14 compatibility.
"""

import os
from pathlib import Path
from groq import Groq

from app.core.config import settings


# Load the Socratic TA prompt
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_system_prompt():
    """Load the system prompt from file."""
    prompt_file = PROMPTS_DIR / "socratic_ta.txt"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "You are a helpful teaching assistant."


def load_knowledge_base():
    """Load knowledge base content from files."""
    knowledge_base_path = Path(__file__).parent.parent.parent.parent.parent / "knowledge_base"
    
    content = []
    
    # Load assignments
    assignments_path = knowledge_base_path / "assignments"
    if assignments_path.exists():
        for file in assignments_path.glob("*.txt"):
            content.append(f"=== {file.name} ===\n{file.read_text(encoding='utf-8')}")
    
    # Load syllabus
    syllabus_path = knowledge_base_path / "syllabus"
    if syllabus_path.exists():
        for file in syllabus_path.glob("*.txt"):
            content.append(f"=== {file.name} ===\n{file.read_text(encoding='utf-8')}")
    
    return "\n\n".join(content) if content else "No course materials loaded."


# Initialize client
def get_groq_client():
    """Get Groq client instance."""
    return Groq(api_key=settings.groq_api_key)


# Placeholder for vectorstore compatibility
def get_vectorstore():
    """Return None - using simple text search instead of ChromaDB for compatibility."""
    return None


async def get_ta_response(vectorstore, question: str, student_code: str) -> dict:
    """
    Get a response from the TA agent using direct Groq API.
    
    Args:
        vectorstore: Ignored (for API compatibility)
        question: The student's question
        student_code: The student's current code
    
    Returns:
        dict with 'answer' and 'sources' keys
    """
    client = get_groq_client()
    system_prompt = load_system_prompt()
    knowledge_base = load_knowledge_base()
    
    # Build the full prompt
    full_prompt = f"""
{system_prompt}

## Lab Context (Course Materials)
{knowledge_base}

## Student's Current Code
```
{student_code}
```

## Student's Question
{question}

## Your Response (as the Socratic TA)
"""
    
    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""
Lab Context:
{knowledge_base[:3000]}  # Limit context size

Student's Code:
```
{student_code}
```

Student's Question: {question}
"""}
            ],
            model=settings.groq_model,
            temperature=0.1,
            max_tokens=1024
        )
        
        answer = chat_completion.choices[0].message.content
        
        return {
            "answer": answer,
            "sources": [{"source": "knowledge_base", "content": "Course materials"}]
        }
    
    except Exception as e:
        return {
            "answer": f"I'm having trouble responding right now. Error: {str(e)}",
            "sources": []
        }


# Synchronous version
def get_ta_response_sync(vectorstore, question: str, student_code: str) -> dict:
    """Synchronous version of get_ta_response."""
    import asyncio
    return asyncio.run(get_ta_response(vectorstore, question, student_code))

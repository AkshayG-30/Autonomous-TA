# Autonomous Lab TA

An AI-powered teaching assistant that helps students with programming labs through Socratic guidance, secure code execution, and RAG-based context from course materials.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Groq API Key (free at https://console.groq.com)

### Setup

1. **Clone and configure environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

2. **Start with Docker Compose**
```bash
docker-compose up --build
```

3. **Or run manually**

Backend:
```bash
cd backend
pip install -r requirements.txt
python -m app.ai_engine.rag.ingest  # Index knowledge base
uvicorn main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
autonomous-lab-ta/
├── backend/                 # FastAPI + AI Engine
├── frontend/                # React + TypeScript
├── sandbox/                 # Docker execution environments
├── knowledge_base/          # Lab instructions for RAG
└── docker-compose.yml       # Orchestration
```

## Tech Stack

- **Backend**: FastAPI, LangChain, Groq API
- **RAG**: ChromaDB + HuggingFace Embeddings
- **Frontend**: React, TypeScript, Monaco Editor
- **Sandbox**: Docker containers

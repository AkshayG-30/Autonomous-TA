"""
RAG Ingestion Script
Loads documents from knowledge_base, creates embeddings, and stores in ChromaDB.
Run this script to initialize or update the knowledge base.

Supports both .txt and .md (Markdown) files.
Markdown files are split semantically by headers for better context preservation.
"""

import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.core.config import settings


# Path to knowledge base relative to backend folder
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent.parent.parent / "knowledge_base"

# Headers to split markdown files on (preserves semantic context)
MARKDOWN_HEADERS = [
    ("#", "topic"),
    ("##", "section"),
    ("###", "subsection"),
]


def get_embeddings():
    """Get HuggingFace embeddings model (runs locally, free)."""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


def load_documents_from_folder(folder_path: Path, file_pattern: str = "**/*"):
    """Load documents from a folder, supporting both .txt and .md files."""
    documents = []
    
    if not folder_path.exists():
        return documents
    
    # Load .txt files
    txt_loader = DirectoryLoader(
        str(folder_path),
        glob=f"{file_pattern}.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents.extend(txt_loader.load())
    
    # Load .md files
    md_loader = DirectoryLoader(
        str(folder_path),
        glob=f"{file_pattern}.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents.extend(md_loader.load())
    
    return documents


def load_documents():
    """Load all documents from the knowledge base."""
    documents = []
    
    # Define all folders to load from
    folders = ["assignments", "syllabus", "concepts", "style_guide"]
    
    for folder_name in folders:
        folder_path = KNOWLEDGE_BASE_PATH / folder_name
        docs = load_documents_from_folder(folder_path)
        documents.extend(docs)
        if docs:
            print(f"  📂 {folder_name}/: {len(docs)} file(s)")
    
    print(f"📄 Loaded {len(documents)} total documents from knowledge base")
    return documents


def split_markdown_content(content: str):
    """Split markdown content by headers first, then by size."""
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False  # Keep headers in the content for context
    )
    
    # First pass: split by headers
    header_splits = md_splitter.split_text(content)
    
    return header_splits


def split_documents(documents):
    """Split documents into chunks for better retrieval.
    
    Markdown files are first split by headers for semantic chunking,
    then further split by size if needed.
    """
    all_chunks = []
    
    # Markdown header splitter
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False
    )
    
    # Size-based splitter for secondary splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    for doc in documents:
        source_path = doc.metadata.get("source", "")
        
        # Check if it's a markdown file
        if source_path.endswith(".md"):
            # Split by headers first
            header_chunks = md_splitter.split_text(doc.page_content)
            
            # Then split by size if chunks are too large
            for chunk in header_chunks:
                # Preserve metadata from original document
                chunk.metadata.update(doc.metadata)
            
            sized_chunks = text_splitter.split_documents(header_chunks)
            all_chunks.extend(sized_chunks)
        else:
            # Regular text files - just split by size
            chunks = text_splitter.split_documents([doc])
            all_chunks.extend(chunks)
    
    print(f"📦 Split into {len(all_chunks)} chunks")
    return all_chunks


def build_knowledge_base():
    """
    Main function to build/rebuild the vector store.
    Call this when you add new lab instructions.
    """
    print("🔨 Building knowledge base...")
    
    # Load and split documents
    documents = load_documents()
    
    if not documents:
        print("⚠️ No documents found in knowledge_base/")
        print(f"   Expected path: {KNOWLEDGE_BASE_PATH}")
        return None
    
    chunks = split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = get_embeddings()
    
    # Create the vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_persist_dir
    )
    
    print(f"✅ Knowledge base built and saved to {settings.chroma_persist_dir}")
    return vectorstore


def get_vectorstore():
    """Get existing vector store or create new one."""
    embeddings = get_embeddings()
    
    # Check if existing vector store exists
    if os.path.exists(settings.chroma_persist_dir):
        return Chroma(
            persist_directory=settings.chroma_persist_dir,
            embedding_function=embeddings
        )
    else:
        # Build new knowledge base
        return build_knowledge_base()


if __name__ == "__main__":
    # Run ingestion when script is called directly
    build_knowledge_base()

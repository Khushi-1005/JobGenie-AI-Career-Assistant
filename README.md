# JobGenie – RAG Service Agent

RAG service for resume processing using LangChain, Google Gemini Embeddings, and ChromaDB for semantic retrieval and AI-powered career assistance.



##  Objective
Build a Retrieval-Augmented Generation (RAG) pipeline that ingests a resume PDF, converts it into searchable vector embeddings, and enables semantic retrieval to support downstream AI career-assistance features (career assessment, job matching).

## Features Completed
- PDF loading via `PyPDFLoader`
- Text chunking via `RecursiveCharacterTextSplitter`
- Embedding generation via Google Gemini (`gemini-embedding-001`)
- Vector storage and persistence via ChromaDB
- Retriever setup for semantic search over resume content

## Workflow
```
Resume PDF → Document Loader → Text Splitter → Embeddings → ChromaDB → Retriever
```

##  Tech Stack
| Component | Tool |
|---|---|
| Language | Python |
| Framework | LangChain |
| Embeddings | Google Gemini |
| Vector Store | ChromaDB |
| PDF Parsing | PyPDFLoader |

## Setup & Run
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-key-here
```
Run the service:
```bash
python app/rag_service.py
```

##  Notes
Some earlier commits in this repo were mislabeled "Week 3" during initial
setup and debugging. This submission reflects Week 2 progress: RAG
pipeline setup, PDF loading, chunking, Gemini embeddings, and Chroma
vector store creation.


##  Project Status

**Project Name:** JobGenie Ai - Job search AI Agent 
**Current Phase:** Week 2 — RAG service implemented and tested end-to-end.
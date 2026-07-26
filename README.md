# JobGenie – AI Agent Workflow

RAG-powered career assessment agent using LangChain, LangGraph, Google Gemini embeddings, ChromaDB, and Groq for AI-powered career assistance.

## Objective

Take the RAG pipeline from last week and turn it into something an actual AI agent can use — instead of manually querying the vector store, the LLM now decides on its own when it needs resume data, pulls it through a tool call, and writes up a full career assessment.

## Features Completed

- `query_resume()` added to the RAG service for semantic search over the resume vector store
- Career Assessment Agent — an LLM (Groq / Llama 3.3) bound to a `fetch_resume_data` tool
- LangGraph workflow connecting an agent node and a tool node, with conditional routing based on whether the LLM requests a tool call
- Tested end-to-end: the agent correctly asks for resume data, gets it back from ChromaDB, and produces a grounded career report

## Workflow

''' User request -> Agent Node -> needs resume data?
yes -> fetch_resume_data tool -> back to Agent Node
no -> Final Career Assessment Report -> END '''

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python |
| Agent framework | LangChain + LangGraph |
| Agent LLM | Groq (Llama 3.3 70B) |
| Embeddings | Google Gemini |
| Vector Store | ChromaDB |
| PDF Parsing | PyPDFLoader |

## Setup & Run

'''python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt'''

Create a `.env` file in the project root:

'''GEMINI_API_KEY=your-key-here
GROQ_API_KEY=your-key-here
ADZUNA_APP_ID=your-key-here
ADZUNA_APP_KEY=your-key-here'''

Run the agent workflow:

'''python -m app.workflow
'''
## Sample Output

![Career assessment report output](screenshots/career_report_output.png)


## Notes

This week, we learned that an AI agent doesn't execute tools directly—it requests tool calls, and the application executes them and returns the results.We also debugged an indentation issue where a method was accidentally nested inside another, preventing it from being called correctly. This helped me better understand both agent workflows and Python class structure.

## Project Status

**Project Name:** JobGenie AI – Job Search AI Agent
**Current Phase:** Week 3 — Career Assessment Agent and LangGraph workflow implemented and tested end-to-end.


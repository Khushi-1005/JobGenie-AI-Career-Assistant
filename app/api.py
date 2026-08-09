"""
JobGenie API — career assessment + job search AI agent workflow,
exposed over HTTP.

Run with:
    uvicorn app.api:app --reload

Then open:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from app.workflow import ExecuteWorkflow
from app.rag_service import RAGServices
from app.agents.job_search_agent import job_search_tool

app = FastAPI(
    title="JobGenie API",
    description=(
        "An AI agent workflow that assesses a candidate's resume and "
        "searches live job listings that match their skills. Built with "
        "LangGraph, LangChain, RAG (ChromaDB + Gemini embeddings), and "
        "the Adzuna jobs API."
    ),
    version="1.0.0",
    contact={"name": "Khushi Nichang"},
)

_workflow = ExecuteWorkflow()
_rag = RAGServices()


# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------
class AssessRequest(BaseModel):
    message: str = Field(
        default="Assess my profile and generate an evaluation report",
        description="The instruction to give the career assessment agent.",
        examples=["Assess my profile and generate an evaluation report"],
    )


class AssessResponse(BaseModel):
    result: str = Field(description="The final report produced by the agent workflow.")


class ResumeQueryRequest(BaseModel):
    question: str = Field(
        description="A question to ask against the candidate's resume.",
        examples=["What programming languages does this candidate know?"],
    )


class ResumeQueryResponse(BaseModel):
    context: str


class JobSearchRequest(BaseModel):
    keyword: str = Field(examples=["Machine Learning Engineer"])
    min_salary: int = Field(default=0, examples=[100000])


class JobSearchResponse(BaseModel):
    listings: str


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Health check")
def root():
    """Basic health check + a quick pointer to the interactive docs."""
    return {
        "status": "JobGenie API is running",
        "docs": "/docs",
        "endpoints": ["/assess-and-search", "/resume/query", "/jobs/search"],
    }


@app.post(
    "/assess-and-search",
    response_model=AssessResponse,
    tags=["Workflow"],
    summary="Run the full agent workflow",
    description=(
        "Runs the complete multi-agent pipeline: the Career Assessment "
        "Agent retrieves resume data and writes a report, then hands off "
        "to the Job Search Agent, which finds live matching job listings."
    ),
)
def assess_and_search(request: AssessRequest):
    try:
        input_state = {"messages": [HumanMessage(content=request.message)]}
        result = _workflow.workflow.invoke(input_state)
        return AssessResponse(result=result["messages"][-1].content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {exc}")


@app.post(
    "/resume/query",
    response_model=ResumeQueryResponse,
    tags=["Resume"],
    summary="Query the resume directly",
    description="Runs a semantic search over the resume vector store, without invoking the full agent workflow.",
)
def query_resume(request: ResumeQueryRequest):
    try:
        context = _rag.query_resume(request.question)
        return ResumeQueryResponse(context=context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Resume query failed: {exc}")


@app.post(
    "/jobs/search",
    response_model=JobSearchResponse,
    tags=["Jobs"],
    summary="Search live job listings directly",
    description="Calls the Adzuna job search tool directly, bypassing the agent's reasoning step.",
)
def search_jobs(request: JobSearchRequest):
    try:
        listings = job_search_tool.invoke(
            {"keyword": request.keyword, "min_salary": request.min_salary}
        )
        return JobSearchResponse(listings=listings)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Job search failed: {exc}")
    
class JobSearchRequest(BaseModel):
    keyword: str = Field(examples=["Machine Learning Engineer"])
    min_salary_lpa: float = Field(default=0, examples=[12])
    location: str = Field(default="any", examples=["Bangalore"])
import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()


@tool
def job_search_tool(keyword: str, min_salary: int = 0) -> str:
    """Fetch job listings matching a keyword and minimum salary."""
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not api_key:
        return "Error: missing ADZUNA_APP_ID or ADZUNA_API_KEY in .env"

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id, "app_key": api_key, "what": keyword,
        "salary_min": min_salary, "results_per_page": 5,
        "content-type": "application/json",
    }
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        return f"Error: job search failed with status {response.status_code}"

    jobs = response.json().get("results", [])
    if not jobs:
        return f"No jobs found for '{keyword}'."

    lines = []
    for job in jobs:
        title = job.get("title", "Unknown title")
        company = job.get("company", {}).get("display_name", "Unknown company")
        location = job.get("location", {}).get("display_name", "Unknown location")
        lines.append(f"- {title} at {company} ({location})")
    return "\n".join(lines)


JOB_SEARCH_SYSTEM_PROMPT = """You are a Job Search AI Agent. Given a
career assessment report, call job_search_tool with a relevant keyword
and salary expectation, then summarize the best-fit job listings found."""


class JobSearchAgent:
    def __init__(self):
        self.tools = [job_search_tool]
        self.tools_map = {t.name: t for t in self.tools}
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0).bind_tools(self.tools)

    def agent_node(self, state):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=JOB_SEARCH_SYSTEM_PROMPT)] + messages
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def tool_node(self, state):
        last_message = state["messages"][-1]
        tool_messages = []
        for call in last_message.tool_calls:
            tool_fn = self.tools_map.get(call["name"])
            output = tool_fn.invoke(call["args"]) if tool_fn else f"Unknown tool: {call['name']}"
            tool_messages.append(
                ToolMessage(content=str(output), tool_call_id=call["id"], name=call["name"])
            )
        return {"messages": tool_messages}
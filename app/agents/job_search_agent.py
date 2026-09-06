import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage

load_dotenv()

INDIAN_METRO_CITIES = ["mumbai", "bangalore", "delhi", "pune", "hyderabad", "chennai", "kolkata"]


def lpa_to_annual(lpa: float) -> int:
    """Convert Lakhs Per Annum to a plain annual salary number."""
    return int(lpa * 100000)


@tool
def job_search_tool(
    keyword: str,
    min_salary_lpa: float = 0,
    location: str = "any",
    remote_ok: bool = True,
    max_notice_period_days: int = 90,
) -> str:
    """Fetch job listings for the Indian job market.

    Arguments:
    keyword -> The role the user is looking for (e.g. "Machine Learning Engineer")
    min_salary_lpa -> Minimum salary in Lakhs Per Annum (e.g. 12 for 12 LPA)
    location -> A city name (e.g. "Bangalore", "Pune") or "any"
    remote_ok -> Whether remote/work-from-home roles should be included
    max_notice_period_days -> Candidate's notice period in days (30/60/90).
        Listings that explicitly require a longer notice period are filtered out.
    """
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        return "Error: missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env"

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    search_terms = keyword if remote_ok else f"{keyword} -remote"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": search_terms,
        "salary_min": lpa_to_annual(min_salary_lpa),
        "results_per_page": 8,
        "content-type": "application/json",
    }
    if location.lower() != "any":
        params["where"] = location

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        return f"Error: job search failed with status {response.status_code}"

    jobs = response.json().get("results", [])
    if not jobs:
        return f"No jobs found for '{keyword}' in {location} with minimum {min_salary_lpa} LPA."

    lines = []
    for job in jobs:
        title = job.get("title", "Unknown title")
        company = job.get("company", {}).get("display_name", "Unknown company")
        job_location = job.get("location", {}).get("display_name", "Unknown location")
        description = (job.get("description") or "").lower()

        salary_min = job.get("salary_min")
        salary_display = f"{round(salary_min / 100000, 1)} LPA" if salary_min else "Not listed"

        is_metro = any(city in job_location.lower() for city in INDIAN_METRO_CITIES)
        tag = "Metro" if is_metro else "Tier-2/Other"

        notice_flag = ""
        for days in (30, 60, 90):
            if f"{days} day" in description or f"{days}-day" in description:
                if days > max_notice_period_days:
                    notice_flag = f" | Notice: {days} days (exceeds your {max_notice_period_days})"
                else:
                    notice_flag = f" | Notice: {days} days (OK)"

        wfh_flag = " | WFH mentioned" if "work from home" in description or "remote" in description else ""

        lines.append(
            f"- {title} at {company} ({job_location}, {tag}) | Salary: {salary_display}{notice_flag}{wfh_flag}"
        )

    return "\n".join(lines)


JOB_SEARCH_SYSTEM_PROMPT = """You are a Job Search AI Agent specialized
in the Indian job market. Given a candidate's career assessment report,
call job_search_tool with a relevant keyword, an appropriate minimum
salary in LPA based on their experience level, and a location if the
candidate has a preference. Summarize results, noting which are in
metro cities vs tier-2 cities."""

class JobSearchAgent:
    def __init__(self):
        self.tools = [job_search_tool]
        self.tools_map = {t.name: t for t in self.tools}
        self.llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0).bind_tools(self.tools)

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
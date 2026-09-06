import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.tools import tool

from app.rag_service import RAGServices

load_dotenv()



CAREER_ASSESSMENT_SYSTEM_PROMPT = """You are a Career Assessment AI Agent.
When asked to assess a candidate's profile:
1. Call fetch_resume_data to retrieve their resume information.
2. Write a Career Assessment Report covering key skills, relevant
   experience, and the type of roles they are best suited for.
Only use information returned by the tool - do not invent details."""


class CareerAssessmentAgent:
    def __init__(self, rag_service: RAGServices):
        self.rag = rag_service
        self.tools = [self._make_fetch_tool()]
        self.tools_map = {t.name: t for t in self.tools}
        self.llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0).bind_tools(self.tools)

    def _make_fetch_tool(self):
        rag = self.rag

        @tool
        def fetch_resume_data(question: str = "Summarize the candidate's education, experience, skills, and projects") -> str:
            """Fetch relevant resume data (education, experience, skills, projects) to build a career assessment."""
            return rag.query_resume(question)

        return fetch_resume_data

    def agent_node(self, state):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=CAREER_ASSESSMENT_SYSTEM_PROMPT)] + messages
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
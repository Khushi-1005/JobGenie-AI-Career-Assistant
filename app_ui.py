import streamlit as st
import os

try:
    for key in ["GEMINI_API_KEY", "GROQ_API_KEY", "ADZUNA_APP_ID", "ADZUNA_APP_KEY"]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    # No secrets.toml locally — fall back to .env (already loaded via load_dotenv elsewhere)
    pass
        
from langchain_core.messages import HumanMessage
from app.workflow import ExecuteWorkflow
from app.agents.job_search_agent import job_search_tool
from app.database import save_search, get_recent_searches

st.set_page_config(
    page_title="JobGenie AI",
    page_icon="🧞",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    .hero {
        background: linear-gradient(135deg, #151d32, #0d1424);
        padding: 35px;
        border-radius: 24px;
        border: 1px solid #27334a;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        color: white;
    }

    .hero-title span {
        color: #ff4b4b;
    }

    .hero-subtitle {
        color: #aab4c5;
        font-size: 17px;
        margin-top: 8px;
    }

    .badge {
        display: inline-block;
        margin-top: 18px;
        padding: 8px 15px;
        border-radius: 20px;
        background-color: #1b263b;
        border: 1px solid #34435d;
        color: #dbe5f5;
        font-size: 13px;
    }

    .card {
        background-color: #111827;
        border: 1px solid #27334a;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .card-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .card-text {
        color: #9aa6b8;
        font-size: 14px;
        line-height: 1.6;
    }

    .metric {
        background-color: #111827;
        border: 1px solid #27334a;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
    }

    .metric-icon {
        font-size: 25px;
    }

    .metric-value {
        color: white;
        font-size: 25px;
        font-weight: 800;
        margin-top: 5px;
    }

    .metric-label {
        color: #8f9bad;
        font-size: 13px;
        margin-top: 5px;
    }

    .result {
        background-color: #111827;
        border: 1px solid #27334a;
        border-radius: 18px;
        padding: 25px;
        margin-top: 20px;
    }

    .history-card {
        background-color: #111827;
        border: 1px solid #27334a;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .history-title {
        color: white;
        font-size: 17px;
        font-weight: 700;
    }

    .history-info {
        color: #9aa6b8;
        font-size: 13px;
        margin-top: 6px;
    }

    .footer {
        text-align: center;
        color: #667085;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #202b3d;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;">
        <div style="font-size:55px;">🧞</div>
        <h2 style="color:white;">JobGenie AI</h2>
        <p style="color:#8f9bad;">Your AI Career Copilot</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("### 🚀 Platform")
    st.write(
        "AI-powered career assessment, resume intelligence "
        "and live job search."
    )

    st.divider()
    st.markdown("### ⚡Features : ")
    st.write("✅ Live Job Search")
    st.write("✅ Salary Filtering")
    st.write("✅ Location Filtering")
    st.write("✅ WFH Detection")
    st.write("✅ SQLite History")
    st.write("✅ Streamlit UI")

    st.divider()
    st.caption("JobGenie AI")
    st.caption("Agentic AI Project")

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🧞 JobGenie <span>AI</span>
        </div>
        <div class="hero-subtitle">
            Your intelligent career copilot for resume analysis,
            job discovery and personalized career insights.
        </div>
        <div class="badge">
            🤖 Agentic AI &nbsp; • &nbsp;
            🔎 Live Job Search &nbsp; • &nbsp;
            📊 Career Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

RESUME_OPTIONS = {
    "My Resume": ("assets/Khushi_Nichang_Resume.pdf", "my_resume"),
    "Sample Resume (provided by instructor)": ("assets/AI_Developer_Resume.pdf", "sample_resume"),
}

resume_choice = st.selectbox("Choose a resume to analyze", list(RESUME_OPTIONS.keys()))

@st.cache_resource
def get_workflow(resume_path: str, collection_name: str):
    return ExecuteWorkflow(resume_path, collection_name)

searches = get_recent_searches(100)
total_searches = len(searches)

st.markdown(
    """
    <h2 style="color:white;">📊 Career Intelligence Dashboard</h2>
    <p style="color:#9aa6b8;">
    Monitor your career search activity and AI tools.
    </p>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-icon">🔎</div>
            <div class="metric-value">{total_searches}</div>
            <div class="metric-label">Job Searches</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">🤖</div>
            <div class="metric-value">AI</div>
            <div class="metric-label">Career Assessment</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">🏠</div>
            <div class="metric-value">WFH</div>
            <div class="metric-label">Remote Detection</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">💾</div>
            <div class="metric-value">SQLite</div>
            <div class="metric-label">Search History</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

tab1, tab2, tab3 = st.tabs(
    [
        "🧠 Career Assessment",
        "🔎 Smart Job Search",
        "🕘 Search History"
    ]
)

with tab1:
    st.markdown(
        """
        <h2 style="color:white;">🧠 AI Career Assessment</h2>
        <p style="color:#9aa6b8;">
        Analyze your resume and generate personalized career
        insights using your AI agent workflow.
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">🤖 Agentic Career Analysis</div>
                <div class="card-text">
                JobGenie analyzes your resume, identifies your
                skills and experience, and generates a career
                assessment.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">✨ Career Insights</div>
                <div class="card-text">
                • Skills analysis<br>
                • Career recommendations<br>
                • Job opportunities<br>
                • Salary insights<br>
                • AI-generated report
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button(
        "✨ Analyze My Profile & Find Jobs",
        type="primary",
        use_container_width=True
    ):
        with st.spinner("🤖 AI agents are analyzing your profile..."):
            try:
                resume_path, collection_name = RESUME_OPTIONS[resume_choice]
                workflow = get_workflow(resume_path, collection_name)

                input_state = {
                    "messages": [
                        HumanMessage(
                            content=(
                                "Assess my profile and generate "
                                "an evaluation report"
                            )
                        )
                    ]
                }

                result = workflow.workflow.invoke(input_state)

                st.success("Career assessment completed!")

                st.markdown(
                    '<div class="result">',
                    unsafe_allow_html=True
                )

                st.markdown(result["messages"][-1].content)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Workflow error: {e}")

with tab2:
    st.markdown(
        """
        <h2 style="color:white;">🔎 Smart Job Search</h2>
        <p style="color:#9aa6b8;">
        Search live Indian job opportunities using your preferred
        role, salary, location and notice period.
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        keyword = st.text_input(
            "💼 Job Role / Keyword",
            value="Data Scientist"
        )

    with col2:
        location = st.text_input(
            "📍 Location",
            value="Bangalore"
        )

    col3, col4 = st.columns(2)

    with col3:
        min_salary_lpa = st.number_input(
            "💰 Minimum Salary (LPA)",
            min_value=0.0,
            value=5.0,
            step=1.0
        )

    with col4:
        max_notice_period_days = st.selectbox(
            "⏳ Maximum Notice Period",
            [30, 60, 90],
            index=2
        )

    remote_ok = st.checkbox(
        "🏠 Include Work-From-Home / Remote jobs",
        value=True
    )

    st.write("")

    if st.button(
        "🚀 Search Live Jobs",
        type="primary",
        use_container_width=True
    ):
        with st.spinner("🔎 Searching live job listings..."):
            try:
                listings = job_search_tool.invoke(
                    {
                        "keyword": keyword,
                        "min_salary_lpa": min_salary_lpa,
                        "location": location,
                        "remote_ok": remote_ok,
                        "max_notice_period_days": max_notice_period_days
                    }
                )

                save_search(
                    keyword,
                    min_salary_lpa,
                    location,
                    listings
                )

                st.session_state["latest_listings"] = listings

                st.success("Job search completed!")

            except Exception as e:
                st.error(f"Job search error: {e}")

    if "latest_listings" in st.session_state:
        st.markdown(
            '<h3 style="color:white;">💼 Job Opportunities</h3>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result">',
            unsafe_allow_html=True
        )

        st.text(st.session_state["latest_listings"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

with tab3:
    st.markdown(
        """
        <h2 style="color:white;">🕘 Search History</h2>
        <p style="color:#9aa6b8;">
        Your recent job searches are stored locally using SQLite.
        </p>
        """,
        unsafe_allow_html=True
    )

    recent_searches = get_recent_searches(10)

    if recent_searches:
        for search in recent_searches:
            created_at = search["created_at"]

            if len(created_at) >= 16:
                created_at = created_at[:16]

            st.markdown(
                f"""
                <div class="history-card">
                    <div class="history-title">
                    🔎 {search["keyword"]}
                    </div>
                    <div class="history-info">
                    📍 {search["location"]}
                    &nbsp;&nbsp; | &nbsp;&nbsp;
                    💰 {search["min_salary_lpa"]} LPA
                    &nbsp;&nbsp; | &nbsp;&nbsp;
                    🕘 {created_at}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info(
            "No searches yet. Perform a job search first."
        )

st.markdown(
    """
    <div class="footer">
        🧞 <b>JobGenie AI</b>
        — Agentic Career Intelligence Platform
        <br><br>
        Python • LangGraph • RAG • SQLite • Streamlit
        <br>
        Development Milestone
    </div>
    """,
    unsafe_allow_html=True
)

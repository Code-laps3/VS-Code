import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from sqlalchemy import text

# ============================================================
# PAGE CONFIG (Must be at the top)
# ============================================================
st.set_page_config(
    page_title="Study Schedule",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    .block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem; }
    .main-title { font-size: 3rem; font-weight: 800; margin-bottom: 0; }
    .subtitle { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }
    [data-testid="stMetric"] { background-color: #1e293b; border: 1px solid #334155; padding: 1rem; border-radius: 14px; }
    .stButton > button { border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE INITIALIZATION
# ============================================================
conn = st.connection("postgres", type="sql")

try:
    with conn.engine.connect() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                subject TEXT PRIMARY KEY,
                exam_date DATE NOT NULL,
                hardest_topics TEXT,
                medium_topics TEXT,
                easy_topics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        session.commit()
except Exception as e:
    st.error(f"Database setup error: {e}")

# ============================================================
# DATABASE HELPER FUNCTIONS (Must be defined before usage)
# ============================================================
def load_exams():
    try:
        df = conn.query("SELECT subject, exam_date, hardest_topics, medium_topics, easy_topics FROM study_sessions ORDER BY exam_date ASC;", ttl="0s")
        
        exams_dict = {}
        for row in df.to_dict(orient="records"):
            exam_dt = row["exam_date"]
            if isinstance(exam_dt, str):
                exam_dt = datetime.strptime(exam_dt, "%Y-%m-%d").date()
            elif isinstance(exam_dt, pd.Timestamp):
                exam_dt = exam_dt.date()

            exams_dict[row["subject"]] = {
                "Exam Date": exam_dt,
                "Revision Date": exam_dt - timedelta(days=1),
                "Paper Date 1": exam_dt - timedelta(days=3),
                "Paper Date 2": exam_dt - timedelta(days=5),
                "Easy Study Date": exam_dt - timedelta(days=7),
                "Medium Study Date": exam_dt - timedelta(days=9),
                "Hard Study Date": exam_dt - timedelta(days=11),
                "Hardest Topics": row["hardest_topics"] or "",
                "Medium Topics": row["medium_topics"] or "",
                "Easy Topics": row["easy_topics"] or ""

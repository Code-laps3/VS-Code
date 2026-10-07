import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from sqlalchemy import text

# ============================================================
# PAGE CONFIG
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
# NEON POSTGRESQL CONNECTION
# ============================================================
DATABASE_URL = "postgresql://neondb_owner:npg_rcv9u1okSKyi@ep-weathered-unit-b48cjlbm-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = st.connection("neon_db", type="sql", url=DATABASE_URL)

try:
    with conn.engine.connect() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS user_study_sessions (
                user_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                exam_date DATE NOT NULL,
                hardest_topics TEXT,
                medium_topics TEXT,
                easy_topics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, subject)
            );
        """))
        session.commit()
except Exception as e:
    st.error(f"Database initialization error: {e}")

# ============================================================
# DATABASE HELPER FUNCTIONS
# ============================================================
def load_user_exams(user_id):
    try:
        df = conn.query(
            "SELECT subject, exam_date, hardest_topics, medium_topics, easy_topics FROM user_study_sessions WHERE user_id = :u_id ORDER BY exam_date ASC;",
            params={"u_id": user_id},
            ttl="0s"
        )
        
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
            }
        return exams_dict
    except Exception as e:
        st.error(f"Error loading exams: {e}")
        return {}

def save_user_exam(user_id, subject_name, exam_info):
    try:
        with conn.engine.connect() as session:
            session.execute(
                text("""
                    INSERT INTO user_study_sessions (user_id, subject, exam_date, hardest_topics, medium_topics, easy_topics)
                    VALUES (:user_id, :subject, :exam_date, :hard, :medium, :easy)
                    ON CONFLICT (user_id, subject) DO UPDATE SET
                        exam_date = EXCLUDED.exam_date,
                        hardest_topics = EXCLUDED.hardest_topics,
                        medium_topics = EXCLUDED.medium_topics,
                        easy_topics = EXCLUDED.easy_topics;
                """),
                {
                    "user_id": user_id,
                    "subject": subject_name,
                    "exam_date": str(exam_info["Exam Date"]),
                    "hard": exam_info["Hardest Topics"],
                    "medium": exam_info["Medium Topics"],
                    "easy": exam_info["Easy Topics"]
                }
            )
            session.commit()
    except Exception as e:
        st.error(f"Error saving to database: {e}")

def delete_user_exam(user_id, subject_name):
    try:
        with conn.engine.connect() as session:
            session.execute(
                text("DELETE FROM user_study_sessions WHERE user_id = :user_id AND subject = :subject;"),
                {"user_id": user_id, "subject": subject_name}
            )
            session.commit()
    except Exception as e:
        st.error(f"Error deleting exam: {e}")

# ============================================================
# USER SELECTION / AUTHENTICATION
# ============================================================
st.sidebar.title("👤 User Login")
user_name = st.sidebar.text_input("Enter Student ID / Name:", value="Student 1")

if not user_name.strip():
    st.warning("Please enter your Student ID or Name in the sidebar to view your study schedule.")
    st.stop()

current_user = user_name.strip().lower()

# Load exams for active student from Neon DB
exams = load_user_exams(current_user)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">📚 Study Sensi</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">'
    f'Active Profile: <strong>{user_name.strip()}</strong> | 1–3–5–7–9–11 day revision schedule.'
    f'</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR — ADD EXAM
# ============================================================
with st.sidebar:
    st.header("➕ Add Exam")
    st.write("Enter exam details to generate your schedule.")

    with st.form("exam_form"):
        exam_name = st.text_input("Subject", placeholder="e.g. Mathematics")
        exam_date_val = st.date_input("Exam date", value=date.today() + timedelta(days=14))

        st.subheader("📖 Topics")
        hardest_topics = st.text_input("Hardest topics", placeholder="e.g. Trigonometry, Algebra")
        medium_topics = st.text_input("Medium topics", placeholder="e.g. Functions, Graphs")
        easy_topics = st.text_input("Easy topics", placeholder="e.g. Statistics, Probability")

        save_exam = st.form_submit_button("💾 Save Exam", use_container_width=True)

if save_exam:
    if not exam_name.strip():
        st.error("Please enter a subject name.")
    else:
        subject_key = exam_name.strip()
        exam_data = {
            "Exam Date": exam_date_val,
            "Revision Date": exam_date_val - timedelta(days=1),
            "Paper Date 1": exam_date_val - timedelta(days=3),
            "Paper Date 2": exam_date_val - timedelta(days=5),
            "Easy Study Date": exam_date_val - timedelta(days=7),
            "Medium Study Date": exam_date_val - timedelta(days=9),
            "Hard Study Date": exam_date_val - timedelta(days=11),
            "Hardest Topics": hardest_topics,
            "Medium Topics": medium_topics,
            "Easy Topics": easy_topics
        }
        save_user_exam(current_user, subject_key, exam_data)
        st.success(f"{subject_key} saved for {user_name.strip()}!")
        st.rerun()

# ============================================================
# DASHBOARD STATISTICS
# ============================================================
st.subheader("📊 Your Study Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Exams", len(exams))

with col2:
    upcoming = sum(1 for exam in exams.values() if exam.get("Exam Date") and exam["Exam Date"] >= date.today())
    st.metric("Upcoming Exams", upcoming)

with col3:
    total_tasks = len(exams) * 6
    st.metric("Study Sessions", total_tasks)

# ============================================================
# EXAMS LIST
# ============================================================
st.subheader("📝 Your Exams")

if not exams:
    st.info("No exams added yet for this student ID. Use the sidebar on the left to add your first exam.")
else:
    exam_to_delete = None

    for exam_name, exam_info in exams.items():
        exam_dt = exam_info["Exam Date"]
        days_until_exam = (exam_dt - date.today()).days

        with st.expander(f"📚 {exam_name} — {exam_dt.strftime('%d %B %Y')}", expanded=False):
            if days_until_exam > 0:
                st.info(f"⏳ {days_until_exam} days until this exam")
            elif days_until_exam == 0:
                st.warning("🔥 The exam is today!")
            else:
                st.write(f"This exam was {abs(days_until_exam)} days ago.")

            st.markdown("### 📅 Revision Schedule")

            schedule = [
                (exam_info["Hard Study Date"], "11 DAYS BEFORE", "🧠 Study hardest topics", exam_info["Hardest Topics"]),
                (exam_info["Medium Study Date"], "9 DAYS BEFORE", "📖 Study medium topics", exam_info["Medium Topics"]),
                (exam_info["Easy Study Date"], "7 DAYS BEFORE", "📘 Study easy topics", exam_info["Easy Topics"]),
                (exam_info["Paper Date 2"], "5 DAYS BEFORE", "📝 Do mixed past papers", ""),
                (exam_info["Paper Date 1"], "3 DAYS BEFORE", "📝 Do mixed past papers", ""),
                (exam_info["Revision Date"], "1 DAY BEFORE", "🔄 Light revision of all content", "Revise all content")
            ]

            for study_date, timing, task, topics in schedule:
                with st.container(border=True):
                    st.caption(timing)
                    st.write(f"**{study_date.strftime('%A, %d %B %Y')}**")
                    st.write(task)
                    if topics:
                        st.write(f"📚 **Topics:** {topics}")

            if st.button(f"🗑️ Delete {exam_name}", key=f"delete_{exam_name}"):
                exam_to_delete = exam

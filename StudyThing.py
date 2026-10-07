import json
import os
from datetime import date, timedelta
import streamlit as st

EXAMS_FILE = "exams.json"


def save_exams():
    """Save all exams permanently to a JSON file."""
    data = {}
    for exam_name, exam_info in st.session_state.exams.items():
        data[exam_name] = {
            key: value.isoformat() if isinstance(value, date) else value
            for key, value in exam_info.items()
        }

    with open(EXAMS_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_exams():
    """Load saved exams from the JSON file."""
    if not os.path.exists(EXAMS_FILE):
        return {}

    with open(EXAMS_FILE, "r") as file:
        data = json.load(file)

    date_keys = [
        "Exam Date",
        "Revision Date",
        "Paper Date 1",
        "Paper Date 2",
        "Easy Study Date",
        "Medium Study Date",
        "Hard Study Date",
    ]

    for exam_info in data.values():
        for key in date_keys:
            if key in exam_info:
                exam_info[key] = date.fromisoformat(exam_info[key])

    return data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="Study Schedule", page_icon="📚", layout="wide")


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
<style>
    /* Main background */
    .stApp {
        background-color: #0f172a;
    }

    /* Main content */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Exam cards */
    .exam-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 1rem;
        border-radius: 14px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
if "exams" not in st.session_state:
    st.session_state.exams = load_exams()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📚 Study Sensi</div>', unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "Your personalised exam revision planner using the 1–3–5–7–9–11 day system."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — ADD EXAM
# ============================================================

with st.sidebar:
    st.header("➕ Add Exam")
    st.write(
        "Enter your exam details and Study Sensi will build your revision schedule."
    )

    with st.form("exam_form"):
        exam_name = st.text_input("Subject", placeholder="e.g. Mathematics")
        exam_date = st.date_input(
            "Exam date", value=date.today() + timedelta(days=14)
        )

        st.subheader("📖 Topics")
        hardest_topics = st.text_input(
            "Hardest topics", placeholder="e.g. Trigonometry, Algebra"
        )
        medium_topics = st.text_input(
            "Medium topics", placeholder="e.g. Functions, Graphs"
        )
        easy_topics = st.text_input(
            "Easy topics", placeholder="e.g. Statistics, Probability"
        )

        save_exam = st.form_submit_button(
            "💾 Save Exam", use_container_width=True
        )


# ============================================================
# SAVE EXAM
# ============================================================

if save_exam:
    if not exam_name.strip():
        st.error("Please enter a subject name.")
    else:
        revision_date = exam_date - timedelta(days=1)
        paper_date_1 = exam_date - timedelta(days=3)
        paper_date_2 = exam_date - timedelta(days=5)
        easy_date = exam_date - timedelta(days=7)
        medium_date = exam_date - timedelta(days=9)
        hard_date = exam_date - timedelta(days=11)

        st.session_state.exams[exam_name.strip()] = {
            "Exam Date": exam_date,
            "Revision Date": revision_date,
            "Paper Date 1": paper_date_1,
            "Paper Date 2": paper_date_2,
            "Easy Study Date": easy_date,
            "Medium Study Date": medium_date,
            "Hard Study Date": hard_date,
            "Hardest Topics": hardest_topics,
            "Medium Topics": medium_topics,
            "Easy Topics": easy_topics,
        }
        save_exams()
        st.success(f"{exam_name} has been added!")


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

st.subheader("📊 Your Study Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Exams", len(st.session_state.exams))

with col

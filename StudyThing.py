import streamlit as st
from datetime import date, timedelta

import streamlit as st
import pandas as pd
from datetime import date

# Establish Google Sheets connection
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

DATE_KEYS = [
    "Exam Date",
    "Revision Date",
    "Paper Date 1",
    "Paper Date 2",
    "Easy Study Date",
    "Medium Study Date",
    "Hard Study Date"
]

def save_exams():
    """Save exams directly to Google Sheets."""
    if "exams" not in st.session_state or not st.session_state.exams:
        st.warning("⚠️ No exam data found in session state to save.")
        return

    rows = []
    # Convert st.session_state.exams into tabular rows
    for exam_name, exam_info in st.session_state.exams.items():
        row = {"Exam Name": exam_name}
        for k, v in exam_info.items():
            row[k] = v.isoformat() if isinstance(v, date) else str(v)
        rows.append(row)
    
    try:
        df = pd.DataFrame(rows)
        # Write to Google Sheet
        conn.update(data=df)
        st.success("✅ Exams successfully saved to Google Sheet!")
    except Exception as e:
        st.error(f"❌ Failed to save to Google Sheet: {e}")


def load_exams():
    """Load saved exams directly from Google Sheets."""
    try:
        df = conn.read(ttl=0) # ttl=0 forces fresh fetch
        if df.empty:
            return {}
        
        data = {}
        for _, row in df.iterrows():
            exam_name = row["Exam Name"]
            exam_info = row.drop("Exam Name").to_dict()
            
            # Convert ISO date strings back into date objects
            for key in DATE_KEYS:
                if key in exam_info and pd.notna(exam_info[key]):
                    exam_info[key] = date.fromisoformat(str(exam_info[key]))
            
            data[exam_name] = exam_info
            
        return data
    except Exception as e:
        st.warning(f"Could not load data from Google Sheet: {e}")
        return {}

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

    .exam-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .exam-date {
        color: #94a3b8;
        margin-bottom: 1rem;
    }

    /* Schedule boxes */
    .schedule-box {
        background-color: #172033;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.5rem;
        border-left: 4px solid #6366f1;
    }

    .schedule-date {
        font-weight: 700;
        font-size: 1.05rem;
    }

    .schedule-type {
        color: #a5b4fc;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
    }

    .topics {
        color: #cbd5e1;
        margin-top: 0.25rem;
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
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "exams" not in st.session_state:
    st.session_state.exams = load_exams()

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-title">📚 Study Sensi</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    'Your personalised exam revision planner using the 1–3–5–7–9–11 day system.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR — ADD EXAM
# ============================================================

with st.sidebar:

    st.header("➕ Add Exam")

    st.write(
        "Enter your exam details and Study Sensi will build your revision schedule.")

    with st.form("exam_form"):

        exam_name = st.text_input(
            "Subject",
            placeholder="e.g. Mathematics"
        )

        exam_date = st.date_input(
            "Exam date",
            value=date.today() + timedelta(days=14)
        )

        st.subheader("📖 Topics")

        hardest_topics = st.text_input(
            "Hardest topics",
            placeholder="e.g. Trigonometry, Algebra"
        )

        medium_topics = st.text_input(
            "Medium topics",
            placeholder="e.g. Functions, Graphs"
        )

        easy_topics = st.text_input(
            "Easy topics",
            placeholder="e.g. Statistics, Probability"
        )

        save_exam = st.form_submit_button(
            "💾 Save Exam",
            use_container_width=True
        )


# ============================================================
# SAVE EXAM
# ============================================================

if save_exam:

    if not exam_name.strip():
        st.error("Please enter a subject name.")

    else:

        # ----------------------------------------------------
        # Calculate all study dates
        # ----------------------------------------------------

        revision_date = exam_date - timedelta(days=1)

        paper_date_1 = exam_date - timedelta(days=3)

        paper_date_2 = exam_date - timedelta(days=5)

        easy_date = exam_date - timedelta(days=7)

        medium_date = exam_date - timedelta(days=9)

        hard_date = exam_date - timedelta(days=11)

        # ----------------------------------------------------
        # Save everything
        # ----------------------------------------------------

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

            "Easy Topics": easy_topics
        }
        save_exams()

        st.success(f"{exam_name} has been added!")


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

st.subheader("📊 Your Study Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Exams",
        len(st.session_state.exams)
    )

with col2:
    upcoming = 0

    for exam_info in st.session_state.exams.values():
        if exam_info["Exam Date"] >= date.today():
            upcoming += 1

    st.metric(
        "Upcoming Exams",
        upcoming
    )

with col3:
    total_tasks = len(st.session_state.exams) * 6

    st.metric(
        "Study Sessions",
        total_tasks
    )


# ============================================================
# EXAMS
# ============================================================

st.subheader("📝 Your Exams")


if not st.session_state.exams:

    st.info(
        "You don't have any exams yet. "
        "Use the panel on the left to add your first exam."
    )

else:

    exam_to_delete = None

    for exam_name, exam_info in st.session_state.exams.items():

        exam_date = exam_info["Exam Date"]
        days_until_exam = (exam_date - date.today()).days

        # ====================================================
        # EXAM DROPDOWN
        # ====================================================

        with st.expander(
            f"📚 {exam_name} — {exam_date.strftime('%d %B %Y')}",
            expanded=False
        ):

            # ------------------------------------------------
            # COUNTDOWN
            # ------------------------------------------------

            if days_until_exam > 0:

                st.info(
                    f"⏳ {days_until_exam} days until this exam"
                )

            elif days_until_exam == 0:

                st.warning("🔥 The exam is today!")

            else:

                st.write(
                    f"This exam was {abs(days_until_exam)} days ago."
                )

            # ------------------------------------------------
            # REVISION SCHEDULE
            # ------------------------------------------------

            st.markdown("### 📅 Revision Schedule")

            schedule = [

                (
                    exam_info["Hard Study Date"],
                    "11 DAYS BEFORE",
                    "🧠 Study hardest topics",
                    exam_info["Hardest Topics"]
                ),

                (
                    exam_info["Medium Study Date"],
                    "9 DAYS BEFORE",
                    "📖 Study medium topics",
                    exam_info["Medium Topics"]
                ),

                (
                    exam_info["Easy Study Date"],
                    "7 DAYS BEFORE",
                    "📘 Study easy topics",
                    exam_info["Easy Topics"]
                ),

                (
                    exam_info["Paper Date 2"],
                    "5 DAYS BEFORE",
                    "📝 Do mixed past papers",
                    ""
                ),

                (
                    exam_info["Paper Date 1"],
                    "3 DAYS BEFORE",
                    "📝 Do mixed past papers",
                    ""
                ),

                (
                    exam_info["Revision Date"],
                    "1 DAY BEFORE",
                    "🔄 Light revision of all content",
                    "Revise all content"
                )
            ]

            # ------------------------------------------------
            # DISPLAY EACH SESSION
            # ------------------------------------------------

            for study_date, timing, task, topics in schedule:

                with st.container(border=True):

                    st.caption(timing)

                    st.write(
                        f"**{study_date.strftime('%A, %d %B %Y')}**"
                    )

                    st.write(task)

                    if topics:
                        st.write(
                            f"📚 **Topics:** {topics}"
                        )

            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            if st.button(
                f"🗑️ Delete {exam_name}",
                key=f"delete_{exam_name}"
            ):
                exam_to_delete = exam_name

    # DELETE AFTER THE LOOP
    if exam_to_delete is not None:
        del st.session_state.exams[exam_to_delete]
        save_exams()
        st.rerun()

from datetime import date, timedelta
import json
import pandas as pd
import streamlit as st

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
# SESSION STATE INITIALIZATION
# ============================================================
if "exams" not in st.session_state:
    st.session_state.exams = {}

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
# SIDEBAR — DATA IMPORT/EXPORT, ADD EXAM, & EDIT EXAM
# ============================================================

with st.sidebar:
    st.header("📂 Backup & Restore")

    # Upload JSON File to load session
    uploaded_file = st.file_uploader(
        "Load schedule JSON file",
        type=["json"],
        help="Upload a previously exported schedule.",
    )

    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            date_keys = [
                "Exam Date",
                "Revision Date",
                "Mixed Practice Date 1",
                "Mixed Practice Date 2",
                "Easy Study Date",
                "Medium Study Date",
                "Hard Study Date",
            ]

            # Convert loaded date strings into date objects
            for exam_info in imported_data.values():
                for key in date_keys:
                    if key in exam_info and isinstance(exam_info[key], str):
                        exam_info[key] = date.fromisoformat(exam_info[key])

            st.session_state.exams.update(imported_data)
            st.success("Schedules loaded successfully!")
        except Exception as e:
            st.error(f"Error loading JSON file: {e}")

    # Export all session exams as single JSON file
    if st.session_state.exams:
        all_exams_json = json.dumps(
            {
                exam_name: {
                    k: v.isoformat() if isinstance(v, date) else v
                    for k, v in exam_info.items()
                }
                for exam_name, exam_info in st.session_state.exams.items()
            },
            indent=4,
        )
        st.download_button(
            label="💾 Download All Data (.json)",
            data=all_exams_json,
            file_name="study_schedule_backup.json",
            mime="application/json",
            use_container_width=True,
        )

    st.divider()

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
            "➕ Add to Schedule", use_container_width=True
        )

    # ============================================================
    # EDIT EXAM SECTION
    # ============================================================
    if st.session_state.exams:
        st.divider()
        st.header("✏️ Edit Exam")

        change_exam = st.selectbox(
            "Change Exam", options=list(st.session_state.exams.keys())
        )

        if change_exam:
            what_to_change = st.selectbox(
                "What do you want to change?",
                options=list(st.session_state.exams[change_exam].keys()),
            )

            current_value = st.session_state.exams[change_exam][what_to_change]

            # Use appropriate input element depending on whether it's a date or text
            if isinstance(current_value, date):
                new_value = st.date_input(
                    f"Enter new value for {what_to_change}", value=current_value
                )
            else:
                new_value = st.text_input(
                    f"Enter new value for {what_to_change}",
                    value=str(current_value),
                )

            if st.button("Update", use_container_width=True):
                st.session_state.exams[change_exam][what_to_change] = new_value

                # If Exam Date is updated, recalculate all dependent schedule dates automatically
                if what_to_change == "Exam Date":
                    new_exam_date = new_value
                    st.session_state.exams[change_exam]["Revision Date"] = (
                        new_exam_date - timedelta(days=1)
                    )
                    st.session_state.exams[change_exam][
                        "Mixed Practice Date 1"
                    ] = (new_exam_date - timedelta(days=3))
                    st.session_state.exams[change_exam][
                        "Mixed Practice Date 2"
                    ] = (new_exam_date - timedelta(days=5))
                    st.session_state.exams[change_exam]["Easy Study Date"] = (
                        new_exam_date - timedelta(days=7)
                    )
                    st.session_state.exams[change_exam]["Medium Study Date"] = (
                        new_exam_date - timedelta(days=9)
                    )
                    st.session_state.exams[change_exam]["Hard Study Date"] = (
                        new_exam_date - timedelta(days=11)
                    )

                st.success(f"Updated {what_to_change} for {change_exam}!")
                st.rerun()


# ============================================================
# SAVE EXAM TO SESSION STATE
# ============================================================

if save_exam:
    if not exam_name.strip():
        st.error("Please enter a subject name.")
    else:
        revision_date = exam_date - timedelta(days=1)
        mixed_practice_1 = exam_date - timedelta(days=3)
        mixed_practice_2 = exam_date - timedelta(days=5)
        easy_date = exam_date - timedelta(days=7)
        medium_date = exam_date - timedelta(days=9)
        hard_date = exam_date - timedelta(days=11)

        st.session_state.exams[exam_name.strip()] = {
            "Exam Date": exam_date,
            "Revision Date": revision_date,
            "Mixed Practice Date 1": mixed_practice_1,
            "Mixed Practice Date 2": mixed_practice_2,
            "Easy Study Date": easy_date,
            "Medium Study Date": medium_date,
            "Hard Study Date": hard_date,
            "Hardest Topics": hardest_topics,
            "Medium Topics": medium_topics,
            "Easy Topics": easy_topics,
        }
        st.success(f"{exam_name} has been added!")
        st.rerun()


# ============================================================
# DASHBOARD STATISTICS & OVERVIEW TABLE
# ============================================================

st.subheader("📊 Your Study Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Exams", len(st.session_state.exams))

with col2:
    upcoming = sum(
        1
        for exam_info in st.session_state.exams.values()
        if exam_info["Exam Date"] >= date.today()
    )
    st.metric("Upcoming Exams", upcoming)

with col3:
    total_tasks = len(st.session_state.exams) * 6
    st.metric("Study Sessions", total_tasks)

# Display schedule overview table if exams exist
if st.session_state.exams:
    st.markdown("### 🗓️ Schedule Overview Table")
    confusion_matrix = pd.DataFrame(
        {
            "Exam Date": [
                info["Exam Date"].strftime("%d %b %Y")
                for info in st.session_state.exams.values()
            ],
            "Hard Topics": [
                info["Hard Study Date"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
            "Medium Topics": [
                info["Medium Study Date"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
            "Easy Topics": [
                info["Easy Study Date"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
            "Mixed Practice 2": [
                info["Mixed Practice Date 2"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
            "Mixed Practice 1": [
                info["Mixed Practice Date 1"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
            "Final Revision": [
                info["Revision Date"].strftime("%d %b")
                for info in st.session_state.exams.values()
            ],
        },
        index=list(st.session_state.exams.keys()),
    )
    st.table(confusion_matrix)


# ============================================================
# EXAMS
# ============================================================

st.subheader("📝 Your Exams")

if not st.session_state.exams:

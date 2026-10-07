import streamlit as st
from datetime import date, datetime, timedelta
import calendar
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Study Schedule Generator",
    page_icon="📅",
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
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION (In-Memory Only)
# ============================================================
if "exams" not in st.session_state:
    st.session_state.exams = {}

# ============================================================
# CALENDAR IMAGE GENERATOR FUNCTION
# ============================================================
def generate_calendar_image(exams_dict):
    """Generates a visual calendar image containing all study dates and exam days."""
    if not exams_dict:
        return None

    # Collect all key dates across all exams
    event_map = {}  # date -> list of strings
    
    colors = {
        "Exam": "#ef4444",         # Red
        "Light Revision": "#f59e0b",# Amber
        "Past Paper": "#3b82f6",    # Blue
        "Easy Topics": "#10b981",   # Green
        "Medium Topics": "#8b5cf6", # Purple
        "Hard Topics": "#ec4899"    # Pink
    }

    all_dates = []
    for subject, info in exams_dict.items():
        exam_dt = info["Exam Date"]
        all_dates.append(exam_dt)

        schedule = [
            (exam_dt, f"🔥 EXAM: {subject}", colors["Exam"]),
            (exam_dt - timedelta(days=1), f"🔄 Light Rev: {subject}", colors["Light Revision"]),
            (exam_dt - timedelta(days=3), f"📝 Paper 1: {subject}", colors["Past Paper"]),
            (exam_dt - timedelta(days=5), f"📝 Paper 2: {subject}", colors["Past Paper"]),
            (exam_dt - timedelta(days=7), f"📘 Easy: {subject}", colors["Easy Topics"]),
            (exam_dt - timedelta(days=9), f"📖 Med: {subject}", colors["Medium Topics"]),
            (exam_dt - timedelta(days=11), f"🧠 Hard: {subject}", colors["Hard Topics"])
        ]

        for d, label, col in schedule:
            all_dates.append(d)
            if d not in event_map:
                event_map[d] = []
            event_map[d].append((label, col))

    min_date = min(all_dates)
    max_date = max(all_dates)

    # Determine unique months to plot
    months_to_plot = []
    curr = min_date.replace(day=1)
    end_month = max_date.replace(day=1)
    while curr <= end_month:
        months_to_plot.append((curr.year, curr.month))
        # Advance to next month
        if curr.month == 12:
            curr = date(curr.year + 1, 1, 1)
        else:
            curr = date(curr.year, curr.month + 1, 1)

    # Setup matplotlib plot grid
    n_months = len(months_to_plot)
    fig, axes = plt.subplots(n_months, 1, figsize=(14, 6 * n_months), facecolor="#0f172a")
    if n_months == 1:
        axes = [axes]

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for idx, (yr, mo) in enumerate(months_to_plot):
        ax = axes[idx]
        ax.set_facecolor("#1e293b")
        ax.axis("off")

        # Title of Month
        month_name = date(yr, mo, 1).strftime("%B %Y")
        ax.text(3.5, 6.5, month_name, fontsize=18, fontweight="bold", color="#f8fafc", ha="center", va="center")

        # Header Days
        for col, day_name in enumerate(day_names):
            ax.text(col + 0.5, 5.7, day_name, fontsize=12, fontweight="bold", color="#94a3b8", ha="center", va="center")

        # Draw Grid & Days
        cal = calendar.monthcalendar(yr, mo)
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                x = col_idx
                y = 5 - row_idx - 0.2

                if day != 0:
                    curr_date = date(yr, mo, day)
                    is_today = (curr_date == date.today())
                    
                    # Cell border
                    border_col = "#38bdf8" if is_today else "#334155"
                    bg_col = "#0f172a" if is_today else "#1e293b"

                    rect = patches.Rectangle((x + 0.05, y - 0.75), 0.9, 0.9, linewidth=1.5,
                                             edgecolor=border_col, facecolor=bg_col, rx=0.08)
                    ax.add_patch(rect)

                    # Day Number
                    num_col = "#38bdf8" if is_today else "#f8fafc"
                    ax.text(x + 0.12, y + 0.05, str(day), fontsize=10, fontweight="bold", color=num_col)

                    # Events on this day
                    if curr_date in event_map:
                        events = event_map[curr_date]
                        for e_idx, (lbl, c_code) in enumerate(events[:3]): # Max 3 per box
                            e_y = y - 0.22 - (e_idx * 0.2)
                            tag_rect = patches.Rectangle((x + 0.08, e_y - 0.08), 0.84, 0.16,
                                                         linewidth=0, facecolor=c_code, alpha=0.85, rx=0.04)
                            ax.add_patch(tag_rect)
                            ax.text(x + 0.5, e_y, lbl[:16], fontsize=6.5, color="#ffffff",
                                    fontweight="bold", ha="center", va="center")

        ax.set_xlim(0, 7)
        ax.set_ylim(-0.5, 7)

    plt.tight_layout()
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">📅 Revision Schedule Visualizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">'
    'Input your exams to generate a revision calendar picture. (No data is saved online or locally)'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR — INPUT EXAMS
# ============================================================
with st.sidebar:
    st.header("➕ Add Exam")
    st.write("Enter exam details below:")

    with st.form("exam_form"):
        exam_name = st.text_input("Subject", placeholder="e.g. Mathematics")
        exam_date_val = st.date_input("Exam date", value=date.today() + timedelta(days=14))

        st.subheader("📖 Topics (Optional)")
        hardest_topics = st.text_input("Hardest topics", placeholder="e.g. Algebra")
        medium_topics = st.text_input("Medium topics", placeholder="e.g. Graphs")
        easy_topics = st.text_input("Easy topics", placeholder="e.g. Statistics")

        add_exam = st.form_submit_button("➕ Add to Schedule", use_container_width=True)

    if add_exam:
        if not exam_name.strip():
            st.error("Please enter a subject name.")
        else:
            subject_key = exam_name.strip()
            st.session_state.exams[subject_key] = {
                "Exam Date": exam_date_val,
                "Hardest Topics": hardest_topics,
                "Medium Topics": medium_topics,
                "Easy Topics": easy_topics
            }
            st.success(f"Added {subject_key}!")
            st.rerun()

    if st.session_state.exams:
        if st.button("🗑️ Clear All Exams", use_container_width=True):
            st.session_state.exams = {}
            st.rerun()

# ============================================================
# MAIN CONTENT — CALENDAR IMAGE GENERATOR
# ============================================================
if not st.session_state.exams:
    st.info("👈 Add your exams using the sidebar on the left to create your visual calendar image.")
else:
    st.subheader("🖼️ Generated Revision Calendar")

    with st.spinner("Generating calendar image..."):
        fig = generate_calendar_image(st.session_state.exams)
        if fig:
            st.pyplot(fig)

    # Detailed List View below image
    st.markdown("---")
    st.subheader("📝 Scheduled Exams Summary")
    
    for subject, info in st.session_state.exams.items():
        exam_dt = info["Exam Date"]
        with st.expander(f"📚 {subject} — {exam_dt.strftime('%d %B %Y')}"):
            st.write(f"• **Hard Study Date (11 Days Before):** {(exam_dt - timedelta(days=11)).strftime('%A, %d %B %Y')}")
            st.write(f"• **Medium Study Date (9 Days Before):** {(exam_dt - timedelta(days=9)).strftime('%A, %d %B %Y')}")
            st.write(f"• **Easy Study Date (7 Days Before):** {(exam_dt - timedelta(days=7)).strftime('%A, %d %B %Y')}")
            st.write(f"• **Past Paper 2 (5 Days Before):** {(exam_dt - timedelta(days=5)).strftime('%A, %d %B %Y')}")
            st.write(f"• **Past Paper 1 (3 Days Before):** {(exam_dt - timedelta(days=3)).strftime('%A, %d %B %Y')}")
            st.write(f"• **Light Revision (1 Day Before):** {(exam_dt - timedelta(days=1)).strftime('%A, %d %B %Y')}")

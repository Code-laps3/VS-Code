import streamlit as st
from datetime import datetime
import pandas as pd
st.title("Study Sensi")

# Sessions
if "exams" not in st.session_state:
    st.session_state.exams = {}
if "new_exam" not in st.session_state:
    st.session_state.new_exam = False

if st.button("New Exam"):
    st.session_state.new_exam = True
    st.session_state.exams = {}


# Getting month and day of exam date
if st.session_state.new_exam:
    exam_name = st.text_input("What subject is it")
    exam_dayraw = st.text_input("What day is the exam?(1-31) ")
    exam_month = st.text_input("What month is the exam?(1-12) ")
    hardest_topics = st.text_input(
        "Based on the scope what are the hardest topics? (separate with commas) ")
    medium_topics = st.text_input(
        "Based on the scope what are the medium topics? (separate with commas) ")
    easy_topics = st.text_input(
        "Based on the scope what are the easy topics? (separate with commas) ")
    if exam_month == "2" or "4" or "6" or "8" or "9" or "11":
        x = 30
    if exam_month == "1" or "3" or "5" or "7" or "10" or "12":
        x = 31
    if exam_month == "3":
        x = 28

    if int(exam_dayraw) < 2:
        RevDay = x - (1 - int(exam_dayraw))
        RevMonth = int(exam_month) - 1
    else:
        RevDay = int(exam_dayraw)-1
        RevMonth = int(exam_month)

    if int(exam_dayraw) < 4:
        PaperDay1 = x - (3 - int(exam_dayraw))
        PaperMonth1 = int(exam_month) - 1
    else:
        PaperDay1 = int(exam_dayraw)-3
        PaperMonth1 = int(exam_month)

    if int(exam_dayraw) < 6:
        PaperDay2 = x - (5 - int(exam_dayraw))
        PaperMonth2 = int(exam_month) - 1
    else:
        PaperDay2 = int(exam_dayraw)-5
        PaperMonth2 = int(exam_month)

    if int(exam_dayraw) < 8:
        EasyStudy = x - (7 - int(exam_dayraw))
        EasyMonth = int(exam_month) - 1
    else:
        EasyStudy = int(exam_dayraw)-7
        EasyMonth = int(exam_month)

    if int(exam_dayraw) < 10:
        MediumStudy = x - (9 - int(exam_dayraw))
        MediumMonth = int(exam_month) - 1
    else:
        MediumStudy = int(exam_dayraw)-9
        MediumMonth = int(exam_month)

    if int(exam_dayraw) < 12:
        HardStudy = x - (11 - int(exam_dayraw))
        HardMonth = int(exam_month) - 1
    else:
        HardStudy = int(exam_dayraw)-11
        HardMonth = int(exam_month)


if st.button("Save Exam"):
    st.session_state.exams[exam_name] = {
        "Day": exam_dayraw,
        "Month": exam_month,
        "Revision Day": RevDay,
        "Revision Month": RevMonth,
        "Paper Day 1": PaperDay1,
        "Paper Month 1": PaperMonth1,
        "Paper Day 2": PaperDay2,
        "Paper Month 2": PaperMonth2,
        "Easy Study Day": EasyStudy,
        "Easy Study Month": EasyMonth,
        "Medium Study Day": MediumStudy,
        "Medium Study Month": MediumMonth,
        "Hard Study Day": HardStudy,
        "Hard Study Month": HardMonth,
        "Hardest Topics": hardest_topics,
        "Medium Topics": medium_topics,
        "Easy Topics": easy_topics
    }

st.header("Exams")

for exam_name, exam_info in st.session_state.exams.items():
    st.write(f"**{exam_name}**")

    st.write(
        f"Revise all content on {exam_info['Revision Day']}/{exam_info['Revision Month']}. "
        f"Do mixed past papers on {exam_info['Paper Day 1']}/{exam_info['Paper Month 1']} "
        f"and {exam_info['Paper Day 2']}/{exam_info['Paper Month 2']}. "
        f"Study {exam_info['Easy Topics']} on "
        f"{exam_info['Easy Study Day']}/{exam_info['Easy Study Month']}, "
        f"the {exam_info['Medium Topics']} on "
        f"{exam_info['Medium Study Day']}/{exam_info['Medium Study Month']}, "
        f"and the {exam_info['Hardest Topics']} on "
        f"{exam_info['Hard Study Day']}/{exam_info['Hard Study Month']}."
    )

    st.write("---")

confusion_matrix = pd.DataFrame({
    "Revision": [f"{exam_info['Revision Day']}/{exam_info['Revision Month']}" for exam_name, exam_info in st.session_state.exams.items()],
    "Easy Topics Day": [f"{exam_info['Easy Study Day']}/{exam_info['Easy Study Month']}" for exam_name, exam_info in st.session_state.exams.items()],
    "Medium Topics Day": [f"{exam_info['Medium Study Day']}/{exam_info['Medium Study Month']}" for exam_name, exam_info in st.session_state.exams.items()],
    "Hard Topics Day": [f"{exam_info['Hard Study Day']}/{exam_info['Hard Study Month']}" for exam_name, exam_info in st.session_state.exams.items()]
},
    index=[exam_name for exam_name in st.session_state.exams.keys()],

)
st.table(confusion_matrix)

change = st.selectbox("Change Exam", options=list(
    st.session_state.exams.keys()))
for change in st.session_state.exams.keys():
    what_to_change = st.selectbox(
        "What do you want to change?", options=list(st.session_state.exams[change].keys()))
    new_value = st.text_input(f"Enter new value for {what_to_change}")
    if st.button("Update"):
        st.session_state.exams[change][what_to_change] = new_value

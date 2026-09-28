import streamlit as st

st.title("Task Organizer")


if "new_task" not in st.session_state:
    st.session_state.new_task = False

if st.button("New Task"):
    st.session_state.new_task = True


Tasks = {}
if st.session_state.new_task:
    task_name = st.text_input("Enter the task name:")
    Priority = st.selectbox(
        "Is the task important? 1 is Yes, 0 is No", ("1", "0"))
    Urgency = st.selectbox("Is the task urgent? 1 is Yes, 0 is No", ("1", "0"))
    if Priority == "1" and Urgency == "1":
        quadrant = "Quadrant 1: Important and Urgent"
    if Priority == "1" and Urgency == "0":
        quadrant = "Quadrant 2: Important but Not Urgent"
    if Priority == "0" and Urgency == "1":
        quadrant = "Quadrant 3: Not Important but Urgent"
    if Priority == "0" and Urgency == "0":
        quadrant = "Quadrant 4: Not Important and Not Urgent"


if st.button("Save Task"):
    if task_name:
        Tasks[task_name] = {
            "Name": task_name,
            "Priority": Priority,
            "Urgency": Urgency,
            "Quadrant": quadrant
        }
        st.success(f"Task '{task_name}' saved successfully!")
    else:
        st.error("Please enter a task name.")
        st.session_state.new_task = False


st.header("Quadrant 1: Important and Urgent")
for task_name, task_info in Tasks.items():
    if task_info["Quadrant"] == "Quadrant 1: Important and Urgent":
        st.write(task_info["Name"])

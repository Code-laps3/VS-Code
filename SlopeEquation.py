import random
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Physics Practice Generator",
                   page_icon="⚡", layout="centered")

st.title("⚡ Physics Problem Generator")
st.caption("Work-Energy Theorem & Conservation of Energy Practice Problems")

# 1. State Management (persists random values across button clicks)
if "problem_data" not in st.session_state:
    st.session_state.problem_data = None


def generate_valid_problem():
    """Generates random variables ensuring non-negative kinetic energy at B."""
    while True:
        mass = random.randint(10, 20)
        speedA = random.randint(0, 10)
        height = random.randint(2, 12)
        slopelength = random.randint(30, 100)
        friction = round(random.uniform(3, 10), 2)

        # Work-Energy Balance: EmA - (Friction * Distance) = EmB
        EmA = (mass * 9.8 * height) + (0.5 * mass * speedA**2)
        work_friction = friction * slopelength

        if EmA > work_friction:
            speedB = round(((EmA - work_friction) / (0.5 * mass)) ** 0.5, 2)
            return {
                "mass": mass,
                "speedA": speedA,
                "height": height,
                "slopelength": slopelength,
                "friction": friction,
                "speedB": speedB,
            }


# 2. Sidebar Controls
with st.sidebar:
    st.header("Controls")
    target_var = st.selectbox(
        "Variable to Solve For:",
        ["Friction", "Velocity At End", "Slope Length",
            "Velocity at Start", "Height"],
    )

    if st.button("🎲 Generate New Problem", use_container_width=True, type="primary"):
        st.session_state.problem_data = generate_valid_problem()

# Generate initial problem if none exists
if st.session_state.problem_data is None:
    st.session_state.problem_data = generate_valid_problem()

data = st.session_state.problem_data

# 3. Main UI Card
st.subheader("Given Values")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Mass (m)", value=f"{data['mass']} kg")
    if target_var != "Velocity at Start":
        st.metric(label="Initial Speed ($v_A$)", value=f"{data['speedA']} m/s")
    if target_var != "Height":
        st.metric(label="Height (h)", value=f"{data['height']} m")

with col2:
    if target_var != "Slope Length":
        st.metric(label="Slope Length (d)", value=f"{data['slopelength']} m")
    if target_var != "Friction":
        st.metric(label="Friction ($f_k$)", value=f"{data['friction']} N")
    if target_var != "Velocity At End":
        st.metric(label="Final Speed ($v_B$)", value=f"{data['speedB']} m/s")

st.divider()

# Question Display
target_labels = {
    "Friction": ("Friction Force ($f_k$)", f"{data['friction']} N"),
    "Velocity At End": ("Final Velocity ($v_B$)", f"{data['speedB']} m/s"),
    "Slope Length": ("Slope Length ($d$)", f"{data['slopelength']} m"),
    "Velocity at Start": ("Initial Velocity ($v_A$)", f"{data['speedA']} m/s"),
    "Height": ("Initial Height ($h$)", f"{data['height']} m"),
}

target_name, target_value = target_labels[target_var]
st.info(f"**Task:** Calculate the **{target_name}**.")

# Answer Reveal
with st.expander("🔍 Show Answer & Formula"):
    st.success(f"**{target_name}:** `{target_value}`")
    st.latex(
        r"mgh + \frac{1}{2}mv_A^2 - f_k \cdot d = \frac{1}{2}mv_B^2"
    )

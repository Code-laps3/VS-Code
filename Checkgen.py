import random
import streamlit as st

st.set_page_config(page_title="Sequence Analyzer & Generator", page_icon="🔢")

st.title("🔢 Sequence Analyzer & Practice Generator")
st.write(
    "Use this app to analyze your own 4-term sequences with full step-by-step working, or generate random practice problems."
)

# Mode Selection
mode = st.radio(
    "Select Mode:",
    ["Analyze Custom Sequence", "Generate Practice Sequence"],
    horizontal=True,
)

st.divider()

# Helper function to cleanly format numbers (e.g., 2.0 -> 2)


def fmt(n):
    if isinstance(n, (int, float)) and float(n).is_integer():
        return str(int(n))
    return str(round(n, 2))


# MODE 1: Custom Sequence Analyzer (With Step-by-Step Output)
if mode == "Analyze Custom Sequence":
    st.header("🧮 Custom Sequence Analyzer")
    st.write("Enter the first four terms of your sequence below:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        FirstDigit = st.number_input("First Digit", value=2.0, step=1.0)
    with col2:
        SecondDigit = st.number_input("Second Digit", value=4.0, step=1.0)
    with col3:
        ThirdDigit = st.number_input("Third Digit", value=6.0, step=1.0)
    with col4:
        FourthDigit = st.number_input("Fourth Digit", value=8.0, step=1.0)

    if st.button("Analyze Pattern", type="primary"):
        # First Differences
        LinearDif1 = SecondDigit - FirstDigit
        LinearDif2 = ThirdDigit - SecondDigit
        LinearDif3 = FourthDigit - ThirdDigit

        # Check Linear
        isLinear = (LinearDif1 == LinearDif2 == LinearDif3)

        # Second Differences
        SecondDifference1 = LinearDif2 - LinearDif1
        SecondDifference2 = LinearDif3 - LinearDif2

        # Check Quadratic
        if SecondDifference1 == SecondDifference2 and SecondDifference1 != 0:
            a = SecondDifference1 / 2.0
            b = LinearDif1 - (a * 3)
            c = FirstDigit - a - b
            isQuadratic = True
        else:
            isQuadratic = False
            a, b, c = 0, 0, 0

        # Geometric Check
        isGeometric = False
        GeometricDif1, GeometricDif2, GeometricDif3 = 0, 0, 0
        if FirstDigit != 0 and SecondDigit != 0 and ThirdDigit != 0:
            GeometricDif1 = SecondDigit / FirstDigit
            GeometricDif2 = ThirdDigit / SecondDigit
            GeometricDif3 = FourthDigit / ThirdDigit

            if (
                abs(GeometricDif1 - GeometricDif2) < 1e-9
                and abs(GeometricDif2 - GeometricDif3) < 1e-9
            ):
                isGeometric = True

        st.subheader("📋 Working Steps")

        # LINEAR OUTPUT
        if isLinear:
            st.success("The sequence is a **Linear** sequence.")

            steps = (
                f"{fmt(SecondDigit)} - {fmt(FirstDigit)} = {fmt(LinearDif1)}\n"
                f"{fmt(ThirdDigit)} - {fmt(SecondDigit)} = {fmt(LinearDif2)}\n"
                f"{fmt(FourthDigit)} - {fmt(ThirdDigit)} = {fmt(LinearDif3)}\n\n"
                f"{fmt(LinearDif1)} = {fmt(LinearDif2)} = {fmt(LinearDif3)} so the sequence is Linear."
            )
            st.code(steps, language="text")

            st.write("**Formula:**")
            st.latex(f"T_n = {fmt(FirstDigit)} + {fmt(LinearDif1)}(n - 1)")

        # QUADRATIC OUTPUT
        elif isQuadratic and a != 0:
            st.success("The sequence is a **Quadratic** sequence.")

            steps = (
                f"First Differences:\n"
                f"{fmt(SecondDigit)} - {fmt(FirstDigit)} = {fmt(LinearDif1)}\n"
                f"{fmt(ThirdDigit)} - {fmt(SecondDigit)} = {fmt(LinearDif2)}\n"
                f"{fmt(FourthDigit)} - {fmt(ThirdDigit)} = {fmt(LinearDif3)}\n\n"
                f"Second Difference: {fmt(SecondDifference1)}\n\n"
                f"Solving for a, b, c:\n"
                f"2a = {fmt(SecondDifference1)}  =>  a = {fmt(a)}\n"
                f"3a + b = {fmt(LinearDif1)}  =>  b = {fmt(b)}\n"
                f"a + b + c = {fmt(FirstDigit)}  =>  c = {fmt(c)}\n\n"
                f"a = {fmt(a)}, b = {fmt(b)}, c = {fmt(c)}"
            )
            st.code(steps, language="text")

            st.write("**Formula:**")
            st.latex(f"T_n = {fmt(a)}n^2 + {fmt(b)}n + {fmt(c)}")

        # GEOMETRIC OUTPUT
        elif isGeometric:
            st.success("The sequence is a **Geometric** sequence.")

            steps = (
                f"{fmt(SecondDigit)} / {fmt(FirstDigit)} = {fmt(GeometricDif1)}\n"
                f"{fmt(ThirdDigit)} / {fmt(SecondDigit)} = {fmt(GeometricDif2)}\n"
                f"{fmt(FourthDigit)} / {fmt(ThirdDigit)} = {fmt(GeometricDif3)}\n\n"
                f"{fmt(GeometricDif1)} = {fmt(GeometricDif2)} = {fmt(GeometricDif3)} so the sequence is Geometric."
            )
            st.code(steps, language="text")

            st.write("**Formula:**")
            st.latex(
                f"T_n = {fmt(FirstDigit)} \\cdot ({fmt(GeometricDif1)})^{{n-1}}")

        else:
            st.error(
                "The entered digits do not form a standard Linear, Quadratic, or Geometric sequence."
            )

# MODE 2: Practice Generator
else:
    st.header("🎲 Practice Sequence Generator")

    def generate_new_sequence():
        RSequence = random.randint(1, 3)

        if RSequence == 1:  # Linear
            Rada = random.randint(-15, 15)
            Radd = random.randint(-10, 10)
            terms = [Rada + Radd * i for i in range(4)]
            st.session_state.current_seq = {
                "type": "Linear",
                "terms": terms,
                "formula": f"T_n = {Rada} + {Radd}(n - 1)",
            }

        elif RSequence == 2:  # Quadratic
            Rada = random.randint(-15, 15)
            Radb = random.randint(-10, 10)
            Radc = random.randint(-20, 20)
            terms = [
                Rada * (n**2) + Radb * n + Radc for n in range(1, 5)
            ]
            st.session_state.current_seq = {
                "type": "Quadratic",
                "terms": terms,
                "formula": f"T_n = {Rada}n^2 + {Radb}n + {Radc}",
            }

        elif RSequence == 3:  # Geometric
            Rada = random.randint(-15, 15)
            Radr = random.randint(-5, 5)
            if Radr == 0:
                Radr = 2
            terms = [Rada * (Radr**i) for i in range(4)]
            st.session_state.current_seq = {
                "type": "Geometric",
                "terms": terms,
                "formula": f"T_n = {Rada} \\cdot ({Radr})^{{n-1}}",
            }

    if "current_seq" not in st.session_state or st.button(
        "🔄 Generate New Sequence"
    ):
        generate_new_sequence()

    seq_data = st.session_state.current_seq
    terms_str = " ; ".join(map(str, seq_data["terms"]))

    st.subheader("Determine the formula of this sequence:")
    st.info(f"**Sequence:** {terms_str}")

    with st.expander("👁️ Check Answer"):
        st.markdown(f"**Type:** {seq_data['type']}")
        st.latex(seq_data["formula"])

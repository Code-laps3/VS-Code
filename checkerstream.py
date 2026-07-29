import streamlit as st

st.title("Sequence Pattern Identifier")

st.write("Enter the first four terms of a sequence.")

# User input
FirstDigit = st.number_input("First term", step=1, format="%d")
SecondDigit = st.number_input("Second term", step=1, format="%d")
ThirdDigit = st.number_input("Third term", step=1, format="%d")
FourthDigit = st.number_input("Fourth term", step=1, format="%d")

if st.button("Analyse Sequence"):

    # Calculate first differences
    LinearDif1 = SecondDigit - FirstDigit
    LinearDif2 = ThirdDigit - SecondDigit
    LinearDif3 = FourthDigit - ThirdDigit

    # Calculate second differences
    SecondDifference1 = LinearDif2 - LinearDif1
    SecondDifference2 = LinearDif3 - LinearDif2

    # Check sequence types
    isLinear = LinearDif1 == LinearDif2 == LinearDif3

    isQuadratic = SecondDifference1 == SecondDifference2 and LinearDif1 != LinearDif2

    # Avoid division by zero
    isGeometric = False
    if FirstDigit != 0 and SecondDigit != 0 and ThirdDigit != 0:
        GeometricDif1 = SecondDigit / FirstDigit
        GeometricDif2 = ThirdDigit / SecondDigit
        GeometricDif3 = FourthDigit / ThirdDigit

        isGeometric = (
            GeometricDif1 == GeometricDif2 == GeometricDif3
        )

    st.subheader("Results")

    if isLinear:
        st.success("The sequence is linear.")
        st.write(
            f"**Formula:** Tₙ = {int(FirstDigit)} + {int(LinearDif1)}(n − 1)")

    if isQuadratic:
        a = SecondDifference1 / 2
        b = LinearDif1 - (3 * a)
        c = FirstDigit - a - b

        st.success("The sequence is quadratic.")
        st.write(
            f"**Formula:** Tₙ = {a:.0f}n² + {b:.0f}n + {c:.0f}"
        )

    if isGeometric:
        st.success("The sequence is geometric.")
        st.write(
            f"**Formula:** Tₙ = {int(FirstDigit)} × ({GeometricDif1})^(n − 1)"
        )

    if not (isLinear or isQuadratic or isGeometric):
        st.warning(
            "This sequence is not linear, quadratic, or geometric based on the first four terms."
        )

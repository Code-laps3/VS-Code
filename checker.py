import streamlit as st

st.title("Sequence Checker")

FirstDigit = st.text_input("What is the first digit of the pattern?")
SecondDigit = st.text_input("What is the second digit of the pattern?")
ThirdDigit = st.text_input("What is the third digit of the pattern?")
FourthDigit = st.text_input("What is the fourth digit of the pattern?")

if FourthDigit is not None:

    FirstDifference1 = int(SecondDigit) - int(FirstDigit)
    FirstDifference2 = int(ThirdDigit) - int(SecondDigit)
    FirstDifference3 = int(FourthDigit) - int(ThirdDigit)


if SecondDifference1 == SecondDifference2 and FirstDifference1 != FirstDifference2 and FirstDifference2 != FirstDifference3:
    print("The sequence is a quadratic sequence.")
    isQuadratic = True
else:
    isQuadratic = False


LinearDif1 = int(SecondDigit) - int(FirstDigit)
LinearDif2 = int(ThirdDigit) - int(SecondDigit)
LinearDif3 = int(FourthDigit) - int(ThirdDigit)

if LinearDif1 == LinearDif2 and LinearDif2 == LinearDif3:
    print("The sequence is a linear sequence.")
    isLinear = True
else:
    isLinear = False


GeometricDif1 = int(SecondDigit) / int(FirstDigit)
GeometricDif2 = int(ThirdDigit) / int(SecondDigit)
GeometricDif3 = int(FourthDigit) / int(ThirdDigit)

if GeometricDif1 == GeometricDif2 and GeometricDif2 == GeometricDif3:
    print("The sequence is a geometric sequence.")
    isGeometric = True
else:
    isGeometric = False

if isLinear is True:
    print(f"Tn={FirstDigit} + {LinearDif1}(n-1)")

if isQuadratic is True:
    a = int(SecondDifference1) / 2
    b = int(FirstDifference1) - (a*3)
    c = int(FirstDigit) - a - b
    print(f"Tn= {int(a)}n^2 + {int(b)}n + {int(c)}")


if isGeometric is True:
    print(f"Tn={FirstDigit} * {GeometricDif1}^(n-1)")

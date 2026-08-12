
import random
RandSeq = input("Do you want a random sequence? Type yes or no: ")
if RandSeq == "no":
    FirstDigit = input("What is the first digit of the pattern?")
    SecondDigit = input("What is the second digit of the pattern?")
    ThirdDigit = input("What is the third digit of the pattern?")
    FourthDigit = input("What is the fourth digit of the pattern?")
    RSequence = 0

if RandSeq == "yes":
    FirstDigit = 2
    SecondDigit = 4
    ThirdDigit = 6
    FourthDigit = 8

    RSequence = random.randint(1, 3)

    if RSequence == 1:

        Rada = random.randint(-15, 15)
        Radd = random.randint(-10, 10)

        RadFirstTerm = Rada + Radd*(0)
        RadSecondTerm = Rada + Radd*(1)
        RadThirdTerm = Rada + Radd*(2)
        RadFourthTerm = Rada + Radd*(3)

        print(
            f"Determine the formula of this sequence: {RadFirstTerm} ; {RadSecondTerm} ; {RadThirdTerm} ; {RadFourthTerm}")
        Check = input("Check answer, Y/N: ")
        if Check == "Y":
            print(
                f" The sequence is linear with the formula: {Rada} + {Radd} (n-1)")

    if RSequence == 2:

        Rada = random.randint(-15, 15)
        Radb = random.randint(-10, 10)
        Radc = random.randint(-20, 20)

        RadFirstTerm = Rada * 1**2 + Radb * 1 + Radc
        RadSecondTerm = Rada * 2**2 + Radb * 2 + Radc
        RadThirdTerm = Rada * 3**2 + Radb * 3 + Radc
        RadFourthTerm = Rada * 4**2 + Radb * 4 + Radc

        print(
            f"Determine the formula of this sequence: {RadFirstTerm} ; {RadSecondTerm} ; {RadThirdTerm} ; {RadFourthTerm}")
        Check = input("Check answer, Y/N: ")
        if Check == "Y":
            print(
                f"The sequence is quadratic with the formula: {Rada}n^2 + {Radb}n + {Radc}")

    if RSequence == 3:
        Rada = random.randint(-15, 15)
        Radr = random.randint(-5, 5)

        RadFirstTerm = Rada * Radr**0
        RadSecondTerm = Rada * Radr**1
        RadThirdTerm = Rada * Radr**2
        RadFourthTerm = Rada * Radr**3

        print(
            f"Determine the formula of this sequence: {RadFirstTerm} ; {RadSecondTerm} ; {RadThirdTerm} ; {RadFourthTerm}")
        Check = input("Check answer, Y/N: ")
    if Check == "Y":
        print(
            f"The sequence is geometric with the formula: {Rada} * {Radr}^(n-1)")


FirstDifference1 = int(SecondDigit) - int(FirstDigit)
FirstDifference2 = int(ThirdDigit) - int(SecondDigit)
FirstDifference3 = int(FourthDigit) - int(ThirdDigit)

SecondDifference1 = FirstDifference2 - FirstDifference1
SecondDifference2 = FirstDifference3 - FirstDifference2

if SecondDifference1 == SecondDifference2:
    a = int(SecondDifference1) / 2
    b = int(FirstDifference1) - (a*3)
    c = int(FirstDigit) - a - b
    isQuadratic = True
else:
    isQuadratic = False


LinearDif1 = int(SecondDigit) - int(FirstDigit)
LinearDif2 = int(ThirdDigit) - int(SecondDigit)
LinearDif3 = int(FourthDigit) - int(ThirdDigit)

if LinearDif1 == LinearDif2 and LinearDif2 == LinearDif3:
    isLinear = True
else:
    isLinear = False

if FirstDigit != "0" and SecondDigit != "0" and ThirdDigit != "0" and FourthDigit != "0":
    GeometricDif1 = int(SecondDigit) / int(FirstDigit)
    GeometricDif2 = int(ThirdDigit) / int(SecondDigit)
    GeometricDif3 = int(FourthDigit) / int(ThirdDigit)


if GeometricDif1 == GeometricDif2 and GeometricDif2 == GeometricDif3:
    isGeometric = True
else:
    isGeometric = False

if isLinear is True and RandSeq == "no":
    print("The sequence is a linear sequence.")
    print(f"Tn={FirstDigit} + {LinearDif1}(n-1)")

if isQuadratic is True and a != 0 and RandSeq == "no":
    print("The sequence is a quadratic sequence.")
    print(f"Tn= {int(a)}n^2 + {int(b)}n + {int(c)}")


if isGeometric is True and RandSeq == "no":
    print("The sequence is a geometric sequence.")
    print(f"Tn={FirstDigit} * {GeometricDif1}^(n-1)")

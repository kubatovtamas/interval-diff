from interval import *
from differential import *

def main():
    # I. Intervallum aritmetika
    print("[1, 4] + [-1, 2] / [-5, -1] - [-2, 1]:\n")

    i1 = Interval([1, 4])
    i2 = Interval([-1, 2])
    i3 = Interval([-5, -1])
    i4 = Interval([-2, 1])

    i1 + i2 / i3 - i4


    # II. Automatikus differenciálás
    print("log(x) * (x^2 + 2x + 4), x = 3")

    x = Differential([3, 1])
    c = Differential([4, 0])

    x.log() * (x**2 + 2*x +c)  # [20.873, 15.122]


    print("(x^3 - x^2 + 5) * (x + 4), x = 2")

    x = Differential([2, 1])
    c1 = Differential([5, 0])
    c2 = Differential([4, 0])
    (x**3 - x**2 + c1) * (x + c2)  ## [54, 57]

    print("sin(x^2) * (y^3+2), x = 1, y = 2")
    x = Differential([1, 1])
    xd = Differential([1, 0])
    y = Differential([2, 1])
    yd = Differential([2, 0])
    c = Differential([2, 0])

    print("x szerinti deriváltja:")
    (x ** 2).sin() * (yd ** 3 + c)  # [8.414, 10.806]

    print("y szerinti deriváltja:")
    (xd ** 2).sin() * (y ** 3 + c)  # [8.415,10.1]

if __name__ == '__main__':
    main()
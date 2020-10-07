#TODO implement int.calc operators
#TODO make differential class
#TODO implement diff.cald operators
#TODO make IO script


from __future__ import annotations
from typing import  Optional, TypeVar
import sympy as sp
import unittest
import math


number = TypeVar('number', int, float)


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'










# Interval arithmetic

class Interval:
    def __init__(self, interval: list):
        self.interval = interval

    @property
    def low(self):
        return self.interval[0]

    @low.setter
    def low(self, value):
        self.interval[0] = value

    @property
    def high(self):
        return self.interval[1]

    @high.setter
    def high(self, value):
        self.interval[1] = value

    def __str__(self):
        return f"[{self.low}, {self.high}]"

    def __eq__(self, other: Interval):
        if isinstance(other, Interval):
            return math.isclose(self.low, other.low, rel_tol=0.0001) and math.isclose(self.high, other.high, rel_tol=0.0001)

    def __add__(self: Interval, other: Interval) -> Interval:
        if isinstance(other, Interval):
            left = self.low + other.low
            right = self.high + other.high

            return Interval([left, right])
        raise TypeError

    def __sub__(self: Interval, other: Interval) -> Interval:
        if isinstance(other, Interval):
            left = self.low - other.high
            right = self.high - other.low

            return Interval([left, right])
        raise TypeError

    def __mul__(self: Interval, other: Interval) -> Interval:
        if isinstance(other, Interval):
            left = min(self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high)
            right = max(self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high)

            return Interval([left, right])
        raise TypeError

    def __truediv__(self: Interval, other: Interval) -> Interval:
        if isinstance(other, Interval):
            if other.low <= 0 <= other.high:
                raise ZeroDivisionError

            right = Interval([1 / other.high, 1 / other.low])
            return self * right
        raise TypeError

    def __pow__(self: Interval, power: int, modulo=None) -> Interval:
        if self.low <= 0 <= self.high:
            return Interval([0, (self.high ** power)])
        val1 = self.low ** power
        val2 = self.high ** power
        return Interval([min(val1, val2), max(val1, val2)])

    def __rxor__(self: Interval, other: number):
        left = other ** self.low
        right = other ** self.high
        return Interval([left, right])

    def log(self, log: number = math.e) -> Interval:
        if self.low > 0 and self.high > 0 and log > 1:
            res = Interval([math.log(self.low, log), math.log(self.high, log)])
            return res
        raise ValueError


def add_interval(F: list, G: list, do_print: bool = True) -> list:
    """
        [a, b] + [c, d] = [a + c, b + d]

        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: interval sum of F and G as list of len 2
    """
    left = F[0] + G[0]
    right = F[1] + G[1]
    if do_print:
        print(f"{F} + {G} = [{F[0]} + {G[0]}, {F[1]} + {G[1]}] =  {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}\n")
    return [left, right]


def sub_interval(F: list, G: list, do_print: bool = True) -> list:
    """
        [a, b] - [c, d] = [a - d, b - c]

        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: interval difference of F and G as list of len 2
    """
    left = F[0] - G[1]
    right = F[1] - G[0]
    if do_print:
        print(f"{F} - {G} = [{F[0]} - {G[1]}, {F[1]} - {G[0]}] = {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}\n")
    return [left, right]


def mul_interval(F: list, G: list, do_print: bool = True) -> list:
    """
        [a, b] * [c, d] = [min(ac, ad, bc, bd), max(ac, ad, bc, bd)]

        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: interval product of F and G as list of len 2
    """
    left = min(F[0] * G[0], F[0] * G[1], F[1] * G[0], F[1] * G[1])
    right = max(F[0] * G[0], F[0] * G[1], F[1] * G[0], F[1] * G[1])
    if do_print:
        print(
            f"[{F[0]:.3f}, {F[1]:.3f}] * [{G[0]:.3f}, {G[1]:.3f}] ="
            f"[min({F[0]:.3f} * {G[0]:.3f}, {F[0]:.3f} * {G[1]:.3f}, {F[1]:.3f} * {G[0]:.3f}, {F[1]:.3f} * {G[1]:.3f}),"
            f" max({F[0]:.3f} * {G[0]:.3f}, {F[0]:.3f} * {G[1]:.3f}, {F[1]:.3f} * {G[0]:.3f}, {F[1]:.3f} * {G[1]:.3f})"
            f" = {Color.RED} [{left:.3f}, {right:.3f}] {Color.END}\n")
    return [left, right]


def div_interval(F: list, G: list, do_print: bool = True) -> Optional[list]:
    """
        [a, b] / [c, d] = [a, b] * [1/d, 1/c], if 0 not in [c, d]

        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: interval quotient of F and G as list of len 2
    """
    if G[0] <= 0 <= G[1]:
        if do_print:
            print(f"{Color.RED}A nevező intervallum eleme a nulla, így a művelet nem elvégezhető{Color.END}\n")
        return None
    if do_print:
        print(f"{F} / {G} = {F} * [1 / {G[1]:.3f}, 1 / {G[0]:.3f}] = ")
    return mul_interval(F, [1 / G[1], 1 / G[0]], do_print)


def pow_interval(F: list, k: int, do_print: bool = True) -> list:
    """
        [a, b] ^ k = {
            [0, b^k] : if k is even, and 0 is in interval [a, b]

            [a^k, b^k] : otherwise
        }

        :param F: the base interval as list of len 2
        :param k: the power to which F is raised
        :param do_print: print to stdout if true
        :return: interval F raised to power k as list of len 2
    """
    if k % 2 == 0:
        # paros kitevo, 0 eleme az intervallumnak
        if F[0] <= 0 <= F[1]:
            if do_print:
                print(f"{F}^{k} = {Color.RED}[0,{(F[1] ** k):.3f}]{Color.END}")
            return [0, (F[1] ** k)]
    if do_print:
        print(f"{F}^{k} = {Color.RED}[{F[0] ** k:.3f}, {F[1] ** k:.3f}]{Color.END}")
    return [(F[0] ** k), (F[1] ** k)]


def log_interval(F: list, do_print: bool = True) -> list:
    #TODO THIS IS FAKE, DONT COPY PASTE
    """
    log([a, b]) = [log(a), log(b)]

    :param F: the input interval as list of len 2
    :param do_print: print to stdout if true
    :return: logarithm of interval F as list of len 2
    """
    left = math.e ** F[0]
    right = math.e ** F[1]
    if do_print:
        print(f"num^{F} = {Color.RED}[{math.e}^{F[0]}, {math.e}{F[1]}]{Color.END}")
    return [left, right]


def exp_interval(F: list, num: number = math.e, do_print: bool = True) -> list:
    """
    x^[a, b] = [x^a, x^b]

    :param F: the power interval as list of len 2
    :param num: the number to be raised to interval F
    :param do_print: print to stdout if true
    :return: interval F raised to power k as list of len 2
    """
    left = num ** F[0]
    right = num ** F[1]
    if do_print:
        print(f"num^{F} = {Color.RED}[{num}^{F[0]}, {num}{F[1]}]{Color.END}")
    return [left, right]


def sin_interval(F: list, do_print: bool = True) -> list:
    """
    sin[a, b] = {
        [-1, ...], if 3pi/2 + 2k * pi in [a, b],

        [..., 1] if pi/2 + 2k * pi in [a, b],

        [min(sin(a), sin(b)), max(sin(a), sin(b))] otherwise
    }

    :param F: interval as list of len 2
    :param do_print: print to stdout if true
    :return: value of sin in interval F as list of len 2
    """
    left = min(math.sin(F[0]), math.sin(F[1]))
    right = max(math.sin(F[0]), math.sin(F[1]))

    a = F[0]
    b = F[1]

    # shift a between [0, 2pi]
    while (2 * math.pi) <= a:
        a = a - (2 * math.pi)
        b = b - (2 * math.pi)

    while a < 0:
        a = a + (2 * math.pi)
        b = b + (2 * math.pi)

    # shorten [a, b] to 2*pi length
    if (b - a) >= 2 * math.pi:
        b = a + (2 * math.pi)

    # critical points: 3pi / 2, 7pi / 2, 11pi / 2 -> -1
    if (a <= ((3 * math.pi) / 2) <= b) or (a <= (7 * math.pi) / 2 <= b) or (a <= (11 * math.pi) / 2 <= b):
        left = -1

    # critical points: pi / 2, 5pi / 2, 9pi / 2 -> 1
    if (a <= (math.pi / 2) <= b) or (a <= (5 * math.pi / 2) <= b) or (a <= (9 * math.pi / 2) <= b):
        right = 1

    if do_print:
        print(f"sin({F}) = [min(sin(a), sin(b)) és -1 ha 3pi/2 + 2k * pi eleme [a, b]-nek,"
              f" max(sin(a), sin(b)) és 1 ha pi/2 + 2k * pi eleme [a, b]-nek"
              f" => {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]


def cos_interval(F: list, do_print: bool = True) -> list:
    """
        cos[a, b] = {
            [-1, ...], if -pi + 2k * pi in [a, b],

            [..., 1] if 0 + 2k * pi in [a, b],

            [min(cos(a), cos(b)), max(cos(a), cos(b))] otherwise
        }

        :param F: interval as list of len 2
        :param do_print: print to stdout if true
        :return: value of cos in interval F as list of len 2
    """

    left = min(math.cos(F[0]), math.cos(F[1]))
    right = max(math.cos(F[0]), math.cos(F[1]))

    a = F[0]
    b = F[1]

    # shift a between [-pi, pi]
    while math.pi <= a:
        a = a - (2 * math.pi)
        b = b - (2 * math.pi)

    while a < (-1 * math.pi):
        a = a + (2 * math.pi)
        b = b + (2 * math.pi)

    # shorten [a, b] to 2*pi length
    if (b - a) >= 2 * math.pi:
        b = a + (2 * math.pi)

    # critical points: -pi, pi, 3pi
    if (a <= (-1 * math.pi) <= b) or (a <= math.pi <= b) or (a <= 3 * math.pi <= b):
        left = -1

    # critical points: 0, 2pi, 4pi
    if (a <= 0 <= b) or (a <= (2 * math.pi) <= b) or (a <= (4 * math.pi) <= b):
        right = 1

    if do_print:
        print(f"cos({F}) = [min(cos(a), cos(b)) és -1 ha pi + 2k * pi eleme [a, b]-nek,"
              f" max(cos(a), cos(b)) és 1 ha 0 + 2k * pi eleme [a, b]-nek"
              f" => {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]

# Differential arithmetic
# Power rule: (x^n)' = n * x^(n-1)
# Product rule: (f * g)' = (f * g') + (f' * g)
# Quotient rule: (f / g)' = ((f' * g) - (f * g')) / g^2
# Chain rule: (f(g(x)))' = f'(g(x)) * g'(x)
# Addition rule: (f + g)' = f' + g'


def add_diff(F: list, G: list, do_print: bool = True) -> list:
    """
        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: differential interval sum of F and G as list of len 2
    """
    left = F[0] + G[0]
    right = F[1] + G[1]
    if do_print:
        print(f"{F} + {G} = {Color.RED}{[left, right]}{Color.END}")
    return [left, right]


def sub_diff(F: list, G: list, do_print: bool = True) -> list:
    """
        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: differential interval difference of F and G as list of len 2
    """
    left = F[0] - G[0]
    right = F[1] - G[1]
    if do_print:
        print(f"{F} - {G} = {Color.RED}{[left, right]}{Color.END}")
    return [left, right]


def mul_diff(F: list, G: list, do_print: bool = True) -> list:
    """
        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: differential interval product of F and G as list of len 2
    """
    left = F[0] * G[0]
    right = F[0] * G[1] + F[1] * G[0]
    if do_print:
        print(f"[{F[0]:.3f},{F[1]:.3f}] * [{G[0]:.3f},{G[1]:.3f}] = {Color.RED}{[left, right]}{Color.END}")
    return [left, right]


def div_diff(F: list, G: list, do_print: bool = True) -> list:
    """
        :param F: interval_1 as list of len 2
        :param G: interval_2 as list of len 2
        :param do_print: print to stdout if true
        :return: differential interval quotient of F and G as list of len 2
    """
    left = F[0] / G[0]
    right = (F[1] * G[0] - F[0] * G[1]) / G[0] ** 2
    if do_print:
        print(f"{F} / {G} = {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]


def pow_diff(F: list, k: int, do_print: bool = True) -> list:
    """
        :param F: the base interval as list of len 2
        :param k: the power to which F is raised
        :param do_print: print to stdout if true
        :return: differential interval F raised to power k as list of len 2
    """
    left = F[0] ** k
    right = k * F[0] ** (k - 1) * F[1]
    if do_print:
        print(f"{F}^{k} = {Color.RED}{[left, right]}{Color.END}")
    return [left, right]


def log_diff(F: list, do_print: bool = True) -> list:
    """
        log([a,b]) = [log(a), b / a]

        :param F: interval as list of len 2
        :param do_print: print to stdout if true
        :return: [log(a), log(a)'] as list of len 2
    """

    left = math.log(F[0], math.e)
    right = F[1] / F[0]

    if do_print:
        print(f"log({F}) = {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]


def sin_diff(F: list, do_print: bool = True) -> list:
    """
        sin([a,b]) = [sin(a), cos(a) * b]

        :param F: interval as list of len 2
        :param do_print: print to stdout if true
        :return: [sin(a), sin(a)'] as list of len 2
    """

    left = math.sin(F[0])
    right = math.cos(F[0]) * F[1]

    if do_print:
        print(f"sin({F}) = {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]


def cos_diff(F: list, do_print: bool = True) -> list:
    """
        cos([a,b]) = [cos(a), -1 * sin(a) * b]

        :param F: interval as list of len 2
        :param do_print: print to stdout if true
        :return: [cos(a), cos(a)'] as list of len 2
    """

    left = math.cos(F[0])
    right = -1 * math.sin(F[0]) * F[1]

    if do_print:
        print(f"cos({F}) = {Color.RED}[{left:.3f}, {right:.3f}]{Color.END}")
    return [left, right]


# x  -> (x,1)
# c  -> (c,0)
def auto_diff(expr: str, evalAt: number, *consts: number) -> None:
    """
        Evaluate auto_diff first, and use differential arithmetic functions for intermediate results

        Multiple variable differential:

        (x,y)' by x -> (x, 1), y -> (y, 0)

        (x,y)' by y -> (y, 1), x -> (x, 0)

        :param expr: The expression to be evaluated                             eg. "x^2 + 3"
        :param evalAt: The value of x for the expression to be evaluated at     eg. 4
        :param consts: The constants                                            eg. 3
    """
    print(f"\n---------- f(x) = {expr}, az x = {evalAt} helyen: ----------\n")

    variable_pair_form = f"({evalAt}, 1)"
    expr_str = str(expr)
    for i in range(len(consts)):
        constant_pair_form = f"({consts[i]},0)"
        expr_str = expr_str.replace(str(consts[i]), constant_pair_form)
    print(f"f(x) = {expr_str}")
    print(f"f({evalAt}) = {expr_str.replace('x', variable_pair_form)}")

    print("\n>> Use mul_diff(F, G) / add_diff(F, G) / sub_diff(F, G) / "
          "div_diff(F, G) / pow_diff(F, k) for intermediate results <<\n")

    x = sp.Symbol('x')
    f = sp.lambdify(x, expr)
    f_prime = sp.diff(expr, x)
    f_prime = sp.lambdify(x, f_prime)

    print(f"= {Color.RED}[{float(f(evalAt)):.3f}, {float(f_prime(evalAt)):.3f}]{Color.END}")


# Examples for interval arithmetic:
# add_interval([0, 1], [2, 3])
# sub_interval([2, 3], [0, 1])
# mul_interval([-2, 3], [-1, 4])
# div_interval([8, 12], [6, 5])
# pow_interval([-1, 5], 2)

# Examples for differential arithmetic:
# mul_diff([3, 1], [3, 1])
# add_diff([16, 8], [3, 0])
# sub_diff([16, 8], [-3, 0])
# div_diff([6, 1], [3, 0])
# pow_diff([4, 1], 2)

# Examples for auto_diff:
# (x^2+3)^2, x = 2, constants = 3
# auto_diff("(x^2+3)^2", 2, 3)
# tmp = pow_diff([2, 1], 2)
# tmp2 = add_diff(tmp, [3, 0])
# res = pow_diff(tmp2, 2)

# (x+4) / 3, x = 2, constants = 4, 3
# auto_diff("(x+4)/3", 2, 4, 3)
# tmp = add_diff([2, 1], [4, 0])
# tmp2 = div_diff(tmp, [3, 0])

# (1/x), x = 1, constants = 1
# auto_diff("1/x", 1, 1)
# tmp = div_diff([1, 0], [1, 1])


class IntervalClassTestCase(unittest.TestCase):
    def setUp(self):
        t7 = Interval([1, 2])
        t8 = Interval([-3, 4])

    def test_interval_init(self):
        t1 = Interval([1, 5])
        self.assertIsInstance(t1, Interval)
        self.assertEqual(t1.low, t1.interval[0])
        self.assertEqual(t1.high, t1.interval[1])
        self.assertEqual(t1.low, 1)
        self.assertEqual(t1.high, 5)

    def test_interval_str(self):
        t1 = Interval([1, 5])
        t3 = Interval([1.0001, 5])
        self.assertEqual(str(t1), "[1, 5]")
        self.assertEqual(str(t3), "[1.0001, 5]")

    def test_interval_eq(self):
        t1 = Interval([1, 5])
        t2 = Interval([1, 5])
        t3 = Interval([1.0001, 5])
        t4 = Interval([1.0002, 5])
        t5 = Interval([0, 1])
        t6 = Interval([2, 3])
        self.assertTrue(t1 == t2)
        self.assertTrue(t1 == t3)
        self.assertFalse(t1 == t4)


    def test_interval_add(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue((t1 + t2) == Interval([2, 4]))
        self.assertTrue((t3 + t4) == Interval([-2, 6]))

        self.assertTrue((t3 + t4) == (t4 + t3))
        self.assertTrue((t3 + t4) == (t4 + t3))

        t5 = (t3 + t4)
        self.assertTrue(t5 == (t4 + t3))
        self.assertTrue(t5 + t1 == (t4 + t3) + t1)

        self.assertTrue(t1 + t2 + t3 == Interval([3, 6]))


    def test_interval_sub(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue(t1 - t2 == Interval([-3, -1]))
        self.assertTrue(t2 - t1 == Interval([1, 3]))
        self.assertTrue(t3 - t4 == Interval([-3, 5]))


    def test_interval_mul(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue(t1 * t2 == Interval([0, 3]))
        self.assertTrue(t3 * t4 == Interval([-6, 8]))


    def test_interval_div(self):
        t1 = Interval([1, 2])
        t2 = Interval([-3, 4])

        with self.assertRaises(ZeroDivisionError):
            t3 = t1 / t2
        self.assertTrue(t1 / t1 == Interval([0.5, 2]))


    def test_interval_pow(self):
        t1 = Interval([-1, 2])
        t2 = Interval([1, 2])
        t3 = Interval([-2, -1])
        t4 = Interval([-3, -2])

        self.assertTrue(t1 ** 3 == Interval([0, 8]))
        self.assertTrue(t1 ** 2 == Interval([0, 4]))

        self.assertTrue(t2 ** 2 == Interval([1, 4]))
        self.assertTrue(t2 ** 0 == Interval([1, 1]))
        self.assertTrue(t2 ** 1 == t2)

        self.assertTrue(t2 ** -1 == Interval([0.5, 1]))
        self.assertTrue(t2 ** -2 == Interval([0.25, 1]))
        self.assertTrue(t2 ** -3 == Interval([1/8, 1]))


        self.assertTrue(t3 ** -1 == Interval([-1, -1/2]))
        self.assertTrue(t3 ** -3 == Interval([-1, -1/8]))
        self.assertTrue(t3 ** -4 == Interval([1/16, 1]))

        self.assertTrue(t4 ** -3 == Interval([-1/8, -1/27]))
        self.assertTrue(t4 ** 0 == Interval([1, 1]))


    def test_interval_exp(self):
        t1 = Interval([1, 2])
        t2 = Interval([-2, 2])
        t3 = Interval([-6, 8])

        self.assertTrue(math.e ^ t1 == Interval([math.e, math.e ** 2]))
        self.assertTrue(2 ^ t2 == Interval([2 ** -2, 2 ** 2]))
        self.assertTrue(math.pi ^ t3 == Interval([math.pi ** -6, math.pi ** 8]))



    def test_interval_log(self):
        t1 = Interval([-1, 2])
        t2 = Interval([0, 2])
        t3 = Interval([2, 5])
        t4 = Interval([1, 3])

        with self.assertRaises(ValueError):
            Interval.log(t1)
            Interval.log(t2)
            Interval.log(t3, 0)
            Interval.log(t3, 0.5)

        self.assertEqual(Interval.log(t3), Interval([math.log(2), math.log(5)]))
        self.assertEqual(Interval.log(t4), Interval([math.log(1), math.log(3)]))



class IntervalArithmeticTestCase(unittest.TestCase):
    def test_add_interval(self):
        self.assertEqual(add_interval([0, 1], [2, 3], False), [2, 4])
        self.assertEqual(add_interval([1, 2], [-3, 4], False), [-2, 6])

    def test_sub_interval(self):
        self.assertEqual(sub_interval([0, 1], [2, 3], False), [-3, -1])
        self.assertEqual(sub_interval([2, 3], [0, 1], False), [1, 3])
        self.assertEqual(sub_interval([1, 2], [-3, 4], False), [-3, 5])

    def test_mul_interval(self):
        self.assertEqual(mul_interval([0, 1], [2, 3], False), [0, 3])
        self.assertEqual(mul_interval([1, 2], [-3, 4], False), [-6, 8])

    def test_div_interval(self):
        self.assertEqual(div_interval([1, 2], [-3, 4], False), None)
        self.assertEqual(div_interval([1, 2], [1, 2], False), [0.5, 2])

    def test_pow_interval(self):
        self.assertEqual(pow_interval([-1, 2], 2, False), [0, 4])

    def test_exp_interval(self):
        self.assertEqual(exp_interval([1, 2], math.e, False), [math.e, math.e ** 2])
        self.assertEqual(exp_interval([-2, 2], 2, False), [2 ** -2, 2 ** 2])
        self.assertEqual(exp_interval([-6, 8], math.pi, False), [math.pi ** -6, math.pi ** 8])

    def test_sin_interval(self):
        self.assertEqual(sin_interval([0, math.pi], False), [0, 1])
        self.assertEqual(sin_interval([-4 * math.pi, 5 * math.pi / 2], False), [-1, 1])
        self.assertEqual(sin_interval([math.pi, 4*math.pi], False), [-1, 1])
        self.assertAlmostEqual(sin_interval([0, 4], False)[0], -0.757, 3)
        self.assertEqual(sin_interval([0, 4], False)[1], 1)
        self.assertEqual(sin_interval([0, 2*math.pi], False)[1], 1)
        self.assertEqual(sin_interval([-1 * math.pi / 2, 0], False), [-1, 0])
        self.assertEqual(sin_interval([-1 * math.pi / 2, 1], False), [-1, math.sin(1)])

    def test_cos_interval(self):
        self.assertEqual(cos_interval([0, 4], False), [-1, 1])
        self.assertEqual(cos_interval([math.pi, 4 * math.pi], False), [-1, 1])
        self.assertEqual(cos_interval([0, 13], False), [-1, 1])
        self.assertEqual(cos_interval([0, 7], False), [-1, 1])
        self.assertAlmostEqual(cos_interval([-1 * math.pi / 2, 0], False)[0], 0, 3)
        self.assertAlmostEqual(cos_interval([-1 * math.pi, -1 * math.pi / 2], False)[1], 0, 3)

    def test_expression(self):
        self.assertEqual(
            sub_interval(
                add_interval(
                    div_interval([2, 4], [1, 2], False),
                    mul_interval([4, 5], [2, 3], False), False
                ), [-5, 6], False
            ), [3, 24])

def main():
    pass
    # Gyak 3:
    # I. Intervallum aritmetika

    # Team1 [1;4]+[-1;2]/[-5;-1]-[-2;1] = [1;4]+[-1;2]*[-1;-1/5]-[-2;1] = [1;4]+[-2;1] -[-2;1] = [-1;5] -[-2;1] = [-2;7]
    # sub_interval(add_interval([1, 4], div_interval([-1, 2], [-5, -1])), [-2, 1])

    # Team2 X=[-1;2] intervallumon a x^2+3x függvényt, minél szűkebb megoldást
    # add_interval(pow_interval([-1, 2], 2), [-3, 6])  # f1(x) = x^2+3x
    # add_interval(mul_interval([-1, 2], [-1, 2]), [-3, 6])  # f2(x) = x * x + 3x
    # mul_interval([-1, 2], add_interval([-1, 2], [3*-1, 3*2]))  # f3(x) = x*(x+3x)
    # f4(x) = (x+3/2)^2-9/4

    # II. Automatikus differenciálás
    # Team 3. a log(x)(x^2+2x+4) -t az x = 3 helyen
    # auto_diff("log(x) * (x^2 + 2*x + 4)", 3, 4)
    # mul_diff(log_diff([3, 1]), add_diff(add_diff(pow_diff([3, 1], 2), [2*3, 2*1]), [4, 0]))

    # Team 4. a (x^3 - x^2 + 5)(x + 4) -t az x = 2 helyen
    # auto_diff("(x^3 - x^2 + 5) * (x + 4)", 2, 5, 4)
    # mul_diff(add_diff(sub_diff(pow_diff([2, 1], 3), pow_diff([2, 1], 2)), [5, 0]), add_diff([2, 1], [4, 0]))

    # Extra: sin(x^2)(y^3+2), x = 1, y = 2
    # diff x
    # auto_diff("sin(x^2) * (2^3 + 2)", 1, 2)
    # mul_diff(sin_diff(pow_diff([1, 1], 2)), add_diff(pow_diff([2, 0], 3), [2, 0]))

    # diff y
    # auto_diff("sin(1^2) * (x^3 + 2)", 2, 1, 2)
    # mul_diff(sin_diff(pow_diff([1, 0], 2)), add_diff(pow_diff([2, 1], 3), [2, 0]))

    # 3. Mi lesz az f(x,y) = x^3+y^2/x+x*cos(y)+4 kétváltozós függvény
    # automatikus deriváltja x = 2 és y = 3 helyen?
    # auto_diff("x^3 + 3^2 / x + x * cos(3) + 4", 2, 3, 4)  # x szerinti
    # add_diff(add_diff(add_diff(pow_diff([2, 1], 3), div_diff(pow_diff([3, 0], 2), [2, 1])), mul_diff([2, 1], cos_diff([3, 0]))), [4, 0])
    #
    # auto_diff("2^3 + x^2 / 2 + 2 * cos(x) + 4", 3, 3, 4)  # y szerinti
    # add_diff(add_diff(add_diff(pow_diff([2, 0], 3), div_diff(pow_diff([3, 1], 2), [2, 0])), mul_diff([2, 0], cos_diff([3, 1]))), [4, 0])

    # 4. Értékeld ki a fenti f(x,y) függvényt az x=[-1;1] és y=[0,4] intervallumon!
    # (((x ^ 3) + ((y ^ 2) / x)) + (x * (cos(y)))) + 4

    # pass
    # print(Interval([4, 3]) + Interval([-2, 5]))
    # print(Interval([1.0001, 5]))



if __name__ == '__main__':
    # unittest.main()
    main()
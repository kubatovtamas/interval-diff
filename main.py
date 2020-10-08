# TODO make differential class
# TODO implement diff.cald operators
# TODO make IO script


from __future__ import annotations
from typing import TypeVar, Union
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
    def low(self) -> number:
        return self.interval[0]

    @low.setter
    def low(self, value):
        self.interval[0] = value

    @property
    def high(self) -> number:
        return self.interval[1]

    @high.setter
    def high(self, value):
        self.interval[1] = value

    def __str__(self: Interval) -> str:
        return f"[{self.low}, {self.high}]"

    def __eq__(self: Interval, other: Interval) -> bool:
        """
            :return: true if the two Intervals low and high is close (rel_tol=0.0001)
            :param other: Interval instance
        """
        if isinstance(other, Interval):
            return math.isclose(self.low, other.low, rel_tol=0.0001) \
                   and math.isclose(self.high, other.high, rel_tol=0.0001)
        raise TypeError

    def __add__(self: Interval, other: Interval) -> Interval:
        """
            [a, b] + [c, d] = [a + c, b + d]

            :param other: Interval instance
            :return: new Interval
        """
        if isinstance(other, Interval):
            left = self.low + other.low
            right = self.high + other.high

            print(f"{self} + {other} = [{self.low} + {other.low}, {self.high} + {other.high}] = "
                  f"{Color.RED}[{left}, {right}]{Color.END}\n")
            return Interval([left, right])
        raise TypeError

    def __sub__(self: Interval, other: Interval) -> Interval:
        """
            [a, b] - [c, d] = [a - d, b - c]

            :param other: Interval instance
            :return: new Interval
        """
        if isinstance(other, Interval):
            left = self.low - other.high
            right = self.high - other.low

            print(f"{self} - {other} = [{self.low} - {other.high}, {self.high} - {other.low}] = "
                  f"{Color.RED}[{left}, {right}]{Color.END}\n")
            return Interval([left, right])
        raise TypeError

    def __mul__(self: Interval, other: Interval) -> Interval:
        """
            [a, b] * [c, d] = [min(ac, ad, bc, bd), max(ac, ad, bc, bd)]

            :param other: Interval instance
            :return: new Interval
        """
        if isinstance(other, Interval):
            left = min(self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high)
            right = max(self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high)

            print(
                f"[{self.low}, {self.high}] * [{other.low}, {other.high}] ="
                f"[min({self.low} * {other.low}, {self.low} * {other.high}, "
                f"{self.high} * {other.low}, {self.high} * {other.high}),"
                f" max({self.low:.3f} * {other.low}, {self.low} * {other.high}, "
                f"{self.high} * {other.low}, {self.high} * {other.high})"
                f" = {Color.RED} [{left}, {right}] {Color.END}\n")
            return Interval([left, right])
        raise TypeError

    def __truediv__(self: Interval, other: Interval) -> Interval:
        """
            [a, b] / [c, d] = [a, b] * [1/d, 1/c], if 0 not in [c, d]

            :param other: Interval instance
            :return: new Interval
        """
        if isinstance(other, Interval):
            if other.low <= 0 <= other.high:
                raise ZeroDivisionError

            right = Interval([1 / other.high, 1 / other.low])

            print(f"{self} / {other} = {self} * [1 / {other.high}, 1 / {other.low}] = ")
            return self * right
        raise TypeError

    def __pow__(self: Interval, power: int, modulo=None) -> Interval:
        """
            [a, b] ^ power = {
                [0, b^power] : if power is even, and 0 is in interval [a, b]

                [a^power, b^power] : otherwise
            }

            :param power: int number the Interval is raised to
            :return: new Interval
        """
        if self.low <= 0 <= self.high:
            print(f"{self}^{power} = {Color.RED}[0,{(self.high ** power)}]{Color.END}")
            return Interval([0, (self.high ** power)])
        val1 = self.low ** power
        val2 = self.high ** power

        print(f"{self}^{power} = {Color.RED}[{self.low ** power}, {self.high ** power}]{Color.END}")
        return Interval([min(val1, val2), max(val1, val2)])

    def __rxor__(self: Interval, other: number) -> Interval:
        """
            x^[a, b] = [x^a, x^b]

            :param other: number to be raised to interval Power
            :return: new Interval
        """
        left = other ** self.low
        right = other ** self.high

        print(f"{other}^{self} = {Color.RED}[{other}^{self.low}, {other}^{self.high}]{Color.END}")
        return Interval([left, right])

    def log(self: Interval, base: number = math.e) -> Interval:
        """
            log([a, b]) = [log(a), log(b)]

            :param base: base of log
            :return: new Interval
        """
        if self.low > 0 and self.high > 0 and base > 1:
            print(f"log({self}) = {Color.RED}[log({self.low}), log({self.high})]{Color.END}")
            return Interval([math.log(self.low, base), math.log(self.high, base)])
        raise ValueError

    def sin(self: Interval) -> Interval:
        """
            sin[a, b] = {
                [-1, ...], if 3pi/2 + 2k * pi in [a, b],

                [..., 1] if pi/2 + 2k * pi in [a, b],

                [min(sin(a), sin(b)), max(sin(a), sin(b))] otherwise
            }

            :return: new Interval
        """

        left = min(math.sin(self.low), math.sin(self.high))
        right = max(math.sin(self.low), math.sin(self.high))

        a = self.low
        b = self.high

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

        # Numeric errors close to 0 and 1
        if math.isclose(left, 0, abs_tol=0.0001):
            left = 0
        if math.isclose(right, 0, abs_tol=0.0001):
            right = 0

        print(f"sin({self}) = [min(sin(a), sin(b)), max(sin(a), sin(b))]\n"
              f"[-1, ...] ha 3pi/2 + 2k * pi eleme [a, b]-nek,\n"
              f"[..., 1]  ha pi/2 + 2k * pi eleme [a, b]-nek\n"
              f" => {Color.RED}[{left}, {right}]{Color.END}")
        return Interval([left, right])

    def cos(self: Interval) -> Interval:
        """
            cos[a, b] = {
                [-1, ...], if -pi + 2k * pi in [a, b],

                [..., 1] if 0 + 2k * pi in [a, b],

                [min(cos(a), cos(b)), max(cos(a), cos(b))] otherwise
            }

            :return: new Interval
        """
        left = min(math.cos(self.low), math.cos(self.high))
        right = max(math.cos(self.low), math.cos(self.high))

        a = self.low
        b = self.high

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

        # Numeric errors close to 0 and 1
        if math.isclose(left, 0, abs_tol=0.0001):
            left = 0
        if math.isclose(right, 0, abs_tol=0.0001):
            right = 0

        print(f"cos({self}) = [min(cos(a), cos(b)), max(cos(a), cos(b))]\n"
              f"[-1, ...] ha -pi + 2k * pi eleme [a, b]-nek,\n"
              f"[..., 1]  ha 0 + 2k * pi eleme [a, b]-nek\n"
              f" => {Color.RED}[{left}, {right}]{Color.END}")
        return Interval([left, right])


# Differential arithmetic
class Differential:
    def __init__(self, interval: list):
        self.interval = interval

    @property
    def val(self) -> number:
        return self.interval[0]

    @val.setter
    def val(self, value):
        self.interval[0] = value

    @property
    def diff(self) -> number:
        return self.interval[1]

    @diff.setter
    def diff(self, value):
        self.interval[1] = value

    def __str__(self: Differential) -> str:
        return f"[{self.val}, {self.diff}]"

    def __eq__(self: Differential, other: Differential) -> bool:
        """
            :return: true if the two Differentials val and diff is close (rel_tol=0.0001)
            :param other: Differential instance
        """
        if isinstance(other, Differential):
            return math.isclose(self.val, other.val, rel_tol=0.0001) \
                   and math.isclose(self.diff, other.diff, rel_tol=0.0001)
        raise TypeError

    def __add__(self: Differential, other: Union[Interval, number]) -> Differential:
        """
            (F + G)' = F' + G'

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, Differential):  # F + G
            left = self.val + other.val
            right = self.diff + other.diff

            print(f"{self} + {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        elif isinstance(other, (int, float)):  # F + c
            left = self.val + other
            right = self.diff

            print(f"{self} + {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __radd__(self: Differential, other: number) -> Differential:
        """
            (F + G)' = F' + G'

            :param other: Differential instance
            :return: new Differential
        """

        if isinstance(other, (int, float)):  # c + F
            left = self.val + other
            right = self.diff

            print(f"{self} + {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __sub__(self: Differential, other: Union[Interval, number]) -> Differential:
        """
            (F - G)' = F' - G'

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, Differential):  # F - G
            left = self.val - other.val
            right = self.diff - other.diff

            print(f"{self} - {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        elif isinstance(other, (int, float)):  # F - c
            left = self.val - other
            right = self.diff

            print(f"{self} - {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __rsub__(self: Differential, other: number) -> Differential:
        """
            (F - G)' = F' - G'

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, (int, float)):  # c - F
            left = other - self.val
            right = -self.diff

            print(f"{other} - {self} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __mul__(self: Differential, other: Union[Interval, number]) -> Differential:
        """
            (F * G)' = (F * G') + (F' * G)

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, Differential):  # F * G
            left = self.val * other.val
            right = self.val * other.diff + self.diff * other.val

            print(f"{self} * {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        elif isinstance(other, (int, float)):  # F * c
            left = other * self.val
            right = other * self.diff

            print(f"{other} * {self} = {Color.RED}[{left}, {right}]{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __rmul__(self: Differential, other: number) -> Differential:
        """
            n * [a, b] = [n * a, n * b]

            :param other: a real number
            :return: new Differential
        """
        if isinstance(other, (int, float)):  # c * F
            left = other * self.val
            right = other * self.diff

            print(f"{other} * {self} = {Color.RED}[{left}, {right}]{Color.END}")
            return Differential([left, right])

    def __truediv__(self: Differential, other: Union[Interval, number]) -> Differential:
        """
            (F / G)' = ((F' * G) - (F * G')) / G^2

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, Differential):  # F / G
            left = self.val / other.val
            right = (self.diff * other.val - self.val * other.diff) / other.val ** 2

            print(f"{self} / {other} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        elif isinstance(other, (int, float)):  # F / c
            left = other / self.val
            right = other / self.diff

            print(f"{other} / {self} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def __rtruediv__(self: Differential, other: number) -> Differential:
        """
            (F / G)' = ((F' * G) - (F * G')) / G^2

            :param other: Differential instance
            :return: new Differential
        """
        if isinstance(other, (int, float)):  # c / F
            print(f"{other} / {self} = ({other} * {self}^-1)")
            return (other * self ** -1)

    def __pow__(self: Differential, power: number, modulo=None) -> Differential:
        """
            (F^k)' = k * F^(k-1)

            :param power: the power to which the Differential interval is raised
            :return: new Differential
        """
        if isinstance(power, (int, float)):
            left = self.val ** power
            right = power * self.val ** (power - 1) * self.diff


            print(f"{self}^{power} = {Color.RED}{[left, right]}{Color.END}")
            return Differential([left, right])
        raise TypeError

    def log(self: Differential, base: number = math.e) -> Differential:
        """
            log_e([a,b]) = [log_e(a), b / a] if base == e
            log_a([a,b]) = [log_a(a), b / (a * ln a)] otherwise

            :param base: the logarithm's base
            :return: new Differential
        """
        if isinstance(base, (int, float)):
            if self.val > 0 and self.diff > 0 and base > 1:
                left = math.log(self.val, base)

                if base == math.e:
                    right = self.diff / self.val
                else:
                    right = self.diff / (self.val * math.log(base))

                print(f"log({self}) = {Color.RED}[{left}, {right}]{Color.END}")
                return Differential([left, right])
            raise ValueError
        raise TypeError

    def sin(self: Differential) -> Differential:
        """
            sin([a,b]) = [sin(a), cos(a) * b]

            :return: new Differential
        """
        left = math.sin(self.val)
        right = math.cos(self.val) * self.diff

        print(f"sin({self}) = {Color.RED}[{left}, {right}]{Color.END}")
        return Differential([left, right])

    def cos(self: Differential) -> Differential:
        """
            cos([a,b]) = [cos(a), -1 * sin(a) * b]

            :return: new Differential
        """
        left = math.cos(self.val)
        right = -1 * math.sin(self.val) * self.diff

        print(f"cos({self}) = {Color.RED}[{left}, {right}]{Color.END}")
        return Differential([left, right])


class IntervalClassTestCase(unittest.TestCase):
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
        self.assertTrue(t2 ** 3 == Interval([1, 8]))

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
        t4 = Interval([0, 2])

        self.assertTrue(math.e ^ t1 == Interval([math.e, math.e ** 2]))
        self.assertTrue(2 ^ t2 == Interval([2 ** -2, 2 ** 2]))
        self.assertTrue(math.pi ^ t3 == Interval([math.pi ** -6, math.pi ** 8]))
        self.assertTrue(2 ^ t4 == Interval([1, 4]))

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

    def test_interval_sin(self):
        t1 = Interval([0, math.pi])
        t2 = Interval([-4 * math.pi, 5 * math.pi / 2])
        t3 = Interval([math.pi, 4 * math.pi])
        t4 = Interval([0, 4])
        t5 = Interval([0, 2 * math.pi])
        t6 = Interval([-1 * math.pi / 2, 0])
        t7 = Interval([-1 * math.pi / 2, 1])

        self.assertTrue(Interval.sin(t1) == Interval([0, 1]))
        self.assertTrue(Interval.sin(t2) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t3) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t4) == Interval([-0.7568, 1]))
        self.assertTrue(Interval.sin(t5) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t6) == Interval([-1, 0]))
        self.assertTrue(Interval.sin(t7) == Interval([-1, math.sin(1)]))

    def test_cos_interval(self):
        t1 = Interval([0, 4])
        t2 = Interval([math.pi, 4 * math.pi])
        t3 = Interval([0, 13])
        t4 = Interval([0, 7])
        t5 = Interval([-math.pi / 2, 0])
        t6 = Interval([-math.pi, -math.pi / 2])

        self.assertTrue(Interval.cos(t1) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t2) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t3) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t4) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t5) == Interval([0, 1]))
        self.assertTrue(Interval.cos(t6) == Interval([-1, 0]))


class DifferentialTestCase(unittest.TestCase):
    def test_differential_init(self):
        d1 = Differential([1, 5])

        self.assertIsInstance(d1, Differential)
        self.assertEqual(d1.val, d1.interval[0])
        self.assertEqual(d1.diff, d1.interval[1])
        self.assertEqual(d1.val, 1)
        self.assertEqual(d1.diff, 5)

    def test_differential_add(self):
        d1 = Differential([2,1])
        d2 = Differential([13,1])
        c1 = Differential([3,0])
        c2 = Differential([1,0])

        self.assertTrue(d1 + c1 == Differential([5, 1]))
        self.assertTrue(c1 + d1 == Differential([5, 1]))
        self.assertTrue(c2 + d2 == Differential([14, 1]))

    def test_differential_sub(self):
        d1 = Differential([2, 1])
        d2 = Differential([13, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([1, 0])
        c3 = Differential([-5, 0])

        self.assertTrue(d1 - c1 == Differential([-1, 1]))
        self.assertTrue(c1 - d1 == Differential([1, -1]))
        self.assertTrue(d2 - c2 == Differential([12, 1]))
        self.assertTrue(d3 - c3 == Differential([0, 1]))

    def test_differential_mul(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([12, 0])
        c3 = Differential([8, 0])

        self.assertTrue(d1 * c1 == Differential([6, 3]))
        self.assertTrue(c1 * d1 == Differential([6, 3]))
        self.assertTrue(c2 * d2 == Differential([120, 12]))
        self.assertTrue(c3 * d3 == Differential([-40, 8]))

    def test_differential_truediv(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([12, 0])
        c3 = Differential([8, 0])

        self.assertTrue(d1 / c1 == Differential([2/3, 1/3]))
        self.assertTrue(c1 / d1 == Differential([3/2, -3/4]))
        self.assertTrue(d2 / c2 == Differential([5/6, 1/12]))
        self.assertTrue(d3 / c3 == Differential([-5/8, 1/8]))

    def test_differential_pow(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1 ** 0 == Differential([1, 0]))
        self.assertTrue(d1 ** 1 == Differential([2, 1]))
        self.assertTrue(d1 ** -1 == Differential([1/2, -1/4]))

        self.assertTrue(d2 ** 3 == Differential([1000, 300]))

        self.assertTrue(d3 ** 3 == Differential([-125, 75]))
        self.assertTrue(d3 ** -3 == Differential([-1/125, -3/625]))

    def test_differential_log(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.log() == Differential([math.log(2), 1/2]))
        self.assertTrue(d2.log() == Differential([math.log(10), 1/10]))
        self.assertEqual(d2.log(2).interval[0], math.log(10) / math.log(2))
        self.assertEqual(d2.log(2).interval[1], 1 / math.log(1024))

        with self.assertRaises(ValueError):
            d3.log()

    def test_differential_sin(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.sin() == Differential([math.sin(2), math.cos(2)]))
        self.assertTrue(d2.sin() == Differential([math.sin(10), math.cos(10)]))
        self.assertTrue(d3.sin() == Differential([- math.sin(5), math.cos(5)]))

    def test_differential_cos(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.cos() == Differential([math.cos(2), -math.sin(2)]))
        self.assertTrue(d2.cos() == Differential([math.cos(10), -math.sin(10)]))
        self.assertTrue(d3.cos() == Differential([math.cos(5), math.sin(5)]))

    def test_differential_rmul(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(2 * d1 == Differential([4, 2]))
        self.assertTrue(5 * d2 == Differential([50, 5]))
        self.assertTrue(-3 * d3 == Differential([15, -3]))
        self.assertTrue(0 * d1 == Differential([0, 0]))


def main():
    # I. Intervallum aritmetika
    print("[1;4]+[-1;2]/[-5;-1]-[-2;1] = [1;4]+[-1;2]*[-1;-1/5]-[-2;1] = "
          "[1;4]+[-2;1] -[-2;1] = [-1;5] -[-2;1] = [-2;7]")

    i1 = Interval([1, 4])
    i2 = Interval([-1, 2])
    i3 = Interval([-5, -1])
    i4 = Interval([-2, 1])

    i1 + i2 / i3 - i4


    # II. Automatikus differenciálás
    print("\nlog(x) * (x^2+2x+4) -t az x = 3 helyen")

    x = Differential([3, 1])
    c = Differential([4, 0])

    x.log() * (x**2 + 2*x +c)  # [20.873, 15.122]


    print("\n\n(x^3 - x^2 + 5)(x + 4) -t az x = 2 helyen")

    x = Differential([2, 1])
    c1 = Differential([5, 0])
    c2 = Differential([4, 0])
    (x**3 - x**2 + c1) * (x + c2)  ## [54, 57]

    print("\n\nsin(x^2) * (y^3+2), x = 1, y = 2")
    x = Differential([1, 1])
    xd = Differential([1, 0])
    y = Differential([2, 1])
    yd = Differential([2, 0])
    c = Differential([2, 0])

    print("\nx szerinti deriváltja:")
    (x ** 2).sin() * (yd ** 3 + c)  # [8.414, 10.806]

    print("\ny szerinti deriváltja:")
    (xd ** 2).sin() * (y ** 3 + c)  # [8.415,10.1]



if __name__ == '__main__':
    # unittest.main()
    main()
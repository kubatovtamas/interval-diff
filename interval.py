from __future__ import annotations
from common import *


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
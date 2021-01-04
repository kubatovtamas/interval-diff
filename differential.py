from __future__ import annotations
from common import *

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

    def __add__(self: Differential, other: Union[Differential, number]) -> Differential:
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

    def __sub__(self: Differential, other: Union[Differential, number]) -> Differential:
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

    def __mul__(self: Differential, other: Union[Differential, number]) -> Differential:
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

    def __truediv__(self: Differential, other: Union[Differential, number]) -> Differential:
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
from __future__ import annotations

import math
from fractions import Fraction
from decimal import Decimal
import itertools

superscripts = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


class Polynomial:
    def __init__(self, coeff_list: list) -> None:
        self.coeff = list(itertools.dropwhile(lambda x: x == 0, coeff_list))
        if not self.coeff:  # edge case: coeff_list == [0]
            self.coeff = [0]

        self.degree = len(self.coeff) - 1

    def coeff_and_power(self) -> tuple:
        for idx, c in enumerate(self.coeff):
            yield (c, self.degree - idx)

    def _number_to_poly(num) -> Polynomial:
        if isinstance(num, (int, float, Decimal, Fraction)):
            return Polynomial([num])
        else:
            return num

    def __neg__(self) -> Polynomial:
        return Polynomial([-c for c in self.coeff])

    def __pos__(self) -> Polynomial:
        return self

    def __add__(self, other) -> Polynomial:
        other = Polynomial._number_to_poly(other)
        common_degree = max(self.degree, other.degree)
        coeff1 = [0] * (common_degree - self.degree) + self.coeff
        coeff2 = [0] * (common_degree - other.degree) + other.coeff
        coeff_result = [c1 + c2 for c1, c2 in zip(coeff1, coeff2)]
        return Polynomial(coeff_result)

    def __sub__(self, other) -> Polynomial:
        other = Polynomial._number_to_poly(other)
        return self.__add__(-other)

    def _term_mul(self, coeff, power) -> Polynomial:
        """Helper function to multiply a polynomial by an individual term."""
        terms = [(coeff * c, p + power) for c, p in self.coeff_and_power()]
        terms = sorted(terms, key=lambda x: x[1], reverse=True)
        degree = terms[0][1]  # power of the leading term
        terms = terms + [(0, 0)] * (degree - len(terms) + 1)
        return Polynomial([t[0] for t in terms])

    def __mul__(self, other) -> Polynomial:
        other = Polynomial._number_to_poly(other)
        h = [self._term_mul(c, p) for c, p in other.coeff_and_power()]
        s = Polynomial([0])
        for p in h:
            s += p
        return s

    def evaluate(self, x):
        return sum(coeff * (x**power) for coeff, power in self.coeff_and_power())

    def __str__(self) -> str:
        # Polynomial(4x¹⁰+6x⁹-7x⁸+4x⁷+2x⁶-4x⁵+6x⁴+2x³+3x²-5x+3)
        polynomial = ""
        if self.coeff == [0]:
            return "Polynomial(0)"
        for coeff, power in self.coeff_and_power():
            if coeff != 0:
                if coeff >= 0:
                    polynomial += "+"
                if coeff != 1 or power == 0:
                    polynomial += str(coeff)
                if power > 1:
                    polynomial += "x" + "".join(superscripts[p] for p in str(power))
                if power == 1:
                    polynomial += "x"
        return f"Polynomial({polynomial.lstrip('+')})"

    def __repr__(self) -> str:
        return self.__str__()


def polynomial_sum(polynomials) -> Polynomial:
    s = Polynomial([0])
    for p in polynomials:
        s += p
    return s


print(Polynomial([3, 3]) * Polynomial([5, 3, 6]))

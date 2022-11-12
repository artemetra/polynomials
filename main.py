import math
from fractions import Fraction
from decimal import Decimal

superscripts = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
}

class Polynomial:
    def __init__(self, coeff_list: list) -> None:

        # removes leading 0 coefficients
        for idx, i in enumerate(coeff_list):
            if i:
                self.coeff = coeff_list[idx:]
                break
        
        self.degree = len(self.coeff)-1

    def __neg__(self):
        return Polynomial([-c for c in self.coeff])

    def __pos__(self):
        return self

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Polynomial([other])
        common_degree = max(self.degree, other.degree)
        coeff1 = [0] * (common_degree-self.degree) + self.coeff
        coeff2 = [0] * (common_degree-other.degree) + other.coeff
        coeff_result = [c1 + c2 for c1, c2 in zip(coeff1, coeff2)]
        return Polynomial(coeff_result)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Polynomial([other])
        return self.__add__(-other)

    def __mul__(self, other):
        ...

    def evaluate(self, x):
        return sum(
            c*(x**(self.degree-idx)) for idx, c in enumerate(self.coeff)
        )

    def __str__(self) -> str:
        # Polynomial(4x¹⁰+6x⁹-7x⁸+4x⁷+2x⁶-4x⁵+6x⁴+2x³+3x²-5x+3)
        polynomial = ""
        for idx, c in enumerate(self.coeff):
            if c != 0:
                power = self.degree - idx
                if c >= 0:
                    polynomial += '+'
                if c != 1 or power == 0:
                    polynomial += str(c)
                if power > 1:
                    polynomial += "x" + "".join(superscripts[p] for p in str(power))
                if power == 1:
                    polynomial += "x"
        return f"Polynomial({polynomial.lstrip('+')})" 

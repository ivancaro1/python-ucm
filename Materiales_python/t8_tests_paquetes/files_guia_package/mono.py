from ..rationals import Rational
from functools import total_ordering
from typing import Self

@total_ordering
class Monomial(object):
    """
    This class represents a monomial: coef * x^degree
    * coef will be a rational number
    * degree>=0 an integer
    * if coef==0, then degree==0
    """
    def __init__(self, coef: Rational = Rational(num=0),
                 degree: int = 0):
        self.coef = coef
        self.degree = degree
        if self.coef == 0:
            self.degree = 0

    def __add__(self, other: Self) -> Self:
        if self.coef == 0:
            return Monomial(other.coef, other.degree)
        if other.degree!=self.degree:
            raise ValueError("I can only sum monomials with the same degree")
        return Monomial(self.coef + other.coef, self.degree)

    def __mul__(self, other: Self) -> Self:
        return Monomial(self.coef * other.coef, self.degree+other.degree)

    def __lt__(self, other: Self) -> Self:
        return (self.degree < other.degree) or \
            (self.degree == other.degree and self.coef < other.coef)

    def __eq__(self, other: Self) -> Self:
        return self.degree == other.degree and self.coef == other.coef


    def __repr__(self) -> str:
        s=str(self.coef)
        if self.degree>0:
            s+=f"·x^{self.degree}"
        return s

    def __truediv__(self, other: Self) -> Self:
        if other.coef == Rational(0):
            raise ValueError("The divisor monomial cannot be zero")
        if other.degree > self.degree:
            raise ValueError("The degree of the divisor monomial cannot be greater than the dividend monomial")
        return Monomial(self.coef/other.coef, self.degree-other.degree)

    @classmethod
    def parse(cls, s:str):
        """
        This static method parses a string that should contain a monomial
        of one of the following forms:
          - <rational> * x^<integer>
          - <rational>
        @type s: string
        @rtype: Monomial
        @raise Exception: if the string is not as described above
        """
        l = s.strip().split("·")
        coef = Rational.parse(l[0].strip())
        if len(l)==1:
            exp=0
        else:
            l[1] = l[1].strip()
            if len(l[1]) == 1:
                exp = 1
            else:
                exp = int(l[1].strip()[2:])
        return cls(coef,exp)

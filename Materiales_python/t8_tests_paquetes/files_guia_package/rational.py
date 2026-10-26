
import functools
from typing import Self

def gcd(a: int, b: int) -> int:
    '''
    Returns the Greatest common divisor (gcd) of a and b.

    :param a: non negative integer
    :param b: positve integer
    :returns: the gcd of a and b
    :raises ValueError: if
      - a is negatve
      - b is non positive

    Examples
    --------
    >>> gcd(24, 16)
    8

    >>> gcd(30, 35)
    5

    >>> gcd(-3, 4)
    Traceback (most recent call last):
        ...
    ValueError: a = -3 must be non negative

    >>> gcd(3, 0)
    Traceback (most recent call last):
        ...
    ValueError: b = 0 must be a positive integer
    '''

    if a<0:
        raise ValueError(f'a = {a} must be non negative')
    if b<=0:
        raise ValueError(f'b = {b} must be a positive integer')

    while b!=0:
        r = a%b
        a = b
        b = r
    return a

@functools.total_ordering
class Rational(object):
    """
    Class to represent rationals: numerator/denominator.
    * denominator > 0
    * numerator and denominator do not have common divisors.
    * if numerator is 0, then denominator is 1

    This class uses the indications in
    http://docs.python.org/reference/datamodel.html#emulating-numeric-types
    to make the rationals easy to use.
    """
    def __init__(self, num:int = 0, den:int = 1):
        """
        Builds a rational
        :num: int
          numerator of the rational
        :den:
          denominator of the rational.
          den != 0
        :raise ValueError: if den == 0
        """
        self._num, self._den = Rational._normalize(num, den)


    @staticmethod
    def _normalize(num:int, den:int) -> tuple[int, int]:
        """
        This returns the numerator and denominator normalized, that is,
        - the sign is in the numerator,
        - if the numerator is zero, the denominaror is 1,
        - the numerator and denominator do not have common divisors.
        """
        if den == 0:
            raise ValueError('The denominator of a rational cannot be zero')

        if den < 0:
            den = -den
            num = -num

        if num != 0:
            divisor = gcd(abs(num), den)
            num = num // divisor
            den = den // divisor
        else:
            den = 1
        return num, den

    @property
    def numerator(self) -> int:
        return self._num

    @property
    def denominator(self) ->int:
        return self._den

    def __repr__(self) -> str:
        """
        Function to transform the rational into a string.
        See the special mehtods in python:
        http://docs.python.org/reference/datamodel.html#special-method-names
        """
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return str(self.numerator)+"/"+str(self.denominator)

    def __add__(self, other: Self | int) -> Self:
        """
        Sum this rational to other
        :other: Rational or int
        :returns: Rational
          a new rational.
        """
        if isinstance(other, Rational):
            divisor = gcd(self.denominator, other.denominator)
            denominator = ( self.denominator * other.denominator ) // divisor
            return Rational( self.numerator*denominator // self.denominator +
                             other.numerator*denominator // other.denominator
                             , denominator)
        elif isinstance(other, int):
            return Rational( self.numerator + other*self.denominator,
                             self.denominator)
        else:
            return NotImplemented

    def __radd__(self, other: int) -> Self:
        """
        this mehtod allows the sum of an integer and a rational
        when the first argument is not a rational
        :other: Rational
        :returns: Rational
        """
        return self.__add__(other)


    def __neg__(self) -> Self:
        """
        This function computes the opposite rational.
        :returns: Rational
          a new rational
        """
        return Rational(-self.numerator, self.denominator)

    def __sub__(self, other: Self | int) -> Self:
        """
        This function performs the substraction between rationals.
        :other: Rational or int
        :returns: Rational
        """
        return self + (-other)

    def __mul__(self, other: Self | int) -> Self:
        """
        This function performs the mutltiplicationa between rationals
        and between rationals ant integers.
        :other: Rational or int
        :returns: Rational
        """
        if isinstance(other, int):
            return Rational(self.numerator*other, self.denominator)
        elif isinstance(other, Rational):
            return Rational(self.numerator*other.numerator,
                            self.denominator*other.denominator)
        else:
            return NotImplemented

    def __pow__(self, other: int) -> int:
        if isinstance(other, int):
            return Rational(self.numerator ** other, self.denominator ** other)
        else:
            return NotImplemented

    def __rmul__(self, other: int):
        """
        This method allows the multiplication when the first operator is an integer.
        :other: int
        :returns: Rational
        """
        return self.__mul__(other)



    def _inv(self) -> Self:
        """
        This function computes the inverse (if exists) if the rational
        :returns: Rational
        :raise ValueError: if this rational is zero.
        """
        return Rational(self.denominator, self.numerator)

    def __div__(self, other : Self | int) -> Self:
        """
        This function performs the divistion between rationals
        :ther: Rational or int
        :returns: Rational
        :raise ValueError: if the other rational is zero
        """
        if isinstance(other, int):
            return self * Rational(1, other)
        elif isinstance(other, Rational):
            return self * other._inv()
        else:
            return NotImplemented


    def __truediv__(self, other: Self | int) -> Self:
        """
        This function performs the divistion between rationals
        :other: Rational or int
        :returns: Rational
        :raise Exception: if the other rational is zero
        """
        return self.__div__(other)



    def _cmp_rational(self, other: Self) -> int:
        """
        This method compares this rational to another rational number.
        :other: Rational
        :returns: integer
        """
        diff = self - other
        return diff.numerator

    def _cmp_integer(self, other: int) -> int:
        """
        This method compares this rational to an integer
        """
        diff = self - Rational(other)
        return diff.numerator

    def _cmp_float(self, other: float) -> int:
        """
        This method compares this rational to a float

        :returns:
         - 0 if equals
         - <0 if other is bigger than self
         - >0 if self is bigger than other
        """
        diff = self.numerator / self.denominator - other
        if diff < 0:
            return -1
        elif diff > 0:
            return 1
        else:
            return 0

    def __cmp__(self, other: Self | int | float) -> int:
        """
        Method to compare two numbers. other can be an integer
        a float or a rational.
        :other: Rational, int or float
        :returns: int
                  0 if equals
                  <0 if other is bigger than self
                  >0 if self is bigger that other
        """
        if isinstance(other, Rational):
            return self._cmp_rational(other)
        elif isinstance(other, int):
            return self._cmp_integer(other)
        elif isinstance(other, float):
            return self._cmp_float(other)

    def __lt__(self, other: Self | int | float) -> bool:
        """
        Method to implement the less than comparation operator.
        This method is necessary to ensure the compatibility with python 3.
        It is not necesary in python 2
        :other: Rational, int or float
        :returns: boolean
                  True if self is lower than other
                  False otherwise
        """
        return self.__cmp__(other) < 0

    def __eq__(self, other: object) -> bool:
        """
        Method to implement the less than comparation operator
        This method is necessary to ensure the compatibility with python 3.
        It is not necesdary in python 2.
        :other: Rational, int
        :returns: boolean
                  True if self and other are equls
                  False otherwise
        """
        return self.__cmp__(other) == 0


    def __hash__(self):
        if self.denominator != 1:
            return hash((self.numerator, self.denominator))
        else:
            return hash(self.numerator)


    @classmethod
    def parse(cls, s: str):
        """
        This static function builds a rational from a string. The
        rational can have the folowing forms:
          - <integer>
          - <integer>/<integer>
        @raise Exception: This function can raise an exception
           - There is no number at all
           - if the second integer is zero
        :s: string
        :returns: Rational
        """
        l = s.strip().split("/")
        num = int(l[0].strip())
        if len(l)>1:
            den = int(l[1].strip())
        else:
            den = 1
        return cls(num, den)

if __name__ == "__main__":
    r1 = Rational(2, 4)
    print(r1)


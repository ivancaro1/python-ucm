from copy import copy, deepcopy #See http://docs.python.org/library/copy.html
import sys
from functools import total_ordering
from .mono import Monomial
from ..rationals import Rational

@total_ordering
class Polynomial(object):
    """
    This class represent a polynomial with rational coefficients.
    The polynomial is represented by a list of monomials satisfying:
    * There are no monomials with zero coeficient.
    The zero polynomial is the empty list
    * The list is ordered according the degree of the monomial.
    The longer degree first.
    * There are no monomials with the same degree.
    """
    def __init__(self, monomials: list[Monomial] = []):
        # If we do not copy the monomials and we modify the monomials
        # the default parameter may change see
        monomials = deepcopy(monomials)
        Polynomial.simplify(monomials)
        self.monomials = monomials

    @staticmethod
    def simplify(monomials: list[Monomial]) -> None:
        #Since the __cmp__ method of monomials only consider the
        #degree, it is enough to consider any sorting algorithm.
        monomials.sort()
        Polynomial.simplify_equal_degree_monomials(monomials)
        Polynomial.remove_zero_monomials(monomials)

    @staticmethod
    def remove_zero_monomials(monomials: list[Monomial]) -> None:
        """
        This function remove all monomials whose coefficient is zero
        """
        zero = Rational(0)
        i=0
        n=len(monomials)
        while i<n:
            if zero == monomials[i].coef:
                del monomials[i]
                n=n-1
            else:
                i+=1

    @staticmethod
    def simplify_equal_degree_monomials(monomials: list[Monomial]) -> None:
        """
        self.monomials is list of monomials sorted according the
        degree.
        """
        n=len(monomials)
        if n>1:
            prev = monomials[0]
            i=1
            while i<n:
                curr = monomials[i]
                if curr.degree==prev.degree:
                    prev = prev + curr
                    monomials[i-1] = prev
                    del monomials[i]
                    n=n-1
                else:
                    prev=curr
                    i+=1
    @classmethod
    def parse(cls, s):
        """
        This static function parses a polynomial from the string s.
        The string maybe the empty one (to denote the zero polynomial)
        of have the following form
        <monomial> + <monomial> + <monomial> .... + <monomial>
        @type s: string
        @rtype: Polynomial
        @raise Exception: if the monomial is not as described above

        """
        l = s.strip().split("+")
        monomials = [None]*len(l)
        i=0
        while i<len(l):
            monomials[i] = Monomial.parse(l[i])
            i+=1
        return cls(monomials)

    @classmethod
    def normalize(cls, monomials: list[Monomial]) -> list[Monomial]:
        """
        Returns an new polinomial normalized with the most representative
        coeficient equals to one.
        """
        coef = monomials[0].coef
        monomials = []
        i = 0
        while i<len(monomials):
            m = deepcopy(monomials[i])
            m.coef = m.coef/coef
            monomials.append(m)
            i += 1
        return cls(monomials)


    def mul_monomial(self, monomial):
        """
        Multiplies the polynomial self by the given monomial
        @type monomial: Monomial
        @param monomial: the coefficient of the monomual is not null.
        """
        i=0
        n=len(self.monomials)
        while i<n:
            self.monomials[i] = self.monomials[i]*monomial
            i+=1

    def __mul__(self,other):
        m = Polynomial([])
        for a in self.monomials:
            s = deepcopy(other)
            s.mul_monomial(a)
            m = m + s
        return m

    def __add__(self,other):
        """
        Note that both, self and other are well constucted polynomials.
        Then it is enough to consider a merge-like algorithm.
        """
        s=Polynomial([])
        i=0
        j=0
        n=len(self.monomials)
        m=len(other.monomials)
        while i<n and j<m:
            if self.monomials[i].degree < other.monomials[j].degree:
                #We do not want memory sharing, so we copy the monomial
                s.monomials.append(deepcopy(self.monomials[i]))
                i+=1
            elif self.monomials[i].degree > other.monomials[j].degree:
                #We do not want memory sharing, so we copy the monomial
                s.monomials.append(deepcopy(other.monomials[j]))
                j+=1
            else:
                new = self.monomials[i] + other.monomials[j]
                if new.coef!=Rational(num=0):
                    s.monomials.append(new)
                i+=1
                j+=1
        while i<n:
                #We do not want memory sharing, so we copy the monomial
            s.monomials.append(deepcopy(self.monomials[i]))
            i+=1
        while j<m:
                #We do not want memory sharing, so we copy the monomial
            s.monomials.append(deepcopy(other.monomials[j]))
            j+=1

        return s

    def __neg__(self):
        """
        This function returns the opposite polynomial
        @rtype: Polynomial
        """
        n = deepcopy(self)
        for m in n.monomials:
            m.coef = -m.coef
        return n

    def __sub__(self,other):
        """
        This function implements the subtraction of polynomials
        @type other: polynomial
        @rtype: Polynomial
        """
        return self + (-other)

    def max_degree(self):
        """
        This function returns the coeficient of the monomial of degree 0 of the polynomial
        @rtype: Rational
        """
        n=len(self.monomials)
        if n==0:
            return Monomial(Rational(0),0)
        else:
            return self.monomials[n-1]

    def degree(self):
        """
        This fucntion returns the degree of the polynomial
        @rtype: integer
        """
        return self.max_degree().degree

    def div_zero_degree(self,q):
        """
        This function divides polynomial p by polynomial q, but
        having into acount that q has degree zero. The remainder is
        always zero, so this function only returns a polynomial
        @type q: Polynomial
        @param q: zero degree polynomial
        @rtype Polynomial
        @param: d where self = q * d
        """
        if len(q.monomials)==0:
            raise Exception("The divisor cannot be zero")
        else:#if degree of q is zero and is not the polynomial zero
            #the only monomial it can have has the coieficient that has
            #to divide q and it cannot be zero
            r = q.monomials[0].coef
        d = deepcopy(self)
        for m in d.monomials:
            m.coef = m.coef/r
        return d

    def __divmod__(self, other):
        """
        This function implements the divmod function
        @rtype other: polynomial
        @rtype: tuple of two polynomials
        @param: returns (q,r) such that
          - if other.degree() >0: self= q * other + r and r.degree()<other.degree()
          - if other.degree()==0: seff = q*other and r is the zero polynomial
        @raise Exception: if the degree of other is zero
        """
        if other.degree()==0:
            return self.div_zero_degree(other), Polynomial([])
        q = Polynomial([]) #Polynomial zero
        r = deepcopy(self)
        while r.degree()>=other.degree():
            cur = r.max_degree() / other.max_degree()
            q.monomials.insert(0,cur)
            m = deepcopy(other)
            m.mul_monomial(cur)
            r -= m
        return q,r

    def __floordiv__(self,other):
        """
        This function implements the // operation
        @rtype other: polynomial
        @rtype: polynomial
        @param: returns the quiotient of the division see __divmod()__
        @raise Exception: if the degree of other is zero
        """
        (q,r) = divmod(self,other)
        return q

    def __mod__(self,other):
        """
        This function implements the % operation
        @rtype other: polynomial
        @rtype: tuple of two polynomials
        @param: returns the remainder of the division see __divmod()__
        @raise Exception: if the degree of other is zero
        """
        (q,r) = divmod(self, other)
        return r

    def __repr__(self):
        if len(self.monomials)>0:
            s = ""
            for m in self.monomials:
                if s!="":
                    s+=" + "
                s += str(m)
            return s
        else:
            return "0"


    """Functions to compute equality. We need to compare the polynomial
       to the zero integer to apply the euclidean_domain functions.
       So we extend the equality to any numerical value,
       so the rationals must implement the equality to any numerical value"""
    def eq_num(self, num):
        if len(self.monomials) > 1:
            return False
        elif len(self.monomials) == 1:
            m = self.monomials[0]
            return m.degree == 0 and m.coef == num
        else:
            return num == 0

    def eq_poly(self, other):
        n = len(self.monomials)
        m = len(other.monomials)
        if m != n:
            return False
        i=0
        while i<n and self.monomials[i] == other.monomials[i]:
            i+=1
        return i==n

    def lt_num(self, num):
        if len(self.monomials) > 1:
            return False
        elif len(self.monomials) == 1:
            m = self.monomials[0]
            return m.degree == 0 and m.coef < num
        else:
            return num < 0

    def lt_poly(self, other):
        n = len(self.monomials)
        m = len(other.monomials)
        i=0
        while i<n and i<m and self.monomials[i] == other.monomials[i]:
            i+=1
        if i == n:
            return False
        elif i == m:
            return True
        else:
            return self.monomials[i].degree < other.monomials[i].degree

    def __eq__(self,other):
        if isinstance(other,Polynomial):
            return self.eq_poly(other)
        elif isinstance(other, int):
            return self.eq_num(other)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Polynomial):
            return self.lt_poly(other)
        elif isinstance(other, int):
            return self.lt_num(other)
        else:
            return NotImplemented


    def diff(self):
        """
        Computes the derivate of this polinomial
        """
        monomials = []
        i = 0
        while i<len(self.monomials):
            curr = self.monomials[i]
            if curr.degree > 0:
                coef = curr.coef * Rational(curr.degree, 1)
                degree = curr.degree -1
                monomials.append(Monomial(coef, degree))
            i += 1
        return Polynomial(monomials)


    def eval(self, x):
        res = Rational(0,1)
        for m in self.monomials:
            res += m.coef * x**m.degree
        return res


if __name__ == "__main__":
    a = Polynomial([Monomial(coef=Rational(1)),
                    Monomial(coef=Rational(2)),
                    Monomial(coef=Rational(0), degree=1)])
    #assert repr(a) == "3"
    print(a)

    # para ejecutar en terminal
    #uv run python -m algebra.polynomials.polynomials

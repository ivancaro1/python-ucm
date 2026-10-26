from ejemplo_paquete.polynomials import Polynomial, Monomial
from ejemplo_paquete.rationals import Rational
from ejemplo_paquete.rationals.rational import gcd

def test_init():
    a = Polynomial([Monomial(coef=Rational(1)),
                    Monomial(coef=Rational(2)),
                    Monomial(coef=Rational(0), degree=1)])
    assert repr(a) == "3"

    b = Polynomial([Monomial(Rational(1),1),
                    Monomial(Rational.parse("2"),2),
                    Monomial(Rational.parse("-1/3"),1),
                    Monomial(Rational.parse("-2"),2),
                    ])
    assert repr(b) == "2/3·x^1"
    print("OK")


def test_eval():
    p1 = Polynomial.parse("1/2 + 2·x")
    assert p1.eval(Rational(0,1)) == Rational(1,2)
    assert p1.eval(Rational(1,1)) == Rational(5,2)
    assert p1.eval(Rational(1,2)) == Rational(3,2)

    p1 = Polynomial.parse("1/2 + 2·x + -1·x^2")
    assert p1.eval(Rational(0,1)) == Rational(1,2)
    assert p1.eval(Rational(1,1)) == Rational(3,2)
    assert p1.eval(Rational(1,2)) == Rational(5,4)

    p1 = Polynomial.parse("1/2 + 2·x + -1·x^2 + 1/3·x^3")
    assert p1.eval(Rational(0,1)) == Rational(1,2)
    assert p1.eval(Rational(1,1)) == Rational(11,6)
    assert p1.eval(Rational(1,2)) == Rational(31,24)

    print('Ok. eval')




def test_eq():
    a = Polynomial([Monomial(coef=Rational(1)),
                    Monomial(coef=Rational(2)),
                    Monomial(coef=Rational(0), degree=1)])
    b = Polynomial.parse("3")
    print(b, a)
    assert a == b

    a = Polynomial([Monomial(Rational(1),1),
                    Monomial(Rational.parse("2"),2),
                    Monomial(Rational.parse("-1/3"),1),
                    Monomial(Rational.parse("-2"),2),
                    ])
    assert a == Polynomial.parse("2/3·x^1")

    a = Polynomial([Monomial(Rational(1),1),
                    Monomial(Rational.parse("2"),2),
                    Monomial(Rational.parse("-1/3"),1)
                    ])
    assert a == Polynomial.parse("2·x^2 + 2/3·x^1")

    a = Polynomial([Monomial(Rational(1),1),
                    Monomial(Rational.parse("2"),2),
                    Monomial(Rational.parse("-1/3"),1)
                    ])
    assert a == Polynomial.parse("2·x^2 + 2/3·x^1 + 0·x^5")

    print('OK')

def test_sum():
    p1 = Polynomial.parse("2·x^3 + -2/3·x^1 + 2·x^1")
    p2 = Polynomial.parse("3·x^4 + 2/3·x^1 + -1·x^1")
    p3 = p1 + p2
    assert p3 == Polynomial.parse("3·x^4 +2·x^3 + 1·x^1")

    p1=Polynomial.parse("5 +           3·x^2 + 4·x^3")
    p2=Polynomial.parse("6 + 1·x^1 + -3·x^2 + 6·x^4")
    p3 = p1 + p2
    assert p3 == Polynomial.parse("6·x^4 +4·x^3 + 1·x^1 + 11")
    print('OK')

def test_mul():
    p1 = Polynomial.parse("2·x^3 + -2/3·x^1 + 2·x^1")
    p2 = Polynomial.parse("3·x^4 + 2/3·x^1 + -1·x^1")
    p3 = p1 * p2
    print(p3)
    assert p3 == Polynomial.parse("-4/9·x^2 + -2/3·x^4 + 4·x^5 + 6·x^7")

    p1=Polynomial.parse("5 +           3·x^2 + 4·x^3")
    p2=Polynomial.parse("6 + 1·x^1 + -3·x^2 + 6·x^4")
    p3 = p1 * p2
    print(p3)
    assert p3 == Polynomial.parse("30 + 5·x^1 + 3·x^2 + 27·x^3 + 25·x^4 + -12·x^5 + 18·x^6 + 24·x^7")
    print('OK')


def test_div():
    c = Polynomial.parse("5 +           3·x^2 + 4·x^3")
    d = Polynomial.parse("6 + 1·x^1 + -3·x^2 + 6·x^4")
    r = Polynomial.parse("1/2 + -3/4·x^1 + 1/3·x^2")
    D = d*c + r
    print(D)

    d1, r1 = divmod(D, c)
    assert d1 == d and r1 == r

    print('OK')


def test_gcd():
    a = Polynomial.parse("5 +           3·x^2 + 4·x^3")
    b = Polynomial.parse("6 + 1·x^1 + -3·x^2 + 6·x^4")
    c = gcd(a, b)
    assert c.degree() ==  0

    a = Polynomial.parse("1·x^2 + 1")
    b = Polynomial.parse("1·x^2 + -1")
    c = Polynomial.parse("1·x^1 + 2")

    d = a * c
    e = b * c

    f = gcd(d, e)

    assert Polynomial.normalize(c.monomials) == Polynomial.normalize(f.monomials)
    print('OK gcd')

def test_diff():
    a = Polynomial.parse("6 + 1·x + -3·x^2 + 6·x^4")
    b = Polynomial.parse("1 + -6·x + 24·x^3")
    c = Polynomial.parse("-6 + 72·x^2")
    d = Polynomial.parse("144·x")
    e = Polynomial.parse("0")
    assert a.diff() == b
    assert b.diff() == c
    assert c.diff() == d
    assert e.diff() == e
    assert e.diff() == e
    print('OK. diff')

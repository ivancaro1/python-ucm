from ejemplo_paquete.polynomials import Monomial
from ejemplo_paquete.rationals import Rational

def test_parse():
    m = Monomial.parse("1·x")
    assert m.coef == Rational(1,1) and m.degree == 1
    m = Monomial.parse("1/2·x")
    assert m.coef == Rational(1,2) and m.degree == 1
    m = Monomial.parse("2·x")
    assert m.coef == Rational(2) and m.degree == 1
    m = Monomial.parse("1/2·x^2")
    assert m.coef == Rational(1, 2) and m.degree == 2
    print('OK. parse')

def test_equal():
    m1 = Monomial.parse("0·x^5")
    m2 = Monomial.parse("0·x^3")
    assert m1 == m2 and m2 == m1

    m1 = Monomial.parse("2·x^5")
    m2 = Monomial.parse("4/2·x^5")
    assert m1 == m2 and m2 == m1

    m1 = Monomial.parse("2·x^5")
    m2 = Monomial.parse("1/4·x^5")
    assert not m1 == m2  and not m2 == m1
    print('OK')

def test_sum_monomial():
    m1 = Monomial.parse("3/13·x^5")
    m2 = Monomial.parse("12/13·x^5")
    m3 = m1 + m2
    assert m3 == Monomial.parse("15/13·x^5")


    m1 = Monomial.parse("3/13·x^5")
    m2 = Monomial.parse("12/13·x^2")
    try:
        m3 = m1 + m2
        assert False, "You are adding {m1} and {m2}, which is not possible"
    except AssertionError as e:
        raise(e)
    except Exception as e:
        print(f'He capturado la excepcion {e}')


def test_prod_monomial():
    m1 = Monomial.parse("2/3·x^5")
    m2 = Monomial.parse("3/5·x^3")
    m3 = m1 * m2
    assert m3 == Monomial.parse("2/5·x^8")

    m1 = Monomial.parse("0·x^5")
    m2 = Monomial.parse("12/13·x^2")
    m3 = m1 * m2
    assert m3 == Monomial.parse("0·x^0")

    print('OK')


def test_div():
    m1 = Monomial(Rational(1,2), 2)
    m2 = Monomial.parse("3/13·x^5")
    m3 = m2 / m1
    print(m3)
    assert m3 == Monomial.parse("6/13·x^3")

def pr_set_mon():
    m1 = Monomial(Rational(1,2), 2)
    m2 = Monomial.parse("3/13·x^5")
    m3 = m2 / m1
    a = {m1, m2, m3}

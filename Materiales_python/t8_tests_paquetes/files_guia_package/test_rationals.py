from ejemplo_paquete.rationals import Rational
import pytest


def test_rational_1():
    a = Rational(1, 2)
    b = Rational(2, 4)
    assert a == b, f'1/2 must be equal 1/4'
    print('OK')


@pytest.mark.parametrize(
    "s, expected",[
        ("1/2", Rational(1, 2)),
        ("3/6", Rational(1, 2)),
        ("-3/6", Rational(-1, 2)),
        ("3/-6", Rational(-1, 2)),
    ]
)

def test_parse(s, expected):
    assert Rational.parse(s) == expected


def test_hash():
    s = { Rational(1,1), Rational(1,2), Rational(1,3) }
    assert 1 in s
    assert 1.0 in s
    assert Rational(1,2) in s

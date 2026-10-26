
from ejemplo_paquete import rationals


def main():
    print("Hello from probar-paquete!")


if __name__ == "__main__":
    main()

    a = rationals.Rational(2, 3)                # __all__ = ["Rational"]
    r = rationals.gcd(4, 6)                         # __all__ = ["Rational"]
    print(a,r)


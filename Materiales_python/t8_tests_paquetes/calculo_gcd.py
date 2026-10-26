
'''
Module to compute the gcd
'''

def gcd(a: int, b :int) -> int:
    """
    Computes the gcd of a and b

    :return:
      the gcd

    :precondition:
      a > 0 and b>0

    :example:
    >>> a = 1
    >>> gcd(a, 2)
    1
    >>> gcd(48, 18)
    6
    >>> gcd(54, 24)
    6
    >>> gcd(7,0)
    Traceback (most recent call last):
      ...
    ValueError: The paameters should be greater than 0. a: 7, b:0
    """

    def gcd_rec(a: int, b: int) -> int:
        if b == 0:
            return a
        else:
            return gcd_rec(b, a % b)

    if a == 0 or b == 0:
        raise ValueError(f"The paameters should be greater than 0. a: {a}, b:{b}")
    return gcd_rec(a, b)


if __name__ == "__main__":
    # validación doctest
    import doctest
    doctest.testmod(verbose= True)


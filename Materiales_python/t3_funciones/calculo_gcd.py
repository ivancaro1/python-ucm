def gcd(a: float, b: int) -> int:
    """
    Calcula el máximo común divisor (MCD) de dos números enteros utilizando el algoritmo de Euclides.
    :param a: El primer número entero.
    :param b: El segundo número entero.
    :returns: El máximo común divisor de `a` y `b`.
    :raises ValueError: Si cualquiera de los dos números es negativo.
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
    ValueError: (False, 'b must be > 0')
    """
    while b != 0:
        r = a % b
        a = b
        b = r
    return a


def dividir_y_obtener_resto(dividendo: int, divisor: int) -> tuple[float, int, int]:
    """
    Calcula el cociente entero y el resto de la división entre dos números enteros.

    Args:
        dividendo (int): El número que se desea dividir.
        divisor (int): El número por el cual se divide el dividendo.

    Returns:
        tuple[float, int, float]: Una tupla donde el primer valor es el cociente y el segundo es el resto.
    """
    if divisor == 0:
        raise ValueError("El divisor no puede ser cero.")

    division = dividendo / divisor
    cociente = dividendo // divisor  # División entera
    resto = dividendo % divisor  # Resto de la división
    return float(division), cociente, resto





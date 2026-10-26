from typing import Final

class Matricula:
    PREFIJO: Final[str] = 'ES'

    def __init__(self, valor: int):
        # Accedemos al atributo de clase y lo incrementamos
        self.cod = f'{Matricula.PREFIJO}-{valor}'

    def __repr__(self):
        return self.cod

if __name__ == '__main__':
    a = Matricula(4587)
    print(a)
    Matricula.PREFIJO = 'IT'
    print(a)
"""Utilidades de dominio para Categorías.

Este módulo incluye ejemplos ejecutables en los docstrings (doctest) que
sirven como documentación viva y como prueba automática (ver
``tests/test_doctests.py``).
"""


def normalizar_nombre(nombre: str) -> str:
    """Normaliza el nombre de una categoría: recorta espacios y capitaliza.

    >>> normalizar_nombre('  tecnología ')
    'Tecnología'
    >>> normalizar_nombre('HOGAR')
    'Hogar'
    >>> normalizar_nombre('deportes y aire libre')
    'Deportes y aire libre'
    """
    return nombre.strip().capitalize()

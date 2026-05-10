"""
Funciones matemáticas de apoyo (sin dependencias de UI).
"""

MAX_ITERACIONES = 50   # límite de iteraciones del algoritmo


def redondear(numero: float, decimales: int = 4) -> float:
    """Redondea evitando errores de punto flotante."""
    factor = 10 ** decimales
    return round(numero * factor) / factor


def es_numero_valido(valor: str) -> bool:
    """Verifica que una cadena represente un número finito."""
    try:
        v = float(valor)
        return v == v and abs(v) != float("inf")   
    except (ValueError, TypeError):
        return False


def formatear_numero(numero: float) -> str:
    """Convierte un float a string eliminando ceros innecesarios."""
    r = redondear(numero)
    if r == int(r):
        return str(int(r))
    return str(r)

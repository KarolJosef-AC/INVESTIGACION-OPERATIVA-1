"""
Estructuras de datos puras que representan el estado
del algoritmo Simplex. No contienen lógica de UI ni de cálculo.
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ── Variable de la base ──────────────────────────────────────────
@dataclass
class VariableBase:
    nombre: str
    indice: int
    es_artificial: bool = False


# ── Restricción del problema ─────────────────────────────────────
@dataclass
class Restriccion:
    coeficientes: List[float]
    signo: str          
    limite: float


# ── Problema de programación lineal ─────────────────────────────
@dataclass
class Problema:
    tipo: str                   
    objetivo: List[float]
    restricciones: List[Restriccion]

    @property
    def cant_variables(self) -> int:
        return len(self.objetivo)

    @property
    def cant_restricciones(self) -> int:
        return len(self.restricciones)


# ── Snapshot de una iteración ────────────────────────────────────
@dataclass
class PasoSimplex:
    numero: int
    descripcion: str
    filas: List[List[float]]
    fila_z: List[float]
    fila_m: List[float]
    variables_en_base: List[VariableBase]
    hay_artificiales: bool
    columnas_eliminadas: List[int]
    columna_pivote: int = -1
    fila_pivote: int = -1


# ── Resultado completo del algoritmo ────────────────────────────
@dataclass
class ResultadoSimplex:
    pasos: List[PasoSimplex]
    valores_variables: List[float]
    valor_z: float
    cant_variables: int
    total_columnas: int
    variables_en_base_final: List[VariableBase]
    filas_final: List[List[float]]
    error: Optional[str] = None

    @property
    def exitoso(self) -> bool:
        return self.error is None

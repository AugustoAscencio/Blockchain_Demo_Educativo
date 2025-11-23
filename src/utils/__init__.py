"""
Paquete de utilidades.

Contiene funciones auxiliares y validadores:
- hash_utils: Funciones para cálculo de hashes SHA-256
- validators: Validadores con patrón Chain of Responsibility
"""

from .hash_utils import calcular_sha256, formatear_hash
from .validators import ValidadorTransaccion, ValidadorBloque, ValidadorCadena

__all__ = [
    "calcular_sha256",
    "formatear_hash",
    "ValidadorTransaccion",
    "ValidadorBloque",
    "ValidadorCadena",
]

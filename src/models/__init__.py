"""
Paquete de modelos de datos.

Contiene las clases principales del dominio de blockchain:
- Transaccion: Representa una transacción individual
- Bloque: Representa un bloque en la cadena
- CadenaDeBloques: Gestiona la cadena completa (Singleton)
"""

from .transaccion import Transaccion
from .bloque import Bloque
from .blockchain import CadenaDeBloques

__all__ = ["Transaccion", "Bloque", "CadenaDeBloques"]

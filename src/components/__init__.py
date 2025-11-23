"""
Paquete de componentes UI reutilizables.

Contiene componentes de interfaz de usuario:
- BloqueCard: Tarjeta visual para mostrar bloques
- Navigation: Barra de navegación lateral
"""

from .bloque_card import BloqueCard
from .navigation import crear_navegacion

__all__ = ["BloqueCard", "crear_navegacion"]

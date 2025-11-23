"""
Paquete de vistas de la aplicación.

Contiene las diferentes vistas de la interfaz:
- HomeView: Vista principal
- AgregarBloqueView: Formulario para agregar bloques
- VisualizarCadenaView: Visualización completa de la blockchain
"""

from .home_view import HomeView
from .agregar_bloque_view import AgregarBloqueView
from .visualizar_cadena_view import VisualizarCadenaView

__all__ = ["HomeView", "AgregarBloqueView", "VisualizarCadenaView"]

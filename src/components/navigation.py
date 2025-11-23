"""
Componente de Navegación.

Este módulo proporciona la barra de navegación lateral
para cambiar entre las diferentes vistas de la aplicación.
"""

import flet as ft
from typing import Callable


def crear_navegacion(
    on_cambio_vista: Callable[[int], None],
    indice_inicial: int = 0
) -> ft.NavigationRail:
    """
    Crea la barra de navegación lateral.
    
    Args:
        on_cambio_vista: Callback cuando cambia la vista seleccionada.
        indice_inicial: Índice de la vista inicial.
    
    Returns:
        NavigationRail configurado.
    
    Example:
        >>> nav = crear_navegacion(lambda idx: print(f"Vista {idx}"))
    """
    
    return ft.NavigationRail(
        selected_index=indice_inicial,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME,
                label="Inicio",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD_BOX_OUTLINED,
                selected_icon=ft.icons.ADD_BOX,
                label="Agregar",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.VIEW_LIST_OUTLINED,
                selected_icon=ft.icons.VIEW_LIST,
                label="Visualizar",
            ),
        ],
        on_change=lambda e: on_cambio_vista(e.control.selected_index),
        bgcolor=ft.colors.BLUE_GREY_900,
    )

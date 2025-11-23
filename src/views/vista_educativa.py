"""
Vista Educativa Principal.

Agrupa todos los componentes educativos en una vista con tabs para
facilitar la navegación entre conceptos.
"""

import flet as ft
from ..components.immutability_demo import crear_immutability_demo
from ..components.hash_link_visualizer import crear_hash_link_visualizer
from ..components.hash_table_education import crear_hash_table_education
from ..components.merkle_tree_visualizer import crear_merkle_tree_visualizer


def crear_vista_educativa(page: ft.Page = None) -> ft.Container:
    """
    Crea la vista educativa principal con tabs para cada concepto.
    
    Args:
        page: Página de Flet.
    
    Returns:
        Container con la vista educativa completa.
    """
    
    # Crear tabs para cada sección educativa
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Inmutabilidad",
                icon=ft.Icons.SHIELD,
                content=crear_immutability_demo(page)
            ),
            ft.Tab(
                text="Hashing como Enlace",
                icon=ft.Icons.LINK,
                content=crear_hash_link_visualizer(page=page)
            ),
            ft.Tab(
                text="Conexión con Hashing",
                icon=ft.Icons.SCHOOL,
                content=crear_hash_table_education(page)
            ),
            ft.Tab(
                text="Árbol de Merkle",
                icon=ft.Icons.ACCOUNT_TREE,
                content=crear_merkle_tree_visualizer(page)
            ),
        ],
        expand=True,
    )
    
    return ft.Container(
        content=ft.Column([
            # Encabezado
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, color="#26c6da", size=32),
                    ft.Column([
                        ft.Text(
                            "Centro Educativo Blockchain",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#26c6da"
                        ),
                        ft.Text(
                            "Aprende los conceptos fundamentales de la tecnología blockchain",
                            size=12,
                            color="#ffffff99"
                        ),
                    ], spacing=2),
                ], spacing=15),
                padding=20,
                bgcolor="#263238",
                border_radius=10,
            ),
            
            # Tabs con contenido educativo
            ft.Container(
                content=tabs,
                expand=True,
            ),
        ], spacing=15, expand=True),
        padding=20,
        expand=True
    )

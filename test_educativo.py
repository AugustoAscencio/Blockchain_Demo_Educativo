"""
Script de prueba para verificar los componentes educativos.
"""

import flet as ft
from src.components.immutability_demo import crear_immutability_demo
from src.components.hash_link_visualizer import crear_hash_link_visualizer  
from src.components.hash_table_education import crear_hash_table_education
from src.components.merkle_tree_visualizer import crear_merkle_tree_visualizer


def main(page: ft.Page):
    page.title = "Test Componentes Educativos"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1400
    page.window_height = 900
    page.bgcolor = "#0a1929"
    
    # Crear tabs de prueba
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Inmutabilidad",
                content=crear_immutability_demo(page)
            ),
            ft.Tab(
                text="Hash Link",
                content=crear_hash_link_visualizer(page=page)
            ),
            ft.Tab(
                text="Conexión",
                content=crear_hash_table_education(page)
            ),
            ft.Tab(
                text="Merkle Tree",
                content=crear_merkle_tree_visualizer(page)
            ),
        ],
        expand=True,
    )
    
    page.add(tabs)


if __name__ == "____main__":
    ft.app(target=main)

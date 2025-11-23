"""
Componente BloqueCard - Versión Simplificada.
"""

import flet as ft
import json
from typing import Dict, Any
from datetime import datetime
from ..utils.hash_utils import formatear_hash


def crear_bloque_card(datos_bloque: Dict[str, Any], es_valido: bool = True, page: ft.Page = None) -> ft.Container:
    """Crea una tarjeta visual para mostrar un bloque."""
    
    color_borde = "#66bb6a" if es_valido else "#ef5350"
    color_fondo = "#1a4d2e" if es_valido else "#4d1a1a"
    
    indice = datos_bloque.get("indice", 0)
    timestamp = datos_bloque.get("timestamp", "")
    hash_actual = datos_bloque.get("hash_actual", "")
    hash_previo = datos_bloque.get("hash_previo", "")
    datos = datos_bloque.get("datos", {})
    
    try:
        dt = datetime.fromisoformat(timestamp)
        timestamp_formateado = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        timestamp_formateado = timestamp
    
    datos_formateados = json.dumps(datos, indent=2, ensure_ascii=False)
    
    detalles_container = ft.Container(
        content=ft.Column([
            ft.Divider(height=1),
            ft.Text("Datos del Bloque:", size=12, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(datos_formateados, size=11, color="#80deea"),
                bgcolor="#00000042",
                padding=10,
                border_radius=5
            ),
            ft.Text("Hash Completo:", size=11, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(hash_actual, size=10, selectable=True),
                bgcolor="#00000042",
                padding=8,
                border_radius=5
            ),
            ft.Text("Hash Previo:", size=11, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(hash_previo, size=10, selectable=True),
                bgcolor="#00000042",
                padding=8,
                border_radius=5
            ),
        ], spacing=8),
        visible=False,
        animate_opacity=300,
    )
    
    def toggle_expandir(e):
        detalles_container.visible = not detalles_container.visible
        boton_expandir.icon = ft.Icons.EXPAND_LESS if detalles_container.visible else ft.Icons.EXPAND_MORE
        if page:
            page.update()
    
    boton_expandir = ft.IconButton(
        icon=ft.Icons.EXPAND_MORE,
        tooltip="Ver detalles",
        on_click=toggle_expandir
    )
    
    icono_validez = ft.Icon(
        name=ft.Icons.CHECK_CIRCLE if es_valido else ft.Icons.ERROR,
        color="#66bb6a" if es_valido else "#ef5350",
        size=20
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text(f"#{indice}", size=24, weight=ft.FontWeight.BOLD, color="#26c6da"),
                    width=60
                ),
                ft.Column([
                    ft.Text(f"Bloque {indice}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(timestamp_formateado, size=11, color="#ffffff99"),
                ], spacing=2, expand=True),
                icono_validez,
                boton_expandir,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Column([
                    ft.Text("Hash:", size=10, color="#ffffff99"),
                    ft.Text(formatear_hash(hash_actual, 16), size=11, color="#4dd0e1"),
                ], spacing=2),
                ft.Icon(ft.Icons.ARROW_BACK, size=16),
                ft.Column([
                    ft.Text("Previo:", size=10, color="#ffffff99"),
                    ft.Text(formatear_hash(hash_previo, 16), size=11, color="#ffb74d"),
                ], spacing=2),
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            detalles_container,
        ], spacing=10),
        padding=15,
        border=ft.border.all(2, color_borde),
        border_radius=10,
        bgcolor=color_fondo,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
    )


class BloqueCard:
    """Wrapper para compatibilidad."""
    
    def __init__(self, datos_bloque: Dict[str, Any], es_valido: bool = True):
        self.datos_bloque = datos_bloque
        self.es_valido = es_valido
        self.page = None
    
    def build(self):
        return crear_bloque_card(self.datos_bloque, self.es_valido, self.page)

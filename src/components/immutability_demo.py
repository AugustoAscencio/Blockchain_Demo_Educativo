"""
Componente de Demostración de Inmutabilidad.

Este componente muestra visualmente cómo un cambio mínimo en los datos
produce un hash SHA-256 completamente diferente, demostrando el principio
de inmutabilidad en blockchain.
"""

import flet as ft
from typing import Callable
from ..utils.hash_utils import calcular_sha256


def crear_immutability_demo(page: ft.Page = None) -> ft.Container:
    """
    Crea una demostración interactiva de inmutabilidad.
    
    Args:
        page: Página de Flet (opcional).
    
    Returns:
        Container con la demostración de inmutabilidad.
    """
    
    # Estados
    texto_original = ft.Ref[ft.TextField]()
    texto_modificado = ft.Ref[ft.TextField]()
    hash_original_display = ft.Ref[ft.Text]()
    hash_modificado_display = ft.Ref[ft.Text]()
    mensaje_diferencia = ft.Ref[ft.Container]()
    
    def actualizar_hash_original(e):
        """Actualiza el hash cuando cambia el texto original."""
        texto = texto_original.current.value or ""
        hash_value = calcular_sha256(texto)
        hash_original_display.current.value = hash_value
        
        # Comparar con hash modificado
        comparar_hashes()
        
        if page:
            page.update()
    
    def actualizar_hash_modificado(e):
        """Actualiza el hash cuando cambia el texto modificado."""
        texto = texto_modificado.current.value or ""
        hash_value = calcular_sha256(texto)
        hash_modificado_display.current.value = hash_value
        
        # Comparar con hash original
        comparar_hashes()
        
        if page:
            page.update()
    
    def comparar_hashes():
        """Compara los dos hashes y muestra el resultado."""
        hash_orig = hash_original_display.current.value
        hash_mod = hash_modificado_display.current.value
        
        if not hash_orig or not hash_mod:
            mensaje_diferencia.current.visible = False
            return
        
        son_iguales = hash_orig == hash_mod
        
        if son_iguales:
            mensaje_diferencia.current.content = ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#66bb6a", size=24),
                ft.Text(
                    "Los hashes son idénticos (datos iguales)",
                    size=14,
                    color="#66bb6a",
                    weight=ft.FontWeight.BOLD
                )
            ], spacing=10)
            mensaje_diferencia.current.bgcolor = "#1b5e20"
        else:
            mensaje_diferencia.current.content = ft.Row([
                ft.Icon(ft.Icons.WARNING, color="#ffa726", size=24),
                ft.Text(
                    "¡Los hashes son completamente diferentes! (inmutabilidad demostrada)",
                    size=14,
                    color="#ffa726",
                    weight=ft.FontWeight.BOLD
                )
            ], spacing=10)
            mensaje_diferencia.current.bgcolor = "#e65100"
        
        mensaje_diferencia.current.visible = True
    
    def copiar_a_modificado(e):
        """Copia el texto original al campo modificado."""
        texto_modificado.current.value = texto_original.current.value
        actualizar_hash_modificado(None)
        if page:
            page.update()
    
    def resetear(e):
        """Resetea todos los campos."""
        texto_original.current.value = ""
        texto_modificado.current.value = ""
        hash_original_display.current.value = "Escribe algo en el campo de arriba..."
        hash_modificado_display.current.value = "Escribe algo en el campo de arriba..."
        mensaje_diferencia.current.visible = False
        if page:
            page.update()
    
    # Construir UI
    return ft.Container(
        content=ft.Column([
            # Título y descripción
            ft.Row([
                ft.Icon(ft.Icons.SHIELD, color="#26c6da", size=32),
                ft.Text(
                    "Demostración de Inmutabilidad",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#26c6da"
                ),
            ], spacing=10),
            
            ft.Text(
                "Modifica el texto y observa cómo un cambio mínimo produce un hash SHA-256 completamente diferente.",
                size=13,
                color="#ffffff99"
            ),
            
            ft.Divider(height=20),
            
            # Sección Original
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            "📄 Datos Originales",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#4dd0e1"
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CONTENT_COPY,
                            tooltip="Copiar al lado modificado",
                            icon_color="#4dd0e1",
                            on_click=copiar_a_modificado
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.TextField(
                        ref=texto_original,
                        label="Escribe tu texto aquí",
                        hint_text="Ejemplo: Hola Mundo",
                        multiline=True,
                        min_lines=2,
                        max_lines=3,
                        on_change=actualizar_hash_original,
                        border_color="#4dd0e1",
                    ),
                    
                    ft.Text("Hash SHA-256:", size=12, color="#ffffff99"),
                    ft.Container(
                        content=ft.Text(
                            ref=hash_original_display,
                            value="Escribe algo en el campo de arriba...",
                            size=11,
                            selectable=True,
                            color="#4dd0e1"
                        ),
                        bgcolor="#00000042",
                        padding=10,
                        border_radius=5,
                        border=ft.border.all(1, "#4dd0e1")
                    ),
                ], spacing=10),
                padding=15,
                bgcolor="#0d47a1",
                border_radius=10,
                border=ft.border.all(2, "#4dd0e1")
            ),
            
            # Sección Modificada
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "✏️ Datos Modificados",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#ffb74d"
                    ),
                    
                    ft.TextField(
                        ref=texto_modificado,
                        label="Modifica el texto aquí",
                        hint_text="Cambia una letra y observa...",
                        multiline=True,
                        min_lines=2,
                        max_lines=3,
                        on_change=actualizar_hash_modificado,
                        border_color="#ffb74d",
                    ),
                    
                    ft.Text("Hash SHA-256:", size=12, color="#ffffff99"),
                    ft.Container(
                        content=ft.Text(
                            ref=hash_modificado_display,
                            value="Escribe algo en el campo de arriba...",
                            size=11,
                            selectable=True,
                            color="#ffb74d"
                        ),
                        bgcolor="#00000042",
                        padding=10,
                        border_radius=5,
                        border=ft.border.all(1, "#ffb74d")
                    ),
                ], spacing=10),
                padding=15,
                bgcolor="#e65100",
                border_radius=10,
                border=ft.border.all(2, "#ffb74d")
            ),
            
            # Mensaje de comparación
            ft.Container(
                ref=mensaje_diferencia,
                visible=False,
                padding=15,
                border_radius=10,
                animate_opacity=300
            ),
            
            # Botones de acción
            ft.Row([
                ft.ElevatedButton(
                    "Resetear",
                    icon=ft.Icons.REFRESH,
                    on_click=resetear
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            # Explicación educativa
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "💡 ¿Qué es la Inmutabilidad?",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#26c6da"
                    ),
                    ft.Text(
                        "• La función hash SHA-256 es determinística: los mismos datos siempre producen el mismo hash",
                        size=12
                    ),
                    ft.Text(
                        "• Un cambio mínimo (incluso una letra) produce un hash completamente diferente",
                        size=12
                    ),
                    ft.Text(
                        "• En blockchain, esto garantiza que cualquier modificación de datos sea inmediatamente detectable",
                        size=12
                    ),
                    ft.Text(
                        "• Es matemáticamente imposible modificar un bloque sin cambiar su hash",
                        size=12
                    ),
                ], spacing=8),
                padding=15,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(1, "#26c6da")
            ),
            
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

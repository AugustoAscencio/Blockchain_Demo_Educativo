"""
Componente de Visualización de Enlaces Hash.

Muestra visualmente cómo los bloques están conectados mediante hashing,
donde el hash de un bloque se convierte en el hash_previo del siguiente bloque.
"""

import flet as ft
from typing import List, Dict, Any


def crear_hash_link_visualizer(
    bloques_ejemplo: List[Dict[str, Any]] = None,
    page: ft.Page = None
) -> ft.Container:
    """
    Crea un visualizador de enlaces hash entre bloques.
    
    Args:
        bloques_ejemplo: Lista de bloques a visualizar (opcional).
        page: Página de Flet (opcional).
    
    Returns:
        Container con la visualización de enlaces hash.
    """
    
    # Bloques de ejemplo si no se proporcionan
    if bloques_ejemplo is None:
        bloques_ejemplo = [
            {
                "indice": 0,
                "hash_actual": "a1b2c3d4e5f6...",
                "hash_previo": "0",
                "datos": {"mensaje": "Bloque Génesis"}
            },
            {
                "indice": 1,
                "hash_actual": "f6e5d4c3b2a1...",
                "hash_previo": "a1b2c3d4e5f6...",
                "datos": {"transaccion": "Alice → Bob: 10"}
            },
            {
                "indice": 2,
                "hash_actual": "9z8y7x6w5v4u...",
                "hash_previo": "f6e5d4c3b2a1...",
                "datos": {"transaccion": "Bob → Carlos: 5"}
            }
        ]
    
    def crear_bloque_visual(bloque: Dict[str, Any], es_ultimo: bool = False) -> ft.Container:
        """Crea la representación visual de un bloque."""
        indice = bloque.get("indice", 0)
        hash_actual = bloque.get("hash_actual", "")
        hash_previo = bloque.get("hash_previo", "")
        datos = bloque.get("datos", {})
        
        # Formatear hash para visualización
        hash_corto_actual = hash_actual[:16] if len(hash_actual) > 16 else hash_actual
        hash_corto_previo = hash_previo[:16] if len(hash_previo) > 16 else hash_previo
        
        # Obtener descripción de datos
        datos_str = ""
        if "mensaje" in datos:
            datos_str = datos["mensaje"]
        elif "transaccion" in datos:
            datos_str = datos["transaccion"]
        else:
            datos_str = str(datos)[:30] + "..."
        
        bloque_container = ft.Container(
            content=ft.Column([
                # Encabezado del bloque
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FOLDER, color="#26c6da", size=20),
                        ft.Text(
                            f"Bloque #{indice}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#26c6da"
                        ),
                    ], spacing=8),
                    padding=10,
                    bgcolor="#1a237e",
                    border_radius=ft.border_radius.only(top_left=10, top_right=10)
                ),
                
                # Contenido del bloque
                ft.Container(
                    content=ft.Column([
                        # Datos
                        ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION, size=16, color="#80deea"),
                            ft.Text("Datos:", size=11, color="#ffffff99"),
                        ], spacing=5),
                        ft.Text(datos_str, size=12, color="#80deea"),
                        
                        ft.Divider(height=10, color="#ffffff1f"),
                        
                        # Hash Previo
                        ft.Row([
                            ft.Icon(ft.Icons.INPUT, size=16, color="#ffb74d"),
                            ft.Text("Hash Previo:", size=11, color="#ffffff99"),
                        ], spacing=5),
                        ft.Container(
                            content=ft.Text(
                                hash_corto_previo,
                                size=10,
                                color="#ffb74d",
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor="#00000042",
                            padding=8,
                            border_radius=5,
                            border=ft.border.all(1, "#ffb74d")
                        ),
                        
                        ft.Divider(height=10, color="#ffffff1f"),
                        
                        # Hash Actual
                        ft.Row([
                            ft.Icon(ft.Icons.TAG, size=16, color="#4dd0e1"),
                            ft.Text("Hash Actual:", size=11, color="#ffffff99"),
                        ], spacing=5),
                        ft.Container(
                            content=ft.Text(
                                hash_corto_actual,
                                size=10,
                                color="#4dd0e1",
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor="#00000042",
                            padding=8,
                            border_radius=5,
                            border=ft.border.all(1, "#4dd0e1")
                        ),
                    ], spacing=8),
                    padding=15,
                    bgcolor="#263238",
                ),
            ], spacing=0),
            width=250,
            border=ft.border.all(2, "#26c6da"),
            border_radius=10,
        )
        
        # Si no es el último bloque, agregar flecha de conexión
        if not es_ultimo:
            return ft.Row([
                bloque_container,
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ARROW_FORWARD, color="#66bb6a", size=32),
                        ft.Container(
                            content=ft.Text(
                                "ENLACE\nVERIFICABLE",
                                size=9,
                                text_align=ft.TextAlign.CENTER,
                                color="#66bb6a",
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor="#1b5e20",
                            padding=5,
                            border_radius=5
                        ),
                        ft.Text(
                            "Hash A →\nHash Previo B",
                            size=8,
                            text_align=ft.TextAlign.CENTER,
                            color="#ffffff99"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=80,
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=0)
        else:
            return bloque_container
    
    # Crear visualización de bloques
    bloques_visuales = []
    for i, bloque in enumerate(bloques_ejemplo):
        es_ultimo = (i == len(bloques_ejemplo) - 1)
        bloque_visual = crear_bloque_visual(bloque, es_ultimo)
        bloques_visuales.append(bloque_visual)
    
    return ft.Container(
        content=ft.Column([
            # Título y descripción
            ft.Row([
                ft.Icon(ft.Icons.LINK, color="#26c6da", size=32),
                ft.Text(
                    "El Hashing como Enlace Inmutable",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#26c6da"
                ),
            ], spacing=10),
            
            ft.Text(
                "Cada bloque contiene el hash del bloque anterior, creando una cadena inmutable y verificable.",
                size=13,
                color="#ffffff99"
            ),
            
            ft.Divider(height=20),
            
            # Visualización de bloques conectados
            ft.Container(
                content=ft.Row(
                    bloques_visuales,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor="#0a1929",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#26c6da")
            ),
            
            # Explicación del proceso
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🔗 ¿Cómo Funciona el Enlace?",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#26c6da"
                    ),
                    
                    ft.Row([
                        ft.Container(
                            content=ft.Text("1", size=20, weight=ft.FontWeight.BOLD),
                            width=40,
                            height=40,
                            bgcolor="#1a237e",
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Text(
                                "El Bloque A calcula su hash usando sus datos",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Hash A = SHA256(índice + timestamp + datos + hash_previo)",
                                size=11,
                                color="#80deea"
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=10),
                    
                    ft.Row([
                        ft.Container(
                            content=ft.Text("2", size=20, weight=ft.FontWeight.BOLD),
                            width=40,
                            height=40,
                            bgcolor="#1a237e",
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Text(
                                "El Hash A se inserta en el Bloque B",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Bloque B.hash_previo = Hash A (puntero verificable)",
                                size=11,
                                color="#ffb74d"
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=10),
                    
                    ft.Row([
                        ft.Container(
                            content=ft.Text("3", size=20, weight=ft.FontWeight.BOLD),
                            width=40,
                            height=40,
                            bgcolor="#1a237e",
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Text(
                                "Cualquier modificación en A cambia su hash",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Esto rompe el enlace con B, haciendo detectable cualquier alteración",
                                size=11,
                                color="#ef5350"
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=10),
                    
                ], spacing=15),
                padding=20,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(1, "#26c6da")
            ),
            
            # Punto clave
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB, color="#ffd54f", size=24),
                    ft.Column([
                        ft.Text(
                            "Punto Clave: Inmutabilidad en Cadena",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#ffd54f"
                        ),
                        ft.Text(
                            "Si alguien modifica el Bloque A, su hash cambia. Esto invalida el hash_previo del Bloque B, "
                            "rompiendo la cadena. Para ocultar el cambio, el atacante tendría que recalcular todos los "
                            "bloques posteriores, lo cual es computacionalmente inviable en una blockchain real.",
                            size=12,
                        ),
                    ], spacing=5, expand=True),
                ], spacing=15),
                padding=15,
                bgcolor="#f57f17",
                border_radius=10,
            ),
            
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

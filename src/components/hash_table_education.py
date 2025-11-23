"""
Componente Educativo de Conexión Hash.

Explica la conexión entre el uso de hashing en blockchain y en tablas de dispersión,
mostrando cómo el mismo principio matemático se usa con propósitos diferentes.
"""

import flet as ft


def crear_hash_table_education(page: ft.Page = None) -> ft.Container:
    """
    Crea un panel educativo sobre la conexión entre hashing en blockchain y tablas hash.
    
    Args:
        page: Página de Flet (opcional).
    
    Returns:
        Container con contenido educativo.
    """
    
    return ft.Container(
        content=ft.Column([
            # Título
            ft.Row([
                ft.Icon(ft.Icons.SCHOOL, color="#26c6da", size=32),
                ft.Text(
                    "Conexión con la Unidad de HASHING",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#26c6da"
                ),
            ], spacing=10),
            
            ft.Text(
                "El mismo principio matemático (SHA-256) con propósitos diferentes: eficiencia vs. seguridad",
                size=13,
                color="#ffffff99"
            ),
            
            ft.Divider(height=20),
            
            # El Principio Común
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.FUNCTIONS, color="#ffd54f", size=28),
                        ft.Text(
                            "El Principio Común: Función Hash",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#ffd54f"
                        ),
                    ], spacing=10),
                    
                    ft.Text(
                        "Una función hash es una operación matemática que convierte datos de entrada de cualquier "
                        "tamaño en una cadena de longitud fija. Tanto las tablas de dispersión como blockchain "
                        "utilizan este concepto fundamental.",
                        size=13,
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Entrada (cualquier tamaño)", size=12, text_align=ft.TextAlign.CENTER),
                            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20),
                            ft.Container(
                                content=ft.Text(
                                    "FUNCIÓN HASH\n(SHA-256)",
                                    size=12,
                                    text_align=ft.TextAlign.CENTER,
                                    weight=ft.FontWeight.BOLD
                                ),
                                bgcolor="#1a237e",
                                padding=15,
                                border_radius=10,
                                border=ft.border.all(2, "#26c6da")
                            ),
                            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20),
                            ft.Text("Salida (256 bits / 64 caracteres hex)", size=12, text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor="#0a1929",
                        border_radius=10
                    ),
                ], spacing=15),
                padding=20,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(2, "#ffd54f")
            ),
            
            # Comparación lado a lado
            ft.Text(
                "Comparación: Dos Aplicaciones, Un Principio",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#26c6da"
            ),
            
            ft.Row([
                # Tabla Hash
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.GRID_ON, color="#4dd0e1", size=24),
                                ft.Text(
                                    "TABLAS DE DISPERSIÓN\n(Hash Tables)",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#4dd0e1",
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor="#0d47a1",
                            padding=15,
                            border_radius=ft.border_radius.only(top_left=10, top_right=10)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.FLAG, color="#4dd0e1", size=18),
                                    ft.Text("Propósito:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "Almacenamiento y búsqueda eficiente de datos",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Row([
                                    ft.Icon(ft.Icons.SPEED, color="#4dd0e1", size=18),
                                    ft.Text("Objetivo:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "Dispersión uniforme para minimizar colisiones y acceso O(1)",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Row([
                                    ft.Icon(ft.Icons.BUILD, color="#4dd0e1", size=18),
                                    ft.Text("Uso:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "• Índice para ubicar datos\n"
                                    "• Búsqueda rápida: clave → valor\n"
                                    "• Optimización de rendimiento",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Ejemplo:", size=11, weight=ft.FontWeight.BOLD, color="#4dd0e1"),
                                        ft.Text(
                                            'hash("Juan") → índice 42\n'
                                            'tabla[42] = datos de Juan',
                                            size=10,
                                            color="#80deea"
                                        ),
                                    ], spacing=5),
                                    bgcolor="#00000042",
                                    padding=10,
                                    border_radius=5
                                ),
                            ], spacing=8),
                            padding=15,
                            bgcolor="#263238",
                        ),
                    ], spacing=0),
                    border=ft.border.all(2, "#4dd0e1"),
                    border_radius=10,
                    expand=1
                ),
                
                # Blockchain
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.LINK, color="#66bb6a", size=24),
                                ft.Text(
                                    "BLOCKCHAIN",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#66bb6a",
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor="#1b5e20",
                            padding=15,
                            border_radius=ft.border_radius.only(top_left=10, top_right=10)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.FLAG, color="#66bb6a", size=18),
                                    ft.Text("Propósito:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "Integridad y seguridad de registros",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Row([
                                    ft.Icon(ft.Icons.SECURITY, color="#66bb6a", size=18),
                                    ft.Text("Objetivo:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "Inmutabilidad y detección de alteraciones",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Row([
                                    ft.Icon(ft.Icons.BUILD, color="#66bb6a", size=18),
                                    ft.Text("Uso:", size=12, weight=ft.FontWeight.BOLD),
                                ], spacing=5),
                                ft.Text(
                                    "• Huella digital del bloque\n"
                                    "• Enlace verificable entre bloques\n"
                                    "• Garantía de no modificación",
                                    size=11,
                                    color="#ffffff99"
                                ),
                                
                                ft.Divider(height=10),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Ejemplo:", size=11, weight=ft.FontWeight.BOLD, color="#66bb6a"),
                                        ft.Text(
                                            'hash(Bloque 1) → a1b2c3...\n'
                                            'Bloque 2.hash_previo = a1b2c3...',
                                            size=10,
                                            color="#a5d6a7"
                                        ),
                                    ], spacing=5),
                                    bgcolor="#00000042",
                                    padding=10,
                                    border_radius=5
                                ),
                            ], spacing=8),
                            padding=15,
                            bgcolor="#263238",
                        ),
                    ], spacing=0),
                    border=ft.border.all(2, "#66bb6a"),
                    border_radius=10,
                    expand=1
                ),
            ], spacing=15),
            
            # Resumen clave
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PSYCHOLOGY, color="#ab47bc", size=24),
                        ft.Text(
                            "Principio Matemático Común, Aplicaciones Diferentes",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#ab47bc"
                        ),
                    ], spacing=10),
                    
                    ft.Text(
                        "✓ Ambos usan funciones hash (ej: SHA-256) que convierten datos en valores de longitud fija",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Tablas Hash: enfoque en EFICIENCIA (dispersión para búsqueda rápida)",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Blockchain: enfoque en SEGURIDAD (inmutabilidad y confianza)",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Las propiedades de las funciones hash (determinismo, avalancha) son cruciales en ambos casos",
                        size=12,
                    ),
                ], spacing=10),
                padding=20,
                bgcolor="#4a148c",
                border_radius=10,
                border=ft.border.all(2, "#ab47bc")
            ),
            
            # Confianza y Registros
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.VERIFIED_USER, color="#26c6da", size=24),
                        ft.Text(
                            "¿Cómo Resuelve Blockchain el Problema de Confianza?",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#26c6da"
                        ),
                    ], spacing=10),
                    
                    ft.Text(
                        "En sistemas tradicionales, confiamos en una autoridad central (banco, gobierno) para mantener "
                        "registros íntegros. Blockchain elimina esa necesidad usando matemáticas:",
                        size=12,
                    ),
                    
                    ft.Column([
                        ft.Row([
                            ft.Text("1️⃣", size=18),
                            ft.Text(
                                "Cada bloque tiene una huella digital (hash) única",
                                size=12,
                                expand=True
                            ),
                        ], spacing=10),
                        
                        ft.Row([
                            ft.Text("2️⃣", size=18),
                            ft.Text(
                                "Los bloques están enlazados: modificar uno invalida todos los siguientes",
                                size=12,
                                expand=True
                            ),
                        ], spacing=10),
                        
                        ft.Row([
                            ft.Text("3️⃣", size=18),
                            ft.Text(
                                "La verificación es pública: cualquiera puede validar la integridad",
                                size=12,
                                expand=True
                            ),
                        ], spacing=10),
                        
                        ft.Row([
                            ft.Text("4️⃣", size=18),
                            ft.Text(
                                "Resultado: confianza sin intermediarios, basada en matemáticas",
                                size=12,
                                expand=True
                            ),
                        ], spacing=10),
                    ], spacing=8),
                ], spacing=12),
                padding=20,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(1, "#26c6da")
            ),
            
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

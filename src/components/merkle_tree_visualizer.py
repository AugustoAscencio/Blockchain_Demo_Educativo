"""
Componente de Visualización de Merkle Tree.

Muestra visualmente cómo funciona un Árbol de Merkle y cómo permite
verificar rápidamente una transacción sin leer todos los registros.
"""

import flet as ft
from typing import List, Dict, Any
from ..utils.hash_utils import calcular_sha256


def crear_merkle_tree_visualizer(page: ft.Page = None) -> ft.Container:
    """
    Crea un visualizador interactivo del Árbol de Merkle.
    
    Args:
        page: Página de Flet (opcional).
    
    Returns:
        Container con la visualización del Merkle Tree.
    """
    
    # Transacciones de ejemplo
    transacciones = [
        "Alice → Bob: 10 BTC",
        "Carlos → Diana: 5 BTC",
        "Eva → Frank: 3 BTC",
        "Grace → Hugo: 7 BTC",
    ]
    
    # Calcular hashes de las transacciones (hojas)
    hojas_hashes = [calcular_sha256(tx) for tx in transacciones]
    
    # Calcular nivel intermedio (parejas de hojas)
    nivel_1_hashes = []
    for i in range(0, len(hojas_hashes), 2):
        if i + 1 < len(hojas_hashes):
            hash_combinado = calcular_sha256(hojas_hashes[i] + hojas_hashes[i + 1])
        else:
            hash_combinado = hojas_hashes[i]  # Si es impar, se duplica
        nivel_1_hashes.append(hash_combinado)
    
    # Calcular raíz (hash de los hashes del nivel 1)
    if len(nivel_1_hashes) >= 2:
        raiz_merkle = calcular_sha256(nivel_1_hashes[0] + nivel_1_hashes[1])
    else:
        raiz_merkle = nivel_1_hashes[0] if nivel_1_hashes else calcular_sha256("")
    
    # Estado de la verificación
    transaccion_seleccionada = ft.Ref[ft.Dropdown]()
    
    def formatear_hash(hash_str: str, longitud: int = 12) -> str:
        """Formatea un hash para visualización."""
        return hash_str[:longitud] + "..." if len(hash_str) > longitud else hash_str
    
    def crear_nodo_merkle(
        hash_value: str,
        label: str,
        color: str = "#26c6da",
        width: int = 160,
        resaltado: bool = False
    ) -> ft.Container:
        """Crea un nodo visual del Merkle Tree."""
        border_color = "#ffd54f" if resaltado else color
        border_width = 3 if resaltado else 2
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    label,
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    content=ft.Text(
                        formatear_hash(hash_value),
                        size=9,
                        color="#ffffff",
                        text_align=ft.TextAlign.CENTER
                    ),
                    bgcolor="#00000042",
                    padding=8,
                    border_radius=5
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=width,
            padding=10,
            bgcolor="#263238",
            border=ft.border.all(border_width, border_color),
            border_radius=10,
        )
    
    def crear_arbol_visual(indice_verificar: int = -1) -> ft.Column:
        """Crea la visualización del árbol, opcionalmente resaltando un camino."""
        
        # Determinar qué nodos resaltar
        nodos_a_resaltar = set()
        if indice_verificar >= 0:
            # Hoja
            nodos_a_resaltar.add(f"hoja_{indice_verificar}")
            
            # Nivel 1 (pareja)
            indice_nivel1 = indice_verificar // 2
            nodos_a_resaltar.add(f"nivel1_{indice_nivel1}")
            
            # Raíz
            nodos_a_resaltar.add("raiz")
        
        # Crear visualización del árbol
        return ft.Column([
            # Nivel 0: Raíz Merkle
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🌳 RAÍZ MERKLE",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#66bb6a",
                        text_align=ft.TextAlign.CENTER
                    ),
                    crear_nodo_merkle(
                        raiz_merkle,
                        "Raíz",
                        "#66bb6a",
                        200,
                        "raiz" in nodos_a_resaltar
                    ),
                    ft.Text(
                        "(Se almacena en el encabezado del bloque)",
                        size=10,
                        color="#ffffff99",
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=10
            ),
            
            # Conectores
            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=24, color="#66bb6a"),
            
            # Nivel 1: Nodos intermedios
            ft.Row([
                ft.Column([
                    crear_nodo_merkle(
                        nivel_1_hashes[0],
                        "Hash(H0+H1)",
                        "#4dd0e1",
                        160,
                        "nivel1_0" in nodos_a_resaltar
                    ),
                    ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Column([
                    crear_nodo_merkle(
                        nivel_1_hashes[1],
                        "Hash(H2+H3)",
                        "#4dd0e1",
                        160,
                        "nivel1_1" in nodos_a_resaltar
                    ),
                    ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
            
            # Nivel 2: Hojas (Transacciones)
            ft.Row([
                ft.Column([
                    crear_nodo_merkle(
                        hojas_hashes[0],
                        f"H0: {transacciones[0][:15]}...",
                        "#ffb74d",
                        160,
                        "hoja_0" in nodos_a_resaltar
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Column([
                    crear_nodo_merkle(
                        hojas_hashes[1],
                        f"H1: {transacciones[1][:15]}...",
                        "#ffb74d",
                        160,
                        "hoja_1" in nodos_a_resaltar
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Column([
                    crear_nodo_merkle(
                        hojas_hashes[2],
                        f"H2: {transacciones[2][:15]}...",
                        "#ffb74d",
                        160,
                        "hoja_2" in nodos_a_resaltar
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Column([
                    crear_nodo_merkle(
                        hojas_hashes[3],
                        f"H3: {transacciones[3][:15]}...",
                        "#ffb74d",
                        160,
                        "hoja_3" in nodos_a_resaltar
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    # Contenedor para el árbol visual (se actualizará dinámicamente)
    contenedor_arbol = ft.Container(
        content=crear_arbol_visual(),
        padding=20,
    )
    
    def verificar_transaccion(e):
        """Simula la verificación de una transacción en el Merkle Tree."""
        if not transaccion_seleccionada.current.value:
            return
        
        indice = int(transaccion_seleccionada.current.value)
        
        # Actualizar visualización con nodos resaltados
        contenedor_arbol.content = crear_arbol_visual(indice_verificar=indice)
        
        if page:
            page.update()
    
    return ft.Container(
        content=ft.Column([
            # Título
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_TREE, color="#26c6da", size=32),
                ft.Text(
                    "Árbol de Merkle: Verificación Eficiente",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#26c6da"
                ),
            ], spacing=10),
            
            ft.Text(
                "Un Merkle Tree permite verificar una transacción específica sin leer todas las demás del bloque.",
                size=13,
                color="#ffffff99"
            ),
            
            ft.Divider(height=20),
            
            # Visualización del árbol
            ft.Container(
                content=ft.Column([
                    contenedor_arbol,
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor="#0a1929",
                padding=20,
                border_radius=10,
                border=ft.border.all(2, "#26c6da")
            ),
            
            # Panel de verificación
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🔍 Verificar una Transacción",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#ffd54f"
                    ),
                    
                    ft.Row([
                        ft.Dropdown(
                            ref=transaccion_seleccionada,
                            label="Selecciona una transacción",
                            options=[
                                ft.dropdown.Option(str(i), f"{i}: {tx}")
                                for i, tx in enumerate(transacciones)
                            ],
                            width=300,
                        ),
                        ft.ElevatedButton(
                            "Verificar",
                            icon=ft.Icons.SEARCH,
                            on_click=verificar_transaccion,
                            bgcolor="#ffd54f",
                            color="#000000"
                        ),
                    ], spacing=10),
                    
                    ft.Text(
                        "Los nodos resaltados en amarillo muestran el camino de verificación mínimo.",
                        size=11,
                        color="#ffffff99"
                    ),
                ], spacing=10),
                padding=15,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(1, "#ffd54f")
            ),
            
            # Explicación
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📚 ¿Cómo Funciona?",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#26c6da"
                    ),
                    
                    ft.Text(
                        "Verificación Tradicional (sin Merkle Tree):",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#ef5350"
                    ),
                    ft.Text(
                        "• Necesitas leer TODAS las transacciones del bloque secuencialmente\n"
                        "• Si un bloque tiene 1000 transacciones, debes leer las 1000\n"
                        "• Complejidad: O(n) - lento e ineficiente",
                        size=11,
                        color="#ffffff99"
                    ),
                    
                    ft.Divider(height=10),
                    
                    ft.Text(
                        "Verificación con Merkle Tree:",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#66bb6a"
                    ),
                    ft.Text(
                        "• Solo necesitas el hash de tu transacción + algunos hashes hermanos\n"
                        "• Para 1000 transacciones, solo necesitas ~10 hashes (log₂ 1000)\n"
                        "• Complejidad: O(log n) - ¡mucho más rápido!\n"
                        "• Reconstruyes el camino hasta la raíz y verificas con el hash del bloque",
                        size=11,
                        color="#ffffff99"
                    ),
                    
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.SPEED, color="#4dd0e1", size=24),
                        ft.Column([
                            ft.Text(
                                "Ejemplo Práctico",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color="#4dd0e1"
                            ),
                            ft.Text(
                                "Para verificar si 'Alice → Bob: 10 BTC' está en el bloque:\n"
                                "1. Obtienes H0 (hash de tu transacción)\n"
                                "2. Obtienes H1 (hash del hermano)\n"
                                "3. Calculas Hash(H0+H1) y comparas con el nodo intermedio\n"
                                "4. Obtienes el otro nodo intermedio Hash(H2+H3)\n"
                                "5. Calculas la raíz y comparas con el hash del bloque\n"
                                "✅ ¡Verificado con solo 3 hashes en lugar de 4 transacciones!",
                                size=11,
                                color="#ffffff99"
                            ),
                        ], spacing=5, expand=True),
                    ], spacing=10),
                    
                ], spacing=12),
                padding=20,
                bgcolor="#263238",
                border_radius=10,
                border=ft.border.all(1, "#26c6da")
            ),
            
            # Beneficios
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB, color="#ffd54f", size=24),
                        ft.Text(
                            "Beneficios del Merkle Tree en Blockchain",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#ffd54f"
                        ),
                    ], spacing=10),
                    
                    ft.Text(
                        "✓ Verificación eficiente: O(log n) en lugar de O(n)",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Ahorro de ancho de banda: no necesitas descargar todas las transacciones",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Ideal para SPV (Simplified Payment Verification) en billeteras móviles",
                        size=12,
                    ),
                    ft.Text(
                        "✓ La raíz Merkle en el encabezado del bloque resume todas las transacciones",
                        size=12,
                    ),
                    ft.Text(
                        "✓ Detecta inmediatamente si alguna transacción fue modificada",
                        size=12,
                    ),
                ], spacing=8),
                padding=15,
                bgcolor="#f57f17",
                border_radius=10,
            ),
            
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    )

"""
Componente Educativo de Agregar Bloques.

Este componente combina la funcionalidad de agregar bloques con interfaces
educativas que muestran paso a paso cómo se crea, hashea y conecta un bloque
nuevo a la cadena.
"""

import flet as ft
from typing import Optional
from ..utils.hash_utils import calcular_sha256
from ..controllers.blockchain_controller import BlockchainController
import json
from datetime import datetime


def crear_agregar_bloque_educativo(page: ft.Page, controller: BlockchainController) -> ft.Container:
    """
    Crea una vista educativa para agregar bloques.
    
    Args:
        page: Página de Flet.
        controller: Controlador de blockchain.
    
    Returns:
        Container con la vista educativa de agregar bloques.
    """
    
    # Referencias a componentes
    campo_emisor = ft.Ref[ft.TextField]()
    campo_receptor = ft.Ref[ft.TextField]()
    campo_cantidad = ft.Ref[ft.TextField]()
    campo_descripcion = ft.Ref[ft.TextField]()
    
    # Visualización de datos
    datos_display = ft.Ref[ft.Text]()
    hash_display = ft.Ref[ft.Text]()
    hash_previo_display = ft.Ref[ft.Text]()
    indice_display = ft.Ref[ft.Text]()
    timestamp_display = ft.Ref[ft.Text]()
    
    # Contenedores de pasos
    paso1_container = ft.Ref[ft.Container]()
    paso2_container = ft.Ref[ft.Container]()
    paso3_container = ft.Ref[ft.Container]()
    paso4_container = ft.Ref[ft.Container]()
    
    mensaje_resultado = ft.Ref[ft.Container]()
    
    def actualizar_preview(e=None):
        """Actualiza la preview de los datos en tiempo real."""
        if not campo_emisor.current.value or not campo_receptor.current.value or not campo_cantidad.current.value:
            datos_display.current.value = "Completa el formulario para ver la preview..."
            datos_display.current.color = "#ffffff66"
            hash_display.current.value = "---"
            
            # Deshabilitar pasos 2, 3, 4
            paso2_container.current.opacity = 0.3
            paso3_container.current.opacity = 0.3
            paso4_container.current.opacity = 0.3
            
            if page:
                page.update()
            return
        
        try:
            # Activar visualización
            paso2_container.current.opacity = 1.0
            paso3_container.current.opacity = 1.0
            paso4_container.current.opacity = 1.0
            
            # Preparar datos
            transaccion = {
                "emisor": campo_emisor.current.value,
                "receptor": campo_receptor.current.value,
                "cantidad": float(campo_cantidad.current.value),
                "descripcion": campo_descripcion.current.value or ""
            }
            
            # Obtener información actual de la blockchain
            stats = controller.obtener_estadisticas()
            cadena = controller.obtener_cadena_completa()
            
            indice = stats.get("total_bloques", 0)
            hash_previo = cadena[-1].get("hash_actual", "0") if cadena else "0"
            timestamp = datetime.now().isoformat()
            
            # Actualizar displays
            datos_display.current.value = json.dumps(transaccion, indent=2, ensure_ascii=False)
            datos_display.current.color = "#4dd0e1"
            
            indice_display.current.value = str(indice)
            timestamp_display.current.value = timestamp
            hash_previo_display.current.value = hash_previo
            
            # Calcular hash simulado
            datos_para_hash = f"{indice}{timestamp}{json.dumps(transaccion)}{hash_previo}"
            hash_calculado = calcular_sha256(datos_para_hash)
            hash_display.current.value = hash_calculado
            
            if page:
                page.update()
                
        except ValueError:
            datos_display.current.value = "❌ La cantidad debe ser un número válido"
            datos_display.current.color = "#ef5350"
            hash_display.current.value = "---"
            
            paso2_container.current.opacity = 0.3
            paso3_container.current.opacity = 0.3
            paso4_container.current.opacity = 0.3
            
            if page:
                page.update()
    
    def agregar_bloque_con_educacion(e):
        """Agrega el bloque y muestra el resultado educativo."""
        mensaje_resultado.current.visible = False
        
        if not campo_emisor.current.value or not campo_receptor.current.value or not campo_cantidad.current.value:
            mensaje_resultado.current.content = ft.Row([
                ft.Icon(ft.Icons.ERROR, color="#ef5350", size=24),
                ft.Text("Todos los campos son obligatorios", color="#ef5350", weight=ft.FontWeight.BOLD)
            ], spacing=10)
            mensaje_resultado.current.bgcolor = "#b71c1c"
            mensaje_resultado.current.visible = True
            page.update()
            return
        
        try:
            cantidad = float(campo_cantidad.current.value)
            exito, mensaje = controller.agregar_bloque_con_transaccion(
                emisor=campo_emisor.current.value,
                receptor=campo_receptor.current.value,
                cantidad=cantidad,
                descripcion=campo_descripcion.current.value or ""
            )
            
            if exito:
                mensaje_resultado.current.content = ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="#66bb6a", size=32),
                        ft.Text("¡Bloque agregado exitosamente!", size=16, color="#66bb6a", weight=ft.FontWeight.BOLD)
                    ], spacing=10),
                    ft.Text(mensaje, size=12, color="#ffffff99"),
                    ft.Divider(height=10),
                    ft.Text("💡 El bloque se agregó a la cadena con:", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"   • Índice: {indice_display.current.value}", size=11),
                    ft.Text(f"   • Hash: {hash_display.current.value[:32]}...", size=11),
                    ft.Text(f"   • Conectado al bloque anterior mediante su hash", size=11),
                ], spacing=5, tight=True)
                mensaje_resultado.current.bgcolor = "#1b5e20"
                
                # Limpiar formulario
                campo_emisor.current.value = ""
                campo_receptor.current.value = ""
                campo_cantidad.current.value = ""
                campo_descripcion.current.value = ""
                
                # Actualizar preview
                actualizar_preview()
            else:
                mensaje_resultado.current.content = ft.Row([
                    ft.Icon(ft.Icons.ERROR, color="#ef5350", size=24),
                    ft.Text(mensaje, color="#ef5350", weight=ft.FontWeight.BOLD)
                ], spacing=10)
                mensaje_resultado.current.bgcolor = "#b71c1c"
            
            mensaje_resultado.current.visible = True
            page.update()
            
        except ValueError:
            mensaje_resultado.current.content = ft.Row([
                ft.Icon(ft.Icons.ERROR, color="#ef5350", size=24),
                ft.Text("La cantidad debe ser un número válido", color="#ef5350", weight=ft.FontWeight.BOLD)
            ], spacing=10)
            mensaje_resultado.current.bgcolor = "#b71c1c"
            mensaje_resultado.current.visible = True
            page.update()
    
    def resetear(e):
        """Resetea el formulario."""
        campo_emisor.current.value = ""
        campo_receptor.current.value = ""
        campo_cantidad.current.value = ""
        campo_descripcion.current.value = ""
        mensaje_resultado.current.visible = False
        actualizar_preview()
    
    # Construir UI
    return ft.Container(
        content=ft.Column([
            # Encabezado
            ft.Row([
                ft.Icon(ft.Icons.ADD_BOX, color="#26c6da", size=32),
                ft.Column([
                    ft.Text(
                        "Vista Educativa: Agregar Bloque",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#26c6da"
                    ),
                    ft.Text(
                        "Observa cómo se crea un bloque paso a paso mientras llenas el formulario",
                        size=12,
                        color="#ffffff99"
                    ),
                ], spacing=2),
            ], spacing=15),
            
            ft.Divider(height=20),
            
            # Contenedor principal con dos columnas
            ft.Row([
                # Columna izquierda: Formulario
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Paso 1: Ingresa los Datos de la Transacción", size=16, weight=ft.FontWeight.BOLD, color="#4dd0e1"),
                        
                        ft.TextField(
                            ref=campo_emisor,
                            label="Emisor",
                            hint_text="Nombre del emisor",
                            border_color="#4dd0e1",
                            on_change=actualizar_preview
                        ),
                        ft.TextField(
                            ref=campo_receptor,
                            label="Receptor",
                            hint_text="Nombre del receptor",
                            border_color="#4dd0e1",
                            on_change=actualizar_preview
                        ),
                        ft.TextField(
                            ref=campo_cantidad,
                            label="Cantidad",
                            hint_text="Monto a transferir",
                            keyboard_type=ft.KeyboardType.NUMBER,
                            border_color="#4dd0e1",
                            on_change=actualizar_preview
                        ),
                        ft.TextField(
                            ref=campo_descripcion,
                            label="Descripción (opcional)",
                            hint_text="Información adicional",
                            multiline=True,
                            max_lines=2,
                            border_color="#4dd0e1",
                            on_change=actualizar_preview
                        ),
                        
                        ft.Divider(),
                        
                        ft.Text("📄 Datos de la Transacción:", size=12, color="#ffffff99"),
                        ft.Container(
                            content=ft.Text(
                                ref=datos_display,
                                value="Completa el formulario para ver la preview...",
                                size=11,
                                selectable=True,
                                color="#ffffff66"
                            ),
                            bgcolor="#00000042",
                            padding=10,
                            border_radius=5,
                            border=ft.border.all(1, "#4dd0e1")
                        ),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Agregar Bloque a la Cadena",
                                icon=ft.Icons.ADD_BOX,
                                on_click=agregar_bloque_con_educacion
                            ),
                            ft.ElevatedButton(
                                "Resetear",
                                icon=ft.Icons.REFRESH,
                                on_click=resetear
                            ),
                        ], spacing=10),
                        
                        ft.Container(
                            ref=mensaje_resultado,
                            visible=False,
                            padding=15,
                            border_radius=10,
                        ),
                        
                    ], spacing=15, scroll=ft.ScrollMode.AUTO),
                    expand=1,
                    padding=20,
                    bgcolor="#263238",
                    border_radius=10,
                    border=ft.border.all(2, "#4dd0e1")
                ),
                
                # Columna derecha: Visualización educativa
                ft.Container(
                    content=ft.Column([
                        ft.Text("🎓 Proceso de Creación del Bloque", size=16, weight=ft.FontWeight.BOLD, color="#ffb74d"),
                        
                        # Paso 2: Metadatos
                        ft.Container(
                            ref=paso2_container,
                            content=ft.Column([
                                ft.Text("⚙️ Paso 2: Metadatos del Bloque", size=14, weight=ft.FontWeight.BOLD, color="#ffb74d"),
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Índice:", size=11, color="#ffffff99"),
                                        ft.Text(ref=indice_display, value="0", size=14, weight=ft.FontWeight.BOLD, color="#ffb74d"),
                                    ], spacing=2),
                                    ft.Column([
                                        ft.Text("Timestamp:", size=11, color="#ffffff99"),
                                        ft.Text(ref=timestamp_display, value="---", size=10, color="#ffb74d"),
                                    ], spacing=2),
                                ], spacing=20),
                            ], spacing=8),
                            padding=12,
                            bgcolor="#4a148c",
                            border_radius=8,
                            border=ft.border.all(1, "#ffb74d"),
                            opacity=0.3
                        ),
                        
                        # Paso 3: Hash previo
                        ft.Container(
                            ref=paso3_container,
                            content=ft.Column([
                                ft.Text("🔗 Paso 3: Conexión con Bloque Anterior", size=14, weight=ft.FontWeight.BOLD, color="#a5d6a7"),
                                ft.Text("Hash del bloque anterior:", size=11, color="#ffffff99"),
                                ft.Container(
                                    content=ft.Text(
                                        ref=hash_previo_display,
                                        value="0",
                                        size=10,
                                        selectable=True,
                                        color="#a5d6a7"
                                    ),
                                    bgcolor="#00000042",
                                    padding=8,
                                    border_radius=5,
                                    border=ft.border.all(1, "#a5d6a7")
                                ),
                                ft.Text("💡 Este hash conecta el nuevo bloque con la cadena existente", size=10, italic=True),
                            ], spacing=8),
                            padding=12,
                            bgcolor="#1b5e20",
                            border_radius=8,
                            border=ft.border.all(1, "#a5d6a7"),
                            opacity=0.3
                        ),
                        
                        # Paso 4: Hash final
                        ft.Container(
                            ref=paso4_container,
                            content=ft.Column([
                                ft.Text("🔐 Paso 4: Cálculo del Hash SHA-256", size=14, weight=ft.FontWeight.BOLD, color="#ef9a9a"),
                                ft.Text("Hash del nuevo bloque:", size=11, color="#ffffff99"),
                                ft.Container(
                                    content=ft.Text(
                                        ref=hash_display,
                                        value="---",
                                        size=10,
                                        selectable=True,
                                        color="#ef9a9a"
                                    ),
                                    bgcolor="#00000042",
                                    padding=8,
                                    border_radius=5,
                                    border=ft.border.all(1, "#ef9a9a")
                                ),
                                ft.Text("💡 Este hash se calcula a partir de todos los datos anteriores", size=10, italic=True),
                            ], spacing=8),
                            padding=12,
                            bgcolor="#b71c1c",
                            border_radius=8,
                            border=ft.border.all(1, "#ef9a9a"),
                            opacity=0.3
                        ),
                        
                        # Explicación educativa
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    "💡 ¿Cómo se crea un bloque?",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color="#26c6da"
                                ),
                                ft.Text("1. Se recopilan los datos de la transacción", size=11),
                                ft.Text("2. Se agregan metadatos (índice, timestamp)", size=11),
                                ft.Text("3. Se obtiene el hash del bloque anterior", size=11),
                                ft.Text("4. Se calcula el hash SHA-256 del nuevo bloque", size=11),
                                ft.Text("5. El bloque se conecta a la cadena", size=11),
                            ], spacing=6),
                            padding=12,
                            bgcolor="#263238",
                            border_radius=8,
                            border=ft.border.all(1, "#26c6da")
                        ),
                        
                    ], spacing=15, scroll=ft.ScrollMode.AUTO),
                    expand=1,
                    padding=20,
                    bgcolor="#263238",
                    border_radius=10,
                    border=ft.border.all(2, "#ffb74d")
                ),
            ], spacing=15, expand=True),
            
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True),
        padding=20,
        expand=True
    )

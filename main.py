"""
Aplicación Principal de Blockchain Demo - Versión Simplificada.
"""

import flet as ft
import logging
from src.controllers.blockchain_controller import BlockchainController
from src.components.bloque_card import crear_bloque_card
from src.models.bloque import Bloque
from src.views.vista_educativa import crear_vista_educativa
from src.components.agregar_bloque_educativo import crear_agregar_bloque_educativo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    page.title = "Blockchain Demo"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1400
    page.window_height = 900
    page.bgcolor = "#0a1929"
    
    logger.info("Aplicación iniciada")
    
    controller = BlockchainController()
    
    # Componentes
    lista_bloques = ft.ListView(spacing=10, padding=20, expand=True)
    total_bloques_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    estado_validez_text = ft.Text("Válida", size=16, color="#66bb6a")
    
    def actualizar_vista():
        stats = controller.obtener_estadisticas()
        total_bloques_text.value = str(stats.get("total_bloques", 0))
        es_valida = stats.get("es_valida", True)
        estado_validez_text.value = "Válida" if es_valida else "Inválida"
        estado_validez_text.color = "#66bb6a" if es_valida else "#ef5350"
        
        cadena = controller.obtener_cadena_completa()
        lista_bloques.controls.clear()
        es_cadena_valida, _ = controller.validar_cadena()
        
        for bloque_dict in reversed(cadena):
            bloque = Bloque.from_dict(bloque_dict)
            es_valido = bloque.validar() and es_cadena_valida
            card = crear_bloque_card(bloque_dict, es_valido=es_valido, page=page)
            lista_bloques.controls.append(card)
        
        page.update()
    
    controller.agregar_observador(actualizar_vista)
    
    # Formulario
    campo_emisor = ft.TextField(label="Emisor", hint_text="Nombre")
    campo_receptor = ft.TextField(label="Receptor", hint_text="Nombre")
    campo_cantidad = ft.TextField(label="Cantidad", hint_text="Monto", keyboard_type=ft.KeyboardType.NUMBER)
    campo_descripcion = ft.TextField(label="Descripción", multiline=True, max_lines=2)
    mensaje_agregar = ft.Container(visible=False, padding=10, border_radius=5)
    
    def agregar_bloque(e):
        mensaje_agregar.visible = False
        if not campo_emisor.value or not campo_receptor.value or not campo_cantidad.value:
            mensaje_agregar.content = ft.Text("Todos los campos son obligatorios", color="#ef5350")
            mensaje_agregar.bgcolor = "#b71c1c"
            mensaje_agregar.visible = True
            page.update()
            return
        
        try:
            cantidad = float(campo_cantidad.value)
            exito, mensaje = controller.agregar_bloque_con_transaccion(
                emisor=campo_emisor.value,
                receptor=campo_receptor.value,
                cantidad=cantidad,
                descripcion=campo_descripcion.value or ""
            )
            
            if exito:
                mensaje_agregar.content = ft.Text(mensaje, color="#66bb6a")
                mensaje_agregar.bgcolor = "#1b5e20"
                campo_emisor.value = ""
                campo_receptor.value = ""
                campo_cantidad.value = ""
                campo_descripcion.value = ""
            else:
                mensaje_agregar.content = ft.Text(mensaje, color="#ef5350")
                mensaje_agregar.bgcolor = "#b71c1c"
            
            mensaje_agregar.visible = True
            page.update()
        except ValueError:
            mensaje_agregar.content = ft.Text("La cantidad debe ser un número", color="#ef5350")
            mensaje_agregar.bgcolor = "#b71c1c"
            mensaje_agregar.visible = True
            page.update()
    
    # Diálogos
    def validar_cadena(e):
        es_valida, mensaje = controller.validar_cadena()
        texto = "✅ La cadena es válida" if es_valida else f"❌ Inválida: {mensaje}"
        dlg = ft.AlertDialog(
            title=ft.Text("Validación"),
            content=ft.Text(texto),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: cerrar_dlg(dlg))],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def simular_ataque_dlg(e):
        stats = controller.obtener_estadisticas()
        total_bloques = stats.get("total_bloques", 0)
        
        # Campo de índice con información
        campo_indice = ft.TextField(
            label="Índice del bloque a modificar",
            hint_text=f"0 a {total_bloques - 1}",
            keyboard_type=ft.KeyboardType.NUMBER,
            helper_text=f"Bloques disponibles: {total_bloques}"
        )
        
        mensaje_error = ft.Container(visible=False, padding=10, border_radius=5)
        
        def simular(e):
            mensaje_error.visible = False
            
            # Validar que hay bloques
            if total_bloques <= 1:
                mensaje_error.content = ft.Row([
                    ft.Icon(ft.Icons.ERROR, color="#ef5350", size=20),
                    ft.Text("Necesitas al menos 2 bloques para simular un ataque", color="#ef5350", size=12)
                ], spacing=10)
                mensaje_error.bgcolor = "#b71c1c"
                mensaje_error.visible = True
                page.update()
                return
            
            # Validar entrada
            if not campo_indice.value:
                campo_indice.error_text = "Ingresa un índice"
                page.update()
                return
            
            try:
                indice = int(campo_indice.value)
                
                # Validar rango
                if indice < 0 or indice >= total_bloques:
                    campo_indice.error_text = f"Índice debe estar entre 0 y {total_bloques - 1}"
                    page.update()
                    return
                
                # Obtener datos del bloque antes del ataque
                cadena_antes = controller.obtener_cadena_completa()
                bloque_antes = cadena_antes[indice] if indice < len(cadena_antes) else None
                
                # Simular ataque
                exito, mensaje = controller.simular_ataque(indice)
                dlg_ataque.open = False
                page.update()
                
                # Obtener datos después del ataque
                cadena_despues = controller.obtener_cadena_completa()
                bloque_despues = cadena_despues[indice] if indice < len(cadena_despues) else None
                
                # Crear diálogo de resultado mejorado
                contenido_resultado = ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.WARNING, color="#ffa726", size=32),
                        ft.Text(mensaje, size=14, weight=ft.FontWeight.BOLD, color="#ffa726")
                    ], spacing=10),
                    
                    ft.Divider(),
                    
                    ft.Text("📊 Comparación:", size=14, weight=ft.FontWeight.BOLD, color="#26c6da"),
                    
                    # Antes
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ANTES del ataque:", size=12, weight=ft.FontWeight.BOLD, color="#66bb6a"),
                            ft.Text(f"Datos: {bloque_antes.get('datos', {})}", size=11),
                            ft.Text(f"Hash: {bloque_antes.get('hash_actual', '')[:32]}...", size=10, color="#4dd0e1"),
                        ], spacing=4),
                        padding=10,
                        bgcolor="#1b5e20",
                        border_radius=8,
                        border=ft.border.all(1, "#66bb6a")
                    ),
                    
                    ft.Icon(ft.Icons.ARROW_DOWNWARD, color="#ffa726", size=24),
                    
                    # Después
                    ft.Container(
                        content=ft.Column([
                            ft.Text("DESPUÉS del ataque:", size=12, weight=ft.FontWeight.BOLD, color="#ef5350"),
                            ft.Text(f"Datos: {bloque_despues.get('datos', {})}", size=11),
                            ft.Text(f"Hash: {bloque_despues.get('hash_actual', '')[:32]}...", size=10, color="#ef5350"),
                        ], spacing=4),
                        padding=10,
                        bgcolor="#b71c1c",
                        border_radius=8,
                        border=ft.border.all(1, "#ef5350")
                    ),
                    
                    ft.Divider(),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("💡 ¿Qué pasó?", size=12, weight=ft.FontWeight.BOLD, color="#26c6da"),
                            ft.Text("• Los datos del bloque fueron modificados", size=11),
                            ft.Text("• El hash NO fue recalculado (simulando un ataque)", size=11),
                            ft.Text("• La cadena ahora es INVÁLIDA", size=11),
                            ft.Text("• Usa 'Validar Cadena' para verificar la corrupción", size=11),
                        ], spacing=4),
                        padding=10,
                        bgcolor="#263238",
                        border_radius=8,
                        border=ft.border.all(1, "#26c6da")
                    ),
                ], spacing=12, scroll=ft.ScrollMode.AUTO)
                
                dlg_resultado = ft.AlertDialog(
                    title=ft.Text("⚠️ Ataque Simulado"),
                    content=contenido_resultado,
                    actions=[
                        ft.TextButton("Ver en Inicio", on_click=lambda _: (cerrar_dlg(dlg_resultado), cambiar_a_inicio())),
                        ft.TextButton("Cerrar", on_click=lambda _: cerrar_dlg(dlg_resultado)),
                    ],
                )
                page.dialog = dlg_resultado
                dlg_resultado.open = True
                page.update()
                
            except ValueError:
                campo_indice.error_text = "Debe ser un número entero"
                page.update()
        
        def cambiar_a_inicio():
            """Cambia a la vista de inicio para ver el resultado."""
            navegacion.selected_index = 0
            contenedor_vista.content = vista_home
            actualizar_vista()
        
        dlg_ataque = ft.AlertDialog(
            title=ft.Text("⚠️ Simular Ataque a la Blockchain"),
            content=ft.Column([
                ft.Text(
                    "Esta acción modificará los datos de un bloque sin recalcular su hash, "
                    "demostrando cómo se detecta la manipulación.",
                    size=12
                ),
                ft.Divider(),
                campo_indice,
                mensaje_error,
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: cerrar_dlg(dlg_ataque)),
                ft.ElevatedButton("💣 Simular Ataque", on_click=simular, bgcolor="#e65100", color="#ffffff"),
            ],
        )
        page.dialog = dlg_ataque
        dlg_ataque.open = True
        page.update()
    
    def cerrar_dlg(dlg):
        dlg.open = False
        page.update()
    
    # Vistas
    vista_home = ft.Column([
        ft.Text("Blockchain Demo", size=28, weight=ft.FontWeight.BOLD, color="#26c6da"),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LAYERS, size=40, color="#26c6da"),
                    total_bloques_text,
                    ft.Text("Bloques", size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=1, padding=20, border_radius=10, bgcolor="#263238",
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.VERIFIED, size=40, color="#66bb6a"),
                    estado_validez_text,
                    ft.Text("Estado", size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=1, padding=20, border_radius=10, bgcolor="#263238",
            ),
        ], spacing=15),
        ft.Row([
            ft.ElevatedButton("Validar Cadena", icon=ft.Icons.CHECK_CIRCLE, on_click=validar_cadena),
            ft.ElevatedButton("Simular Ataque", icon=ft.Icons.WARNING, on_click=simular_ataque_dlg),
        ], spacing=10),
        ft.Divider(),
        ft.Text("Bloques en la Cadena", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(content=lista_bloques, expand=True, border=ft.border.all(1, "#ffffff3d"), border_radius=10),
    ], spacing=10, expand=True)
    
    vista_agregar = ft.Column([
        ft.Text("Agregar Nuevo Bloque", size=28, weight=ft.FontWeight.BOLD, color="#26c6da"),
        ft.Container(
            content=ft.Column([
                ft.Text("Nueva Transacción", size=20, weight=ft.FontWeight.BOLD, color="#26c6da"),
                campo_emisor,
                campo_receptor,
                campo_cantidad,
                campo_descripcion,
                mensaje_agregar,
                ft.ElevatedButton("Agregar Bloque", icon=ft.Icons.ADD_BOX, on_click=agregar_bloque),
            ], spacing=15),
            padding=30,
            border=ft.border.all(2, "#0097a7"),
            border_radius=15,
            bgcolor="#263238",
        ),
    ], spacing=20, expand=True)
    
    vista_educativa_container = crear_vista_educativa(page)
    vista_agregar_educativo_container = crear_agregar_bloque_educativo(page, controller)
    
    contenedor_vista = ft.Container(content=vista_home, expand=True, padding=20)
    
    def cambiar_vista(e):
        indice = e.control.selected_index
        if indice == 0:
            contenedor_vista.content = vista_home
            actualizar_vista()
        elif indice == 1:
            contenedor_vista.content = vista_agregar
        elif indice == 2:
            contenedor_vista.content = vista_agregar_educativo_container
        elif indice == 3:
            contenedor_vista.content = vista_educativa_container
        page.update()
    
    navegacion = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.ADD_BOX_OUTLINED, selected_icon=ft.Icons.ADD_BOX, label="Agregar"),
            ft.NavigationRailDestination(icon=ft.Icons.SCIENCE_OUTLINED, selected_icon=ft.Icons.SCIENCE, label="Agregar (Edu)"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL_OUTLINED, selected_icon=ft.Icons.SCHOOL, label="Educación"),
        ],
        on_change=cambiar_vista,
        bgcolor="#263238",
    )
    
    page.appbar = ft.AppBar(
        title=ft.Row([
            ft.Icon(ft.Icons.LINK, color="#26c6da"),
            ft.Text("Blockchain Demo", size=20, weight=ft.FontWeight.BOLD, color="#26c6da"),
        ]),
        bgcolor="#263238",
    )
    
    page.add(ft.Row([navegacion, ft.VerticalDivider(width=1), contenedor_vista], expand=True, spacing=0))
    
    actualizar_vista()
    logger.info("Interfaz cargada")


if __name__ == "__main__":
    ft.app(target=main)

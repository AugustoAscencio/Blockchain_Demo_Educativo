"""
Aplicación Principal de Blockchain Demo - Versión Simplificada.
"""

import flet as ft
import logging
from src.controllers.blockchain_controller import BlockchainController
from src.components.bloque_card import crear_bloque_card
from src.models.bloque import Bloque
from src.views.vista_educativa import crear_vista_educativa

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
        campo_indice = ft.TextField(label="Índice del bloque", keyboard_type=ft.KeyboardType.NUMBER)
        
        def simular(e):
            try:
                indice = int(campo_indice.value)
                exito, mensaje = controller.simular_ataque(indice)
                dlg_ataque.open = False
                page.update()
                dlg_resultado = ft.AlertDialog(
                    title=ft.Text("Ataque Simulado"),
                    content=ft.Text(mensaje),
                    actions=[ft.TextButton("Cerrar", on_click=lambda _: cerrar_dlg(dlg_resultado))],
                )
                page.dialog = dlg_resultado
                dlg_resultado.open = True
                page.update()
            except ValueError:
                campo_indice.error_text = "Número inválido"
                page.update()
        
        dlg_ataque = ft.AlertDialog(
            title=ft.Text("Simular Ataque"),
            content=ft.Column([
                ft.Text("Modificará un bloque para demostrar inmutabilidad"),
                campo_indice,
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: cerrar_dlg(dlg_ataque)),
                ft.TextButton("Simular", on_click=simular),
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
    
    contenedor_vista = ft.Container(content=vista_home, expand=True, padding=20)
    
    def cambiar_vista(e):
        indice = e.control.selected_index
        if indice == 0:
            contenedor_vista.content = vista_home
            actualizar_vista()
        elif indice == 1:
            contenedor_vista.content = vista_agregar
        elif indice == 2:
            contenedor_vista.content = vista_educativa_container
        page.update()
    
    navegacion = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.ADD_BOX_OUTLINED, selected_icon=ft.Icons.ADD_BOX, label="Agregar"),
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

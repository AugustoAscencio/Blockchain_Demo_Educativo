"""
Vista de Agregar Bloque.

Este módulo define la vista con el formulario para agregar
nuevos bloques a la blockchain.
"""

import flet as ft
from typing import Optional
from ..controllers.blockchain_controller import BlockchainController


class AgregarBloqueView(ft.UserControl):
    """
    Vista para agregar nuevos bloques a la blockchain.
    
    Proporciona un formulario para ingresar datos de transacciones
    y agregarlas como nuevos bloques.
    
    Attributes:
        controller: Controlador de la blockchain.
        on_navegar: Callback para navegar a otras vistas.
    """
    
    def __init__(
        self,
        controller: BlockchainController,
        on_navegar: Optional[callable] = None
    ):
        """
        Inicializa la vista de agregar bloque.
        
        Args:
            controller: Controlador de la blockchain.
            on_navegar: Callback para navegación.
        """
        super().__init__()
        self.controller = controller
        self.on_navegar = on_navegar
    
    def build(self):
        """Construye la vista de agregar bloque."""
        # Campos del formulario
        self.campo_emisor = ft.TextField(
            label="Emisor",
            hint_text="Nombre o dirección del emisor",
            prefix_icon=ft.icons.PERSON,
            border_color=ft.colors.CYAN_700,
            focused_border_color=ft.colors.CYAN_400,
        )
        
        self.campo_receptor = ft.TextField(
            label="Receptor",
            hint_text="Nombre o dirección del receptor",
            prefix_icon=ft.icons.PERSON_OUTLINE,
            border_color=ft.colors.CYAN_700,
            focused_border_color=ft.colors.CYAN_400,
        )
        
        self.campo_cantidad = ft.TextField(
            label="Cantidad",
            hint_text="Monto a transferir",
            prefix_icon=ft.icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.colors.CYAN_700,
            focused_border_color=ft.colors.CYAN_400,
        )
        
        self.campo_descripcion = ft.TextField(
            label="Descripción (opcional)",
            hint_text="Descripción de la transacción",
            prefix_icon=ft.icons.DESCRIPTION,
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_color=ft.colors.CYAN_700,
            focused_border_color=ft.colors.CYAN_400,
        )
        
        # Barra de progreso
        self.barra_progreso = ft.ProgressBar(
            visible=False,
            color=ft.colors.CYAN_400,
        )
        
        # Mensaje de resultado
        self.mensaje_resultado = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_400),
                ft.Text("", size=14),
            ]),
            visible=False,
            padding=10,
            border_radius=5,
            bgcolor=ft.colors.GREEN_900,
        )
        
        # Botones
        botones = ft.Row([
            ft.ElevatedButton(
                "Agregar Bloque",
                icon=ft.icons.ADD_BOX,
                on_click=self._agregar_bloque,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.CYAN_700,
                    color=ft.colors.WHITE,
                ),
            ),
            ft.OutlinedButton(
                "Limpiar Formulario",
                icon=ft.icons.CLEAR,
                on_click=self._limpiar_formulario,
            ),
            ft.OutlinedButton(
                "Ver Blockchain",
                icon=ft.icons.VIEW_LIST,
                on_click=lambda _: self.on_navegar(0) if self.on_navegar else None,
            ),
        ], spacing=10)
        
        # Formulario
        formulario = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Nueva Transacción",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.CYAN_400
                ),
                ft.Divider(height=20),
                self.campo_emisor,
                self.campo_receptor,
                self.campo_cantidad,
                self.campo_descripcion,
                self.barra_progreso,
                self.mensaje_resultado,
                ft.Divider(height=20),
                botones,
            ], spacing=15),
            padding=30,
            border=ft.border.all(2, ft.colors.CYAN_700),
            border_radius=15,
            bgcolor=ft.colors.BLUE_GREY_900,
        )
        
        # Información adicional
        info_panel = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.CYAN_400, size=30),
                    ft.Text(
                        "Información",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.CYAN_400
                    ),
                ]),
                ft.Divider(height=10),
                ft.Text(
                    "• Cada transacción se almacena en un nuevo bloque",
                    size=13,
                ),
                ft.Text(
                    "• El bloque se enlaza criptográficamente con el anterior",
                    size=13,
                ),
                ft.Text(
                    "• Los datos son inmutables una vez agregados",
                    size=13,
                ),
                ft.Text(
                    "• Todos los campos excepto descripción son obligatorios",
                    size=13,
                ),
            ], spacing=10),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.BLUE_GREY_800,
        )
        
        # Layout principal
        return ft.Column([
            ft.Text(
                "Agregar Nuevo Bloque",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            ft.Row([
                ft.Container(
                    content=formulario,
                    expand=2,
                ),
                ft.Container(
                    content=info_panel,
                    expand=1,
                ),
            ], spacing=20, expand=True),
        ], spacing=20, expand=True)
    
    def _agregar_bloque(self, e):
        """Agrega un nuevo bloque con los datos del formulario."""
        # Limpiar mensajes anteriores
        self.mensaje_resultado.visible = False
        self._limpiar_errores()
        
        # Validar campos
        if not self._validar_formulario():
            self.update()
            return
        
        # Mostrar progreso
        self.barra_progreso.visible = True
        self.update()
        
        # Agregar bloque
        try:
            cantidad = float(self.campo_cantidad.value)
            
            exito, mensaje = self.controller.agregar_bloque_con_transaccion(
                emisor=self.campo_emisor.value,
                receptor=self.campo_receptor.value,
                cantidad=cantidad,
                descripcion=self.campo_descripcion.value or ""
            )
            
            # Ocultar progreso
            self.barra_progreso.visible = False
            
            # Mostrar resultado
            if exito:
                self._mostrar_exito(mensaje)
                self._limpiar_formulario(None)
            else:
                self._mostrar_error(mensaje)
            
        except ValueError:
            self.barra_progreso.visible = False
            self._mostrar_error("La cantidad debe ser un número válido")
        
        self.update()
    
    def _validar_formulario(self) -> bool:
        """
        Valida los campos del formulario.
        
        Returns:
            True si el formulario es válido, False en caso contrario.
        """
        es_valido = True
        
        if not self.campo_emisor.value:
            self.campo_emisor.error_text = "El emisor es obligatorio"
            es_valido = False
        
        if not self.campo_receptor.value:
            self.campo_receptor.error_text = "El receptor es obligatorio"
            es_valido = False
        
        if not self.campo_cantidad.value:
            self.campo_cantidad.error_text = "La cantidad es obligatoria"
            es_valido = False
        else:
            try:
                cantidad = float(self.campo_cantidad.value)
                if cantidad <= 0:
                    self.campo_cantidad.error_text = "La cantidad debe ser mayor a cero"
                    es_valido = False
            except ValueError:
                self.campo_cantidad.error_text = "Ingrese un número válido"
                es_valido = False
        
        return es_valido
    
    def _limpiar_errores(self):
        """Limpia los mensajes de error de los campos."""
        self.campo_emisor.error_text = None
        self.campo_receptor.error_text = None
        self.campo_cantidad.error_text = None
        self.campo_descripcion.error_text = None
    
    def _limpiar_formulario(self, e):
        """Limpia todos los campos del formulario."""
        self.campo_emisor.value = ""
        self.campo_receptor.value = ""
        self.campo_cantidad.value = ""
        self.campo_descripcion.value = ""
        self._limpiar_errores()
        self.mensaje_resultado.visible = False
        self.update()
    
    def _mostrar_exito(self, mensaje: str):
        """Muestra un mensaje de éxito."""
        self.mensaje_resultado.content = ft.Row([
            ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_400),
            ft.Text(mensaje, size=14, color=ft.colors.GREEN_400),
        ])
        self.mensaje_resultado.bgcolor = ft.colors.GREEN_900
        self.mensaje_resultado.visible = True
    
    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error."""
        self.mensaje_resultado.content = ft.Row([
            ft.Icon(ft.icons.ERROR, color=ft.colors.RED_400),
            ft.Text(mensaje, size=14, color=ft.colors.RED_400),
        ])
        self.mensaje_resultado.bgcolor = ft.colors.RED_900
        self.mensaje_resultado.visible = True

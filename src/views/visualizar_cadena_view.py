"""
Vista de Visualización de Cadena.

Este módulo define la vista para visualizar la blockchain completa
con funcionalidades de búsqueda, exportación e importación.
"""

import flet as ft
from typing import Optional
from ..controllers.blockchain_controller import BlockchainController
from ..components.bloque_card import BloqueCard


class VisualizarCadenaView(ft.UserControl):
    """
    Vista para visualizar y gestionar la blockchain completa.
    
    Proporciona funcionalidades de búsqueda, exportación,
    importación y visualización detallada de la cadena.
    
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
        Inicializa la vista de visualización.
        
        Args:
            controller: Controlador de la blockchain.
            on_navegar: Callback para navegación.
        """
        super().__init__()
        self.controller = controller
        self.on_navegar = on_navegar
        self.controller.agregar_observador(self._actualizar_lista)
    
    def build(self):
        """Construye la vista de visualización."""
        # Campo de búsqueda
        self.campo_busqueda = ft.TextField(
            hint_text="Buscar en bloques...",
            prefix_icon=ft.icons.SEARCH,
            on_change=self._buscar,
            border_color=ft.colors.CYAN_700,
            focused_border_color=ft.colors.CYAN_400,
        )
        
        # Botones de acción
        botones_accion = ft.Row([
            ft.ElevatedButton(
                "Exportar JSON",
                icon=ft.icons.DOWNLOAD,
                on_click=self._exportar_blockchain,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                ),
            ),
            ft.ElevatedButton(
                "Importar JSON",
                icon=ft.icons.UPLOAD,
                on_click=self._importar_blockchain,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.PURPLE_700,
                    color=ft.colors.WHITE,
                ),
            ),
            ft.ElevatedButton(
                "Actualizar Vista",
                icon=ft.icons.REFRESH,
                on_click=lambda _: self._actualizar_lista(),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREEN_700,
                    color=ft.colors.WHITE,
                ),
            ),
        ], spacing=10)
        
        # Lista de bloques
        self.lista_bloques = ft.ListView(
            spacing=10,
            padding=20,
            expand=True,
        )
        
        # Contador de bloques
        self.contador_bloques = ft.Text(
            "0 bloques",
            size=14,
            color=ft.colors.WHITE60
        )
        
        # FilePicker para exportar/importar
        self.file_picker = ft.FilePicker(
            on_result=self._on_file_picker_result
        )
        
        # Diálogo de resultado
        self.dialogo_resultado = ft.AlertDialog(
            modal=True,
            title=ft.Text("Resultado"),
            content=ft.Text(""),
            actions=[
                ft.TextButton("Cerrar", on_click=self._cerrar_dialogo),
            ],
        )
        
        # Layout principal
        return ft.Column([
            self.file_picker,
            ft.Text(
                "Visualizar Blockchain",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            ft.Row([
                ft.Container(content=self.campo_busqueda, expand=True),
                self.contador_bloques,
            ], spacing=15),
            botones_accion,
            ft.Divider(height=20),
            ft.Container(
                content=self.lista_bloques,
                expand=True,
                border=ft.border.all(1, ft.colors.WHITE24),
                border_radius=10,
            ),
        ], spacing=15, expand=True)
    
    def did_mount(self):
        """Se ejecuta cuando el componente se monta."""
        self.page.overlay.append(self.file_picker)
        self._actualizar_lista()
    
    def will_unmount(self):
        """Se ejecuta cuando el componente se desmonta."""
        self.controller.remover_observador(self._actualizar_lista)
    
    def _actualizar_lista(self, criterio: str = ""):
        """
        Actualiza la lista de bloques.
        
        Args:
            criterio: Criterio de búsqueda (opcional).
        """
        if not self.page:
            return
        
        self.lista_bloques.controls.clear()
        
        if criterio:
            # Búsqueda
            bloques = self.controller.buscar_bloques(criterio)
        else:
            # Mostrar todos
            bloques = self.controller.obtener_cadena_completa()
        
        # Validar cadena
        es_cadena_valida, _ = self.controller.validar_cadena()
        
        # Crear tarjetas
        for bloque_dict in reversed(bloques):
            from ..models.bloque import Bloque
            bloque = Bloque.from_dict(bloque_dict)
            es_valido = bloque.validar() and es_cadena_valida
            
            card = BloqueCard(bloque_dict, es_valido=es_valido)
            self.lista_bloques.controls.append(card)
        
        # Actualizar contador
        self.contador_bloques.value = f"{len(bloques)} bloque(s)"
        
        self.update()
    
    def _buscar(self, e):
        """Busca bloques según el criterio ingresado."""
        criterio = self.campo_busqueda.value
        self._actualizar_lista(criterio)
    
    def _exportar_blockchain(self, e):
        """Exporta la blockchain a un archivo JSON."""
        self.accion_file_picker = "exportar"
        self.file_picker.save_file(
            dialog_title="Exportar Blockchain",
            file_name="blockchain.json",
            allowed_extensions=["json"],
        )
    
    def _importar_blockchain(self, e):
        """Importa una blockchain desde un archivo JSON."""
        self.accion_file_picker = "importar"
        self.file_picker.pick_files(
            dialog_title="Importar Blockchain",
            allowed_extensions=["json"],
            allow_multiple=False,
        )
    
    def _on_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Maneja el resultado del file picker."""
        if not e.path and not e.files:
            return
        
        if self.accion_file_picker == "exportar":
            ruta = e.path
            exito, mensaje = self.controller.exportar_blockchain(ruta)
            
            self.dialogo_resultado.title.value = "Exportar Blockchain"
            if exito:
                self.dialogo_resultado.content.value = f"✅ {mensaje}"
            else:
                self.dialogo_resultado.content.value = f"❌ {mensaje}"
            
        elif self.accion_file_picker == "importar":
            ruta = e.files[0].path
            exito, mensaje = self.controller.importar_blockchain(ruta)
            
            self.dialogo_resultado.title.value = "Importar Blockchain"
            if exito:
                self.dialogo_resultado.content.value = f"✅ {mensaje}"
                self._actualizar_lista()
            else:
                self.dialogo_resultado.content.value = f"❌ {mensaje}"
        
        self.page.dialog = self.dialogo_resultado
        self.dialogo_resultado.open = True
        self.page.update()
    
    def _cerrar_dialogo(self, e):
        """Cierra el diálogo de resultado."""
        self.dialogo_resultado.open = False
        self.page.update()

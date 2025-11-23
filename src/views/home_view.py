"""
Vista Principal (Home).

Este módulo define la vista principal de la aplicación que muestra
la lista de bloques y las estadísticas de la blockchain.
"""

import flet as ft
from typing import Optional
from ..controllers.blockchain_controller import BlockchainController
from ..components.bloque_card import BloqueCard


class HomeView(ft.UserControl):
    """
    Vista principal de la aplicación.
    
    Muestra la lista de bloques, estadísticas y acciones principales.
    Implementa el patrón Observer para actualizarse automáticamente.
    
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
        Inicializa la vista principal.
        
        Args:
            controller: Controlador de la blockchain.
            on_navegar: Callback para navegación.
        """
        super().__init__()
        self.controller = controller
        self.on_navegar = on_navegar
        
        # Registrarse como observador
        self.controller.agregar_observador(self._actualizar_vista)
    
    def build(self):
        """Construye la vista principal."""
        # Panel de estadísticas
        self.total_bloques_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
        self.estado_validez_text = ft.Text("Válida", size=16, color=ft.colors.GREEN_400)
        self.tamano_text = ft.Text("0 bytes", size=14)
        self.tiempo_promedio_text = ft.Text("0 seg", size=14)
        
        panel_estadisticas = ft.Container(
            content=ft.Row([
                # Total de bloques
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.LAYERS, size=40, color=ft.colors.CYAN_400),
                        self.total_bloques_text,
                        ft.Text("Bloques", size=12, color=ft.colors.WHITE60),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    expand=1,
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_GREY_900,
                ),
                # Estado de validez
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.VERIFIED, size=40, color=ft.colors.GREEN_400),
                        self.estado_validez_text,
                        ft.Text("Estado", size=12, color=ft.colors.WHITE60),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    expand=1,
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_GREY_900,
                ),
                # Tamaño
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.STORAGE, size=40, color=ft.colors.ORANGE_400),
                        self.tamano_text,
                        ft.Text("Tamaño", size=12, color=ft.colors.WHITE60),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    expand=1,
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_GREY_900,
                ),
                # Tiempo promedio
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.TIMER, size=40, color=ft.colors.PURPLE_400),
                        self.tiempo_promedio_text,
                        ft.Text("Tiempo Prom.", size=12, color=ft.colors.WHITE60),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    expand=1,
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_GREY_900,
                ),
            ], spacing=15),
            margin=ft.margin.only(bottom=20)
        )
        
        # Botones de acción
        botones_accion = ft.Row([
            ft.ElevatedButton(
                "Agregar Bloque",
                icon=ft.icons.ADD,
                on_click=lambda _: self.on_navegar(1) if self.on_navegar else None,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.CYAN_700,
                    color=ft.colors.WHITE,
                ),
            ),
            ft.ElevatedButton(
                "Validar Cadena",
                icon=ft.icons.CHECK_CIRCLE,
                on_click=self._validar_cadena,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREEN_700,
                    color=ft.colors.WHITE,
                ),
            ),
            ft.ElevatedButton(
                "Simular Ataque",
                icon=ft.icons.WARNING,
                on_click=self._mostrar_dialogo_ataque,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.RED_700,
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
        
        # Diálogo de resultado
        self.dialogo_resultado = ft.AlertDialog(
            modal=True,
            title=ft.Text("Resultado"),
            content=ft.Text(""),
            actions=[
                ft.TextButton("Cerrar", on_click=self._cerrar_dialogo),
            ],
        )
        
        # Contenedor principal
        return ft.Column([
            ft.Text(
                "Blockchain Demo",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            panel_estadisticas,
            botones_accion,
            ft.Divider(height=20),
            ft.Text("Bloques en la Cadena", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.lista_bloques,
                expand=True,
                border=ft.border.all(1, ft.colors.WHITE24),
                border_radius=10,
            ),
        ], spacing=10, expand=True)
    
    def did_mount(self):
        """Se ejecuta cuando el componente se monta."""
        self._actualizar_vista()
    
    def will_unmount(self):
        """Se ejecuta cuando el componente se desmonta."""
        self.controller.remover_observador(self._actualizar_vista)
    
    def _actualizar_vista(self):
        """Actualiza la vista con los datos actuales de la blockchain."""
        if not self.page:
            return
        
        # Actualizar estadísticas
        stats = self.controller.obtener_estadisticas()
        
        self.total_bloques_text.value = str(stats.get("total_bloques", 0))
        
        es_valida = stats.get("es_valida", True)
        self.estado_validez_text.value = "Válida" if es_valida else "Inválida"
        self.estado_validez_text.color = ft.colors.GREEN_400 if es_valida else ft.colors.RED_400
        
        tamano_kb = stats.get("tamano_bytes", 0) / 1024
        self.tamano_text.value = f"{tamano_kb:.2f} KB"
        
        self.tiempo_promedio_text.value = f"{stats.get('tiempo_promedio_segundos', 0):.2f} seg"
        
        # Actualizar lista de bloques
        cadena = self.controller.obtener_cadena_completa()
        self.lista_bloques.controls.clear()
        
        # Validar cada bloque
        es_cadena_valida, _ = self.controller.validar_cadena()
        
        for bloque_dict in reversed(cadena):  # Mostrar del más reciente al más antiguo
            # Verificar validez individual del bloque
            from ..models.bloque import Bloque
            bloque = Bloque.from_dict(bloque_dict)
            es_valido = bloque.validar() and es_cadena_valida
            
            card = BloqueCard(bloque_dict, es_valido=es_valido)
            self.lista_bloques.controls.append(card)
        
        self.update()
    
    def _validar_cadena(self, e):
        """Valida la cadena y muestra el resultado."""
        es_valida, mensaje = self.controller.validar_cadena()
        
        self.dialogo_resultado.title.value = "Validación de Cadena"
        if es_valida:
            self.dialogo_resultado.content.value = "✅ La cadena es válida e íntegra"
        else:
            self.dialogo_resultado.content.value = f"❌ La cadena es inválida:\n{mensaje}"
        
        self.page.dialog = self.dialogo_resultado
        self.dialogo_resultado.open = True
        self.page.update()
    
    def _mostrar_dialogo_ataque(self, e):
        """Muestra diálogo para simular ataque."""
        def simular(e):
            try:
                indice = int(campo_indice.value)
                exito, mensaje = self.controller.simular_ataque(indice)
                
                dialogo_ataque.open = False
                self.page.update()
                
                self.dialogo_resultado.title.value = "Ataque Simulado"
                self.dialogo_resultado.content.value = mensaje
                self.page.dialog = self.dialogo_resultado
                self.dialogo_resultado.open = True
                self.page.update()
                
            except ValueError:
                campo_indice.error_text = "Ingrese un número válido"
                self.page.update()
        
        campo_indice = ft.TextField(
            label="Índice del bloque a modificar",
            hint_text="0, 1, 2, ...",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        dialogo_ataque = ft.AlertDialog(
            modal=True,
            title=ft.Text("Simular Ataque a la Blockchain"),
            content=ft.Column([
                ft.Text("Esto modificará los datos de un bloque sin recalcular su hash,"),
                ft.Text("demostrando cómo se detecta la manipulación."),
                campo_indice,
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo_custom(dialogo_ataque)),
                ft.TextButton("Simular Ataque", on_click=simular),
            ],
        )
        
        self.page.dialog = dialogo_ataque
        dialogo_ataque.open = True
        self.page.update()
    
    def _cerrar_dialogo(self, e):
        """Cierra el diálogo de resultado."""
        self.dialogo_resultado.open = False
        self.page.update()
    
    def _cerrar_dialogo_custom(self, dialogo):
        """Cierra un diálogo personalizado."""
        dialogo.open = False
        self.page.update()

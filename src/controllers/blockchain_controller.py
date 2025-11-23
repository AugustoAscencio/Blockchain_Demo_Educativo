"""
Controlador de Blockchain.

Este módulo implementa el controlador principal que gestiona la lógica
de negocio y actúa como intermediario entre las vistas y el modelo.
Implementa el patrón Observer para notificar cambios a las vistas.
"""

from typing import List, Callable, Dict, Any, Optional
import logging
from ..models.blockchain import CadenaDeBloques
from ..models.transaccion import Transaccion
from ..utils.validators import ValidadorTransaccion

logger = logging.getLogger(__name__)


class BlockchainController:
    """
    Controlador principal de la aplicación blockchain.
    
    Gestiona la lógica de negocio y coordina las interacciones
    entre las vistas y el modelo. Implementa patrón Observer.
    
    Attributes:
        __blockchain: Instancia única de la blockchain.
        __observadores: Lista de callbacks a notificar cuando hay cambios.
    """
    
    def __init__(self):
        """Inicializa el controlador."""
        self.__blockchain = CadenaDeBloques.get_instance()
        self.__observadores: List[Callable] = []
        self.__validador_transaccion = ValidadorTransaccion()
        
        logger.info("BlockchainController inicializado")
    
    # Patrón Observer
    
    def agregar_observador(self, callback: Callable) -> None:
        """
        Agrega un observador que será notificado de cambios.
        
        Args:
            callback: Función a llamar cuando hay cambios.
        """
        if callback not in self.__observadores:
            self.__observadores.append(callback)
            logger.debug(f"Observador agregado. Total: {len(self.__observadores)}")
    
    def remover_observador(self, callback: Callable) -> None:
        """
        Remueve un observador.
        
        Args:
            callback: Función a remover.
        """
        if callback in self.__observadores:
            self.__observadores.remove(callback)
            logger.debug(f"Observador removido. Total: {len(self.__observadores)}")
    
    def notificar_observadores(self) -> None:
        """Notifica a todos los observadores de un cambio."""
        logger.debug(f"Notificando a {len(self.__observadores)} observadores")
        for observador in self.__observadores:
            try:
                observador()
            except Exception as e:
                logger.error(f"Error al notificar observador: {str(e)}")
    
    # Operaciones de Blockchain
    
    def agregar_bloque_con_transaccion(
        self,
        emisor: str,
        receptor: str,
        cantidad: float,
        descripcion: str = ""
    ) -> tuple[bool, str]:
        """
        Agrega un nuevo bloque con una transacción.
        
        Args:
            emisor: Dirección del emisor.
            receptor: Dirección del receptor.
            cantidad: Cantidad a transferir.
            descripcion: Descripción opcional.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            # Validar datos de la transacción
            datos_transaccion = {
                "emisor": emisor,
                "receptor": receptor,
                "cantidad": cantidad,
                "descripcion": descripcion
            }
            
            es_valida, mensaje = self.__validador_transaccion.validar(datos_transaccion)
            
            if not es_valida:
                return False, mensaje
            
            # Crear transacción
            transaccion = Transaccion(emisor, receptor, cantidad, descripcion)
            
            # Agregar bloque con la transacción
            exito = self.__blockchain.agregar_bloque(transaccion.to_dict())
            
            if exito:
                self.notificar_observadores()
                return True, "Bloque agregado exitosamente"
            else:
                return False, "Error al agregar el bloque"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Error al agregar bloque: {str(e)}")
            return False, f"Error inesperado: {str(e)}"
    
    def agregar_bloque_personalizado(self, datos: Dict[str, Any]) -> tuple[bool, str]:
        """
        Agrega un bloque con datos personalizados.
        
        Args:
            datos: Diccionario con datos a almacenar.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            exito = self.__blockchain.agregar_bloque(datos)
            
            if exito:
                self.notificar_observadores()
                return True, "Bloque agregado exitosamente"
            else:
                return False, "Error al agregar el bloque"
                
        except Exception as e:
            logger.error(f"Error al agregar bloque: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def obtener_cadena_completa(self) -> List[Dict[str, Any]]:
        """
        Obtiene toda la cadena en formato diccionario.
        
        Returns:
            Lista de bloques en formato diccionario.
        """
        return self.__blockchain.obtener_cadena_completa()
    
    def validar_cadena(self) -> tuple[bool, str]:
        """
        Valida la integridad de la cadena completa.
        
        Returns:
            Tupla (es_válida, mensaje).
        """
        return self.__blockchain.validar_cadena()
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la blockchain.
        
        Returns:
            Diccionario con estadísticas.
        """
        return self.__blockchain.obtener_estadisticas()
    
    def buscar_bloques(self, criterio: str) -> List[Dict[str, Any]]:
        """
        Busca bloques por criterio.
        
        Args:
            criterio: Texto a buscar.
        
        Returns:
            Lista de bloques que coinciden.
        """
        bloques = self.__blockchain.buscar_bloques(criterio)
        return [bloque.to_dict() for bloque in bloques]
    
    def exportar_blockchain(self, ruta_archivo: str) -> tuple[bool, str]:
        """
        Exporta la blockchain a un archivo JSON.
        
        Args:
            ruta_archivo: Ruta donde guardar el archivo.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            exito = self.__blockchain.exportar_json(ruta_archivo)
            
            if exito:
                return True, f"Blockchain exportada a {ruta_archivo}"
            else:
                return False, "Error al exportar blockchain"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def importar_blockchain(self, ruta_archivo: str) -> tuple[bool, str]:
        """
        Importa una blockchain desde un archivo JSON.
        
        Args:
            ruta_archivo: Ruta del archivo a importar.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            exito = self.__blockchain.importar_json(ruta_archivo)
            
            if exito:
                self.notificar_observadores()
                return True, f"Blockchain importada desde {ruta_archivo}"
            else:
                return False, "Error al importar blockchain"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def simular_ataque(self, indice_bloque: int) -> tuple[bool, str]:
        """
        Simula un ataque modificando un bloque.
        
        Args:
            indice_bloque: Índice del bloque a modificar.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            nuevos_datos = {
                "mensaje": "¡DATOS MODIFICADOS!",
                "atacante": "Hacker",
                "nota": "Este bloque fue modificado para demostrar inmutabilidad"
            }
            
            exito = self.__blockchain.simular_ataque(indice_bloque, nuevos_datos)
            
            if exito:
                self.notificar_observadores()
                return True, f"Bloque {indice_bloque} modificado. La cadena ahora es inválida."
            else:
                return False, "No se pudo modificar el bloque"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_longitud(self) -> int:
        """
        Obtiene la longitud de la cadena.
        
        Returns:
            Número de bloques.
        """
        return self.__blockchain.longitud()
    
    def reiniciar_blockchain(self) -> tuple[bool, str]:
        """
        Reinicia la blockchain al estado inicial.
        
        Returns:
            Tupla (éxito, mensaje).
        """
        try:
            self.__blockchain.reiniciar()
            self.notificar_observadores()
            return True, "Blockchain reiniciada exitosamente"
        except Exception as e:
            return False, f"Error al reiniciar: {str(e)}"

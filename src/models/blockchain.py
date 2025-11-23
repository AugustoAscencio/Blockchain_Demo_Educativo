"""
Modelo de Blockchain.

Este módulo define la clase CadenaDeBloques que gestiona la cadena completa,
implementando el patrón Singleton para garantizar una única instancia.
"""

from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime
from .bloque import Bloque
from ..utils.validators import ValidadorCadena, ValidadorBloque

logger = logging.getLogger(__name__)


class CadenaDeBloques:
    """
    Gestiona la cadena de bloques completa.
    
    Implementa el patrón Singleton para garantizar una única instancia
    de la blockchain en toda la aplicación.
    
    Attributes:
        __instance: Instancia única de la clase (Singleton).
        __cadena: Lista de bloques que conforman la cadena.
    """
    
    __instance: Optional['CadenaDeBloques'] = None
    
    def __new__(cls):
        """
        Implementación del patrón Singleton.
        
        Returns:
            La única instancia de CadenaDeBloques.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__inicializado = False
        return cls.__instance
    
    def __init__(self):
        """Inicializa la blockchain con el bloque génesis."""
        # Evitar reinicialización en llamadas subsecuentes
        if self.__inicializado:
            return
        
        self.__cadena: List[Bloque] = []
        self.__validador_cadena = ValidadorCadena()
        self.__validador_bloque = ValidadorBloque()
        
        # Crear bloque génesis
        bloque_genesis = Bloque.crear_bloque_genesis()
        self.__cadena.append(bloque_genesis)
        
        self.__inicializado = True
        logger.info("Blockchain inicializada con bloque génesis")
    
    @classmethod
    def get_instance(cls) -> 'CadenaDeBloques':
        """
        Obtiene la instancia única de la blockchain (Singleton).
        
        Returns:
            La única instancia de CadenaDeBloques.
        
        Example:
            >>> blockchain = CadenaDeBloques.get_instance()
        """
        if cls.__instance is None:
            cls()
        return cls.__instance
    
    def agregar_bloque(self, datos: Dict[str, Any]) -> bool:
        """
        Agrega un nuevo bloque a la cadena.
        
        Args:
            datos: Datos a almacenar en el nuevo bloque.
        
        Returns:
            True si el bloque se agregó exitosamente, False en caso contrario.
        
        Example:
            >>> blockchain.agregar_bloque({"transaccion": "Alice -> Bob: 100"})
            True
        """
        try:
            # Obtener el último bloque
            ultimo_bloque = self.obtener_ultimo_bloque()
            
            # Crear nuevo bloque
            nuevo_indice = ultimo_bloque.get_indice() + 1
            hash_previo = ultimo_bloque.get_hash()
            
            nuevo_bloque = Bloque.crear_bloque(nuevo_indice, datos, hash_previo)
            
            # Validar el nuevo bloque antes de agregarlo
            es_valido, mensaje = self.__validador_bloque.validar(nuevo_bloque.to_dict())
            
            if not es_valido:
                logger.error(f"Bloque inválido: {mensaje}")
                return False
            
            # Agregar a la cadena
            self.__cadena.append(nuevo_bloque)
            logger.info(f"Bloque {nuevo_indice} agregado exitosamente")
            
            return True
            
        except Exception as e:
            logger.error(f"Error al agregar bloque: {str(e)}")
            return False
    
    def obtener_ultimo_bloque(self) -> Bloque:
        """
        Obtiene el último bloque de la cadena.
        
        Returns:
            El último bloque de la cadena.
        """
        return self.__cadena[-1]
    
    def validar_cadena(self) -> tuple[bool, str]:
        """
        Valida la integridad completa de la cadena.
        
        Verifica:
        1. Integridad de cada bloque individual
        2. Enlaces correctos entre bloques
        3. Estructura general de la cadena
        
        Returns:
            Tupla (es_valida, mensaje).
        
        Example:
            >>> es_valida, mensaje = blockchain.validar_cadena()
        """
        # Validar cada bloque individualmente
        for bloque in self.__cadena:
            if not bloque.validar():
                return False, f"Bloque {bloque.get_indice()} tiene hash inválido"
        
        # Validar la estructura de la cadena
        cadena_dict = [bloque.to_dict() for bloque in self.__cadena]
        es_valida, mensaje = self.__validador_cadena.validar(cadena_dict)
        
        if es_valida:
            logger.info("Cadena validada correctamente")
        else:
            logger.warning(f"Cadena inválida: {mensaje}")
        
        return es_valida, mensaje
    
    def obtener_cadena_completa(self) -> List[Dict[str, Any]]:
        """
        Obtiene toda la cadena en formato diccionario.
        
        Returns:
            Lista de diccionarios con los datos de cada bloque.
        """
        return [bloque.to_dict() for bloque in self.__cadena]
    
    def longitud(self) -> int:
        """
        Obtiene la longitud de la cadena.
        
        Returns:
            Número de bloques en la cadena.
        """
        return len(self.__cadena)
    
    def obtener_bloque(self, indice: int) -> Optional[Bloque]:
        """
        Obtiene un bloque específico por su índice.
        
        Args:
            indice: Índice del bloque a obtener.
        
        Returns:
            El bloque solicitado o None si no existe.
        """
        if 0 <= indice < len(self.__cadena):
            return self.__cadena[indice]
        return None
    
    def buscar_bloques(self, criterio: str) -> List[Bloque]:
        """
        Busca bloques que contengan el criterio en sus datos.
        
        Args:
            criterio: Texto a buscar en los datos de los bloques.
        
        Returns:
            Lista de bloques que coinciden con el criterio.
        """
        resultados = []
        criterio_lower = criterio.lower()
        
        for bloque in self.__cadena:
            datos_str = json.dumps(bloque.get_datos(), ensure_ascii=False).lower()
            if criterio_lower in datos_str:
                resultados.append(bloque)
        
        logger.debug(f"Búsqueda '{criterio}': {len(resultados)} resultados")
        return resultados
    
    def exportar_json(self, ruta_archivo: str) -> bool:
        """
        Exporta la blockchain a un archivo JSON.
        
        Args:
            ruta_archivo: Ruta del archivo donde guardar.
        
        Returns:
            True si se exportó exitosamente, False en caso contrario.
        """
        try:
            cadena_dict = self.obtener_cadena_completa()
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(cadena_dict, archivo, indent=2, ensure_ascii=False)
            
            logger.info(f"Blockchain exportada a {ruta_archivo}")
            return True
            
        except Exception as e:
            logger.error(f"Error al exportar blockchain: {str(e)}")
            return False
    
    def importar_json(self, ruta_archivo: str) -> bool:
        """
        Importa una blockchain desde un archivo JSON.
        
        Args:
            ruta_archivo: Ruta del archivo a importar.
        
        Returns:
            True si se importó exitosamente, False en caso contrario.
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                cadena_dict = json.load(archivo)
            
            # Validar la cadena importada
            es_valida, mensaje = self.__validador_cadena.validar(cadena_dict)
            
            if not es_valida:
                logger.error(f"Cadena importada inválida: {mensaje}")
                return False
            
            # Reconstruir la cadena
            nueva_cadena = [Bloque.from_dict(bloque_dict) for bloque_dict in cadena_dict]
            self.__cadena = nueva_cadena
            
            logger.info(f"Blockchain importada desde {ruta_archivo}")
            return True
            
        except Exception as e:
            logger.error(f"Error al importar blockchain: {str(e)}")
            return False
    
    def simular_ataque(self, indice_bloque: int, nuevos_datos: Dict[str, Any]) -> bool:
        """
        Simula un ataque modificando datos de un bloque sin recalcular hash.
        
        SOLO PARA DEMOSTRACIÓN de inmutabilidad.
        
        Args:
            indice_bloque: Índice del bloque a modificar.
            nuevos_datos: Nuevos datos a establecer.
        
        Returns:
            True si se pudo modificar, False en caso contrario.
        """
        if 0 <= indice_bloque < len(self.__cadena):
            bloque = self.__cadena[indice_bloque]
            bloque._modificar_datos(nuevos_datos)
            logger.warning(f"¡ATAQUE SIMULADO! Bloque {indice_bloque} modificado")
            return True
        return False
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la blockchain.
        
        Returns:
            Diccionario con estadísticas.
        """
        if len(self.__cadena) == 0:
            return {}
        
        # Calcular tamaño en bytes
        cadena_json = json.dumps(self.obtener_cadena_completa())
        tamano_bytes = len(cadena_json.encode('utf-8'))
        
        # Calcular tiempo promedio entre bloques
        if len(self.__cadena) > 1:
            primer_bloque = self.__cadena[0]
            ultimo_bloque = self.__cadena[-1]
            
            tiempo_inicio = datetime.fromisoformat(primer_bloque.get_timestamp())
            tiempo_fin = datetime.fromisoformat(ultimo_bloque.get_timestamp())
            
            diferencia = (tiempo_fin - tiempo_inicio).total_seconds()
            tiempo_promedio = diferencia / (len(self.__cadena) - 1) if len(self.__cadena) > 1 else 0
        else:
            tiempo_promedio = 0
        
        es_valida, _ = self.validar_cadena()
        
        return {
            "total_bloques": len(self.__cadena),
            "tamano_bytes": tamano_bytes,
            "tiempo_promedio_segundos": round(tiempo_promedio, 2),
            "es_valida": es_valida
        }
    
    def reiniciar(self) -> None:
        """
        Reinicia la blockchain al estado inicial (solo bloque génesis).
        
        ADVERTENCIA: Esto elimina todos los bloques excepto el génesis.
        """
        logger.warning("Reiniciando blockchain")
        self.__cadena = [Bloque.crear_bloque_genesis()]

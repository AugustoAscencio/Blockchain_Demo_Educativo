"""
Modelo de Bloque.

Este módulo define la clase Bloque que representa un bloque individual
en la blockchain, implementando el patrón Factory Method.
"""

from datetime import datetime
from typing import Dict, Any, Optional
import logging
from ..utils.hash_utils import calcular_sha256, combinar_datos_para_hash

logger = logging.getLogger(__name__)


class Bloque:
    """
    Representa un bloque en la blockchain.
    
    Implementa el patrón Factory Method para la creación de bloques.
    Los atributos son privados para garantizar encapsulación.
    
    Attributes:
        __indice: Posición del bloque en la cadena.
        __timestamp: Marca de tiempo de creación.
        __datos: Datos almacenados en el bloque.
        __hash_previo: Hash del bloque anterior.
        __hash_actual: Hash calculado de este bloque.
        __nonce: Número usado para proof-of-work (opcional).
    """
    
    def __init__(
        self,
        indice: int,
        timestamp: str,
        datos: Dict[str, Any],
        hash_previo: str,
        nonce: int = 0
    ):
        """
        Inicializa un bloque (uso interno, preferir métodos factory).
        
        Args:
            indice: Posición del bloque en la cadena.
            timestamp: Marca de tiempo ISO format.
            datos: Datos a almacenar en el bloque.
            hash_previo: Hash del bloque anterior.
            nonce: Número para proof-of-work.
        """
        self.__indice = indice
        self.__timestamp = timestamp
        self.__datos = datos
        self.__hash_previo = hash_previo
        self.__nonce = nonce
        self.__hash_actual = self.calcular_hash()
        
        logger.debug(f"Bloque {indice} creado con hash {self.__hash_actual[:16]}...")
    
    def calcular_hash(self) -> str:
        """
        Calcula el hash SHA-256 del bloque.
        
        El hash se calcula combinando: índice + timestamp + datos + hash_previo + nonce
        
        Returns:
            Hash SHA-256 en formato hexadecimal.
        """
        datos_combinados = combinar_datos_para_hash(
            self.__indice,
            self.__timestamp,
            self.__datos,
            self.__hash_previo,
            self.__nonce
        )
        return calcular_sha256(datos_combinados)
    
    def validar(self) -> bool:
        """
        Verifica la integridad del bloque.
        
        Recalcula el hash y lo compara con el hash almacenado.
        
        Returns:
            True si el bloque es válido, False en caso contrario.
        """
        hash_recalculado = self.calcular_hash()
        es_valido = hash_recalculado == self.__hash_actual
        
        if not es_valido:
            logger.warning(f"Bloque {self.__indice} inválido: hash no coincide")
        
        return es_valido
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa el bloque a un diccionario.
        
        Returns:
            Diccionario con todos los datos del bloque.
        """
        return {
            "indice": self.__indice,
            "timestamp": self.__timestamp,
            "datos": self.__datos,
            "hash_previo": self.__hash_previo,
            "hash_actual": self.__hash_actual,
            "nonce": self.__nonce
        }
    
    @staticmethod
    def from_dict(datos: Dict[str, Any]) -> 'Bloque':
        """
        Crea un bloque desde un diccionario.
        
        Args:
            datos: Diccionario con los datos del bloque.
        
        Returns:
            Nueva instancia de Bloque.
        
        Raises:
            KeyError: Si faltan campos requeridos.
        """
        bloque = Bloque(
            indice=datos["indice"],
            timestamp=datos["timestamp"],
            datos=datos["datos"],
            hash_previo=datos["hash_previo"],
            nonce=datos.get("nonce", 0)
        )
        
        # Restaurar el hash original
        bloque.__hash_actual = datos["hash_actual"]
        
        return bloque
    
    @staticmethod
    def crear_bloque(
        indice: int,
        datos: Dict[str, Any],
        hash_previo: str
    ) -> 'Bloque':
        """
        Factory Method: Crea un nuevo bloque válido.
        
        Args:
            indice: Posición del bloque en la cadena.
            datos: Datos a almacenar.
            hash_previo: Hash del bloque anterior.
        
        Returns:
            Nueva instancia de Bloque.
        
        Example:
            >>> bloque = Bloque.crear_bloque(1, {"transaccion": "..."}, "hash_anterior")
        """
        timestamp = datetime.now().isoformat()
        return Bloque(indice, timestamp, datos, hash_previo)
    
    @staticmethod
    def crear_bloque_genesis() -> 'Bloque':
        """
        Factory Method: Crea el bloque génesis (primer bloque de la cadena).
        
        El bloque génesis tiene índice 0 y hash_previo "0".
        
        Returns:
            Bloque génesis.
        
        Example:
            >>> genesis = Bloque.crear_bloque_genesis()
        """
        datos_genesis = {
            "mensaje": "Bloque Génesis",
            "descripcion": "Primer bloque de la cadena"
        }
        timestamp = datetime.now().isoformat()
        
        logger.info("Creando bloque génesis")
        return Bloque(0, timestamp, datos_genesis, "0")
    
    # Getters para acceso controlado a atributos privados
    
    def get_indice(self) -> int:
        """Retorna el índice del bloque."""
        return self.__indice
    
    def get_timestamp(self) -> str:
        """Retorna el timestamp del bloque."""
        return self.__timestamp
    
    def get_datos(self) -> Dict[str, Any]:
        """Retorna los datos del bloque."""
        return self.__datos.copy()  # Retornar copia para evitar modificaciones
    
    def get_hash_previo(self) -> str:
        """Retorna el hash del bloque anterior."""
        return self.__hash_previo
    
    def get_hash(self) -> str:
        """Retorna el hash actual del bloque."""
        return self.__hash_actual
    
    def get_nonce(self) -> int:
        """Retorna el nonce del bloque."""
        return self.__nonce
    
    # Método especial para simular ataque (solo para demostración)
    def _modificar_datos(self, nuevos_datos: Dict[str, Any]) -> None:
        """
        SOLO PARA DEMOSTRACIÓN: Modifica los datos sin recalcular hash.
        
        Esto rompe la integridad del bloque intencionalmente.
        
        Args:
            nuevos_datos: Nuevos datos a establecer.
        """
        logger.warning(f"¡ATENCIÓN! Modificando datos del bloque {self.__indice} sin recalcular hash")
        self.__datos = nuevos_datos
    
    def __str__(self) -> str:
        """Representación en string del bloque."""
        return f"Bloque #{self.__indice} [Hash: {self.__hash_actual[:16]}...]"
    
    def __repr__(self) -> str:
        """Representación técnica del bloque."""
        return f"Bloque(indice={self.__indice}, hash={self.__hash_actual[:16]}...)"

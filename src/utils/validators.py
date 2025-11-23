"""
Validadores con patrón Chain of Responsibility.

Este módulo implementa validadores para transacciones, bloques y cadenas
usando el patrón de diseño Chain of Responsibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging

# Configurar logging
logger = logging.getLogger(__name__)


class Validador(ABC):
    """
    Clase base abstracta para validadores.
    
    Implementa el patrón Chain of Responsibility permitiendo
    encadenar múltiples validadores.
    """
    
    def __init__(self):
        """Inicializa el validador."""
        self._siguiente: Optional[Validador] = None
    
    def establecer_siguiente(self, validador: 'Validador') -> 'Validador':
        """
        Establece el siguiente validador en la cadena.
        
        Args:
            validador: Siguiente validador a ejecutar.
        
        Returns:
            El validador establecido para permitir encadenamiento.
        """
        self._siguiente = validador
        return validador
    
    def validar(self, datos: Any) -> tuple[bool, str]:
        """
        Valida los datos y pasa al siguiente validador si existe.
        
        Args:
            datos: Datos a validar.
        
        Returns:
            Tupla (es_valido, mensaje_error).
        """
        # Ejecutar validación específica
        es_valido, mensaje = self._validar_especifico(datos)
        
        if not es_valido:
            return False, mensaje
        
        # Si hay siguiente validador, continuar la cadena
        if self._siguiente:
            return self._siguiente.validar(datos)
        
        return True, "Validación exitosa"
    
    @abstractmethod
    def _validar_especifico(self, datos: Any) -> tuple[bool, str]:
        """
        Método abstracto para validación específica.
        
        Args:
            datos: Datos a validar.
        
        Returns:
            Tupla (es_valido, mensaje_error).
        """
        pass


class ValidadorTransaccion(Validador):
    """Validador para transacciones."""
    
    def _validar_especifico(self, datos: Dict) -> tuple[bool, str]:
        """
        Valida que una transacción tenga los campos requeridos.
        
        Args:
            datos: Diccionario con datos de la transacción.
        
        Returns:
            Tupla (es_valido, mensaje_error).
        """
        # Verificar que sea un diccionario
        if not isinstance(datos, dict):
            return False, "La transacción debe ser un diccionario"
        
        # Campos requeridos
        campos_requeridos = ["emisor", "receptor", "cantidad"]
        
        for campo in campos_requeridos:
            if campo not in datos:
                return False, f"Falta el campo requerido: {campo}"
            
            if not datos[campo]:
                return False, f"El campo '{campo}' no puede estar vacío"
        
        # Validar que la cantidad sea numérica y positiva
        try:
            cantidad = float(datos["cantidad"])
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a cero"
        except (ValueError, TypeError):
            return False, "La cantidad debe ser un número válido"
        
        logger.debug(f"Transacción validada: {datos['emisor']} -> {datos['receptor']}")
        return True, ""


class ValidadorBloque(Validador):
    """Validador para bloques individuales."""
    
    def _validar_especifico(self, datos: Dict) -> tuple[bool, str]:
        """
        Valida que un bloque tenga la estructura correcta.
        
        Args:
            datos: Diccionario con datos del bloque.
        
        Returns:
            Tupla (es_valido, mensaje_error).
        """
        # Verificar que sea un diccionario
        if not isinstance(datos, dict):
            return False, "El bloque debe ser un diccionario"
        
        # Campos requeridos en un bloque
        campos_requeridos = ["indice", "timestamp", "datos", "hash_previo", "hash_actual"]
        
        for campo in campos_requeridos:
            if campo not in datos:
                return False, f"Falta el campo requerido en el bloque: {campo}"
        
        # Validar que el índice sea numérico
        try:
            indice = int(datos["indice"])
            if indice < 0:
                return False, "El índice del bloque debe ser mayor o igual a cero"
        except (ValueError, TypeError):
            return False, "El índice debe ser un número entero válido"
        
        # Validar que los hashes no estén vacíos
        if not datos["hash_actual"]:
            return False, "El hash actual del bloque no puede estar vacío"
        
        logger.debug(f"Bloque {datos['indice']} validado correctamente")
        return True, ""


class ValidadorCadena(Validador):
    """Validador para la integridad de la cadena completa."""
    
    def _validar_especifico(self, datos: List[Dict]) -> tuple[bool, str]:
        """
        Valida la integridad de toda la cadena de bloques.
        
        Args:
            datos: Lista de bloques en formato diccionario.
        
        Returns:
            Tupla (es_valido, mensaje_error).
        """
        # Verificar que sea una lista
        if not isinstance(datos, list):
            return False, "La cadena debe ser una lista de bloques"
        
        # Verificar que tenga al menos el bloque génesis
        if len(datos) == 0:
            return False, "La cadena está vacía"
        
        # Validar el bloque génesis
        bloque_genesis = datos[0]
        if bloque_genesis.get("indice") != 0:
            return False, "El primer bloque debe tener índice 0"
        
        if bloque_genesis.get("hash_previo") != "0":
            return False, "El bloque génesis debe tener hash_previo = '0'"
        
        # Validar enlaces entre bloques
        for i in range(1, len(datos)):
            bloque_actual = datos[i]
            bloque_anterior = datos[i - 1]
            
            # Verificar que el índice sea consecutivo
            if bloque_actual.get("indice") != i:
                return False, f"Índice incorrecto en bloque {i}"
            
            # Verificar que el hash_previo coincida con el hash del bloque anterior
            if bloque_actual.get("hash_previo") != bloque_anterior.get("hash_actual"):
                return False, f"Cadena rota en bloque {i}: hash_previo no coincide"
        
        logger.info(f"Cadena de {len(datos)} bloques validada correctamente")
        return True, ""


def crear_cadena_validacion() -> Validador:
    """
    Crea una cadena de validadores para transacciones.
    
    Returns:
        Validador raíz de la cadena.
    
    Example:
        >>> validador = crear_cadena_validacion()
        >>> es_valido, mensaje = validador.validar({"emisor": "A", "receptor": "B", "cantidad": 100})
    """
    validador_transaccion = ValidadorTransaccion()
    return validador_transaccion

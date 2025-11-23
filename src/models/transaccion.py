"""
Modelo de Transacción.

Este módulo define la clase Transaccion que representa una transacción
individual en la blockchain.
"""

from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Transaccion:
    """
    Representa una transacción en la blockchain.
    
    Una transacción contiene información sobre el emisor, receptor,
    cantidad transferida y una descripción opcional.
    
    Attributes:
        emisor: Dirección o nombre del emisor.
        receptor: Dirección o nombre del receptor.
        cantidad: Cantidad a transferir (debe ser positiva).
        descripcion: Descripción opcional de la transacción.
        timestamp: Marca de tiempo de creación.
    """
    
    def __init__(
        self,
        emisor: str,
        receptor: str,
        cantidad: float,
        descripcion: str = ""
    ):
        """
        Inicializa una nueva transacción.
        
        Args:
            emisor: Dirección o nombre del emisor.
            receptor: Dirección o nombre del receptor.
            cantidad: Cantidad a transferir.
            descripcion: Descripción opcional de la transacción.
        
        Raises:
            ValueError: Si la cantidad es negativa o cero.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        
        self.emisor = emisor
        self.receptor = receptor
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.timestamp = datetime.now().isoformat()
        
        logger.debug(f"Transacción creada: {emisor} -> {receptor}: {cantidad}")
    
    def to_dict(self) -> Dict:
        """
        Convierte la transacción a un diccionario.
        
        Returns:
            Diccionario con los datos de la transacción.
        
        Example:
            >>> t = Transaccion("Alice", "Bob", 100, "Pago")
            >>> t.to_dict()
            {'emisor': 'Alice', 'receptor': 'Bob', 'cantidad': 100, ...}
        """
        return {
            "emisor": self.emisor,
            "receptor": self.receptor,
            "cantidad": self.cantidad,
            "descripcion": self.descripcion,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def from_dict(datos: Dict) -> 'Transaccion':
        """
        Crea una transacción desde un diccionario.
        
        Args:
            datos: Diccionario con los datos de la transacción.
        
        Returns:
            Nueva instancia de Transaccion.
        
        Raises:
            KeyError: Si faltan campos requeridos.
        """
        transaccion = Transaccion(
            emisor=datos["emisor"],
            receptor=datos["receptor"],
            cantidad=datos["cantidad"],
            descripcion=datos.get("descripcion", "")
        )
        
        # Restaurar timestamp si existe
        if "timestamp" in datos:
            transaccion.timestamp = datos["timestamp"]
        
        return transaccion
    
    def __str__(self) -> str:
        """
        Representación en string de la transacción.
        
        Returns:
            String descriptivo de la transacción.
        """
        return f"{self.emisor} -> {self.receptor}: {self.cantidad}"
    
    def __repr__(self) -> str:
        """
        Representación técnica de la transacción.
        
        Returns:
            String con representación técnica.
        """
        return f"Transaccion(emisor='{self.emisor}', receptor='{self.receptor}', cantidad={self.cantidad})"

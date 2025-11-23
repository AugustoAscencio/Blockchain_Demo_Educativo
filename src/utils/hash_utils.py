"""
Utilidades para cálculo de hashes SHA-256.

Este módulo proporciona funciones para calcular y formatear hashes
criptográficos usando el algoritmo SHA-256.
"""

import hashlib
import json
from typing import Any, Union


def calcular_sha256(datos: Union[str, dict]) -> str:
    """
    Calcula el hash SHA-256 de los datos proporcionados.
    
    Args:
        datos: Datos a hashear. Puede ser string o diccionario.
               Si es diccionario, se convierte a JSON string.
    
    Returns:
        Hash SHA-256 en formato hexadecimal (64 caracteres).
    
    Example:
        >>> calcular_sha256("Hola Mundo")
        'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    """
    # Convertir diccionario a string JSON si es necesario
    if isinstance(datos, dict):
        datos_str = json.dumps(datos, sort_keys=True, ensure_ascii=False)
    else:
        datos_str = str(datos)
    
    # Calcular hash SHA-256
    hash_objeto = hashlib.sha256(datos_str.encode('utf-8'))
    return hash_objeto.hexdigest()


def formatear_hash(hash_completo: str, longitud: int = 16) -> str:
    """
    Formatea un hash para visualización truncándolo.
    
    Args:
        hash_completo: Hash completo en formato hexadecimal.
        longitud: Número de caracteres a mostrar (default: 16).
    
    Returns:
        Hash truncado con puntos suspensivos si fue acortado.
    
    Example:
        >>> formatear_hash("a591a6d40bf420404a011733cfb7b190", 8)
        'a591a6d4...'
    """
    if len(hash_completo) <= longitud:
        return hash_completo
    
    return f"{hash_completo[:longitud]}..."


def combinar_datos_para_hash(*args: Any) -> str:
    """
    Combina múltiples datos en un string para hashear.
    
    Args:
        *args: Datos variables a combinar.
    
    Returns:
        String combinado de todos los argumentos.
    
    Example:
        >>> combinar_datos_para_hash(1, "abc", {"key": "value"})
        '1|abc|{"key": "value"}'
    """
    partes = []
    for dato in args:
        if isinstance(dato, dict):
            partes.append(json.dumps(dato, sort_keys=True, ensure_ascii=False))
        else:
            partes.append(str(dato))
    
    return "|".join(partes)


def verificar_hash(datos: Union[str, dict], hash_esperado: str) -> bool:
    """
    Verifica si el hash de los datos coincide con el hash esperado.
    
    Args:
        datos: Datos a verificar.
        hash_esperado: Hash esperado para comparar.
    
    Returns:
        True si los hashes coinciden, False en caso contrario.
    
    Example:
        >>> verificar_hash("test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")
        True
    """
    hash_calculado = calcular_sha256(datos)
    return hash_calculado == hash_esperado

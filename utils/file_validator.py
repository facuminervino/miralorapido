"""
Validación y seguridad de archivos subidos
"""
import os
from pathlib import Path
from typing import Tuple, Optional
import config


def validate_file_extension(filename: str) -> bool:
    """
    Valida que la extensión del archivo sea permitida.

    Args:
        filename: Nombre del archivo

    Returns:
        True si la extensión es válida
    """
    ext = Path(filename).suffix.lower()
    return ext in config.ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> Tuple[bool, Optional[str]]:
    """
    Valida que el tamaño del archivo esté dentro del límite.

    Args:
        file_size: Tamaño del archivo en bytes

    Returns:
        Tuple de (es_válido, mensaje_de_error)
    """
    if file_size > config.MAX_FILE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        return False, f"Archivo muy grande ({size_mb:.1f}MB). Límite: {config.MAX_FILE_SIZE_MB}MB"

    return True, None


def validate_magic_number(file_bytes: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Valida que el archivo tenga los magic numbers correctos (no solo confiar en extensión).

    Args:
        file_bytes: Primeros bytes del archivo
        filename: Nombre del archivo

    Returns:
        Tuple de (es_válido, mensaje_de_error)
    """
    ext = Path(filename).suffix.lower()

    # Obtener magic number esperado
    if ext == '.psd':
        expected_magic = config.MAGIC_NUMBERS['psd']
        if not file_bytes.startswith(expected_magic):
            return False, "El archivo no parece ser un PSD válido"

    elif ext == '.ai':
        expected_magic = config.MAGIC_NUMBERS['ai']
        if not file_bytes.startswith(expected_magic):
            return False, (
                "El archivo AI no parece tener PDF embebido. "
                "Asegúrate de que sea un archivo AI moderno (versión CS o superior)"
            )

    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza el nombre del archivo para prevenir path traversal y otros ataques.

    Args:
        filename: Nombre original del archivo

    Returns:
        Nombre sanitizado
    """
    # Obtener solo el nombre base (sin path)
    filename = os.path.basename(filename)

    # Remover caracteres peligrosos
    dangerous_chars = ['..', '/', '\\', '\x00']
    for char in dangerous_chars:
        filename = filename.replace(char, '')

    # Limitar longitud
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext

    return filename


def validate_uploaded_file(uploaded_file) -> Tuple[bool, Optional[str]]:
    """
    Valida un archivo subido completamente (extensión, tamaño, magic numbers).

    Args:
        uploaded_file: Objeto UploadedFile de Streamlit

    Returns:
        Tuple de (es_válido, mensaje_de_error)
    """
    # Validar extensión
    if not validate_file_extension(uploaded_file.name):
        return False, f"Tipo de archivo no permitido. Solo se aceptan: {', '.join(config.ALLOWED_EXTENSIONS)}"

    # Validar tamaño
    is_valid, error_msg = validate_file_size(uploaded_file.size)
    if not is_valid:
        return False, error_msg

    # Leer primeros bytes para validar magic number
    file_bytes = uploaded_file.read(512)  # Leer primeros 512 bytes
    uploaded_file.seek(0)  # Volver al inicio

    is_valid, error_msg = validate_magic_number(file_bytes, uploaded_file.name)
    if not is_valid:
        return False, error_msg

    return True, None


def get_file_type(filename: str) -> Optional[str]:
    """
    Determina el tipo de archivo basado en la extensión.

    Args:
        filename: Nombre del archivo

    Returns:
        'psd' o 'ai', o None si no es reconocido
    """
    ext = Path(filename).suffix.lower()
    if ext == '.psd':
        return 'psd'
    elif ext == '.ai':
        return 'ai'
    return None

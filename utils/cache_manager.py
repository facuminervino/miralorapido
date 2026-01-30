"""
Gestión de cache y limpieza de archivos temporales
"""
import os
import time
import gc
from pathlib import Path
from typing import List


def cleanup_old_files(directory: str, max_age_seconds: int = 900) -> int:
    """
    Limpia archivos temporales más antiguos que max_age_seconds.

    Args:
        directory: Directorio a limpiar
        max_age_seconds: Edad máxima en segundos (por defecto 15 minutos)

    Returns:
        Número de archivos eliminados
    """
    if not os.path.exists(directory):
        return 0

    current_time = time.time()
    deleted_count = 0

    try:
        for filepath in Path(directory).glob('**/*'):
            if filepath.is_file():
                file_age = current_time - filepath.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        filepath.unlink()
                        deleted_count += 1
                    except Exception:
                        pass  # Ignorar errores al eliminar archivos individuales

    except Exception:
        pass  # Ignorar errores de lectura de directorio

    return deleted_count


def get_directory_size(directory: str) -> int:
    """
    Calcula el tamaño total de un directorio en bytes.

    Args:
        directory: Path del directorio

    Returns:
        Tamaño total en bytes
    """
    total_size = 0

    try:
        for filepath in Path(directory).glob('**/*'):
            if filepath.is_file():
                total_size += filepath.stat().st_size
    except Exception:
        pass

    return total_size


def force_garbage_collection():
    """
    Fuerza garbage collection agresivo para liberar memoria.
    Útil después de procesar archivos grandes.
    """
    gc.collect()
    gc.collect()  # Dos veces para asegurar limpieza completa
    gc.collect()


def cleanup_streamlit_cache(max_age_seconds: int = 900):
    """
    Limpia el cache de Streamlit de archivos antiguos.

    Args:
        max_age_seconds: Edad máxima en segundos (por defecto 15 minutos)
    """
    # Streamlit guarda cache en diferentes ubicaciones según el OS
    cache_dirs = [
        os.path.join(os.path.expanduser("~"), ".streamlit", "cache"),
        "/tmp/streamlit",
    ]

    total_deleted = 0
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            deleted = cleanup_old_files(cache_dir, max_age_seconds)
            total_deleted += deleted

    return total_deleted

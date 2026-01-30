"""
Procesador de archivos PSD optimizado para archivos grandes (50-100MB)
"""
import gc
from io import BytesIO
from typing import Tuple, Optional
from PIL import Image
from psd_tools import PSDImage
import config


def process_psd_for_preview(psd_file, max_size: int = None) -> Tuple[Image.Image, Tuple[int, int]]:
    """
    Genera preview optimizado para Streamlit Cloud (1GB RAM).

    Args:
        psd_file: Archivo PSD (path o BytesIO)
        max_size: Tamaño máximo en píxeles (por defecto usa config.MAX_PREVIEW_SIZE)

    Returns:
        Tuple de (imagen_preview, dimensiones_originales)
    """
    if max_size is None:
        max_size = config.MAX_PREVIEW_SIZE

    psd = None
    composite = None

    try:
        # Abrir archivo PSD
        psd = PSDImage.open(psd_file)
        original_size = (psd.width, psd.height)

        # Extraer composite (imagen aplanada)
        composite = psd.composite()

        # Convertir CMYK a RGB si es necesario
        if composite.mode == 'CMYK':
            composite = composite.convert('RGB')

        # Convertir 16-bit a 8-bit si es necesario
        if composite.mode == 'I' or composite.mode == 'I;16':
            composite = composite.convert('RGB')

        # Si es muy grande, reducir inmediatamente para ahorrar RAM
        if max(composite.size) > max_size:
            ratio = max_size / max(composite.size)
            new_size = (int(composite.width * ratio), int(composite.height * ratio))
            composite = composite.resize(new_size, Image.Resampling.LANCZOS)

        # Asegurar que tenga modo RGB o RGBA
        if composite.mode not in ('RGB', 'RGBA'):
            if composite.mode == 'L':  # Grayscale
                composite = composite.convert('RGB')
            elif composite.mode == 'LA':  # Grayscale with alpha
                composite = composite.convert('RGBA')

        return composite, original_size

    except Exception as e:
        raise RuntimeError(f"Error procesando archivo PSD: {str(e)}")

    finally:
        # Limpieza agresiva de memoria
        if psd is not None:
            try:
                psd._record = None  # Liberar estructura interna
            except:
                pass
        del psd
        gc.collect()


def process_psd_for_download(psd_file, format: str = 'PNG') -> BytesIO:
    """
    Genera imagen full resolution solo al descargar.

    Args:
        psd_file: Archivo PSD (path o BytesIO)
        format: Formato de salida ('PNG' o 'JPEG')

    Returns:
        BytesIO con la imagen en el formato especificado
    """
    psd = None
    composite = None

    try:
        # Abrir archivo PSD
        psd = PSDImage.open(psd_file)

        # Extraer composite en resolución completa
        composite = psd.composite()

        # Convertir CMYK a RGB si es necesario
        if composite.mode == 'CMYK':
            composite = composite.convert('RGB')

        # Para JPG, convertir a RGB (sin transparencia)
        if format.upper() == 'JPEG' or format.upper() == 'JPG':
            if composite.mode == 'RGBA':
                # Crear fondo blanco
                background = Image.new('RGB', composite.size, (255, 255, 255))
                background.paste(composite, mask=composite.split()[-1])  # Usar alpha como máscara
                composite = background
            elif composite.mode != 'RGB':
                composite = composite.convert('RGB')

        # Guardar en BytesIO
        output = BytesIO()

        if format.upper() == 'PNG':
            composite.save(output, format='PNG', optimize=True)
        elif format.upper() in ('JPEG', 'JPG'):
            composite.save(output, format='JPEG', quality=config.JPG_QUALITY, optimize=True)
        else:
            raise ValueError(f"Formato no soportado: {format}")

        output.seek(0)
        return output

    except Exception as e:
        raise RuntimeError(f"Error generando descarga: {str(e)}")

    finally:
        # Limpieza agresiva de memoria
        del composite
        if psd is not None:
            try:
                psd._record = None
            except:
                pass
        del psd
        gc.collect()


def get_psd_info(psd_file) -> dict:
    """
    Extrae información básica del archivo PSD sin procesar la imagen completa.

    Args:
        psd_file: Archivo PSD (path o BytesIO)

    Returns:
        Dict con información del archivo (width, height, channels, color_mode)
    """
    psd = None

    try:
        psd = PSDImage.open(psd_file)

        info = {
            'width': psd.width,
            'height': psd.height,
            'channels': psd.channels,
            'depth': psd.depth,
            'color_mode': psd.color_mode.name if hasattr(psd.color_mode, 'name') else str(psd.color_mode),
        }

        return info

    except Exception as e:
        raise RuntimeError(f"Error leyendo información del PSD: {str(e)}")

    finally:
        if psd is not None:
            try:
                psd._record = None
            except:
                pass
        del psd
        gc.collect()

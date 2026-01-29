"""
Procesador de archivos AI (Adobe Illustrator) usando PyMuPDF.
Los archivos AI modernos (CS+) son PDF-compatibles.
"""
import gc
from io import BytesIO
from typing import Tuple, Optional
from PIL import Image
import fitz  # PyMuPDF
import config


def process_ai_for_preview(ai_file, max_size: int = None, dpi: int = 150) -> Tuple[Image.Image, Tuple[int, int]]:
    """
    Genera preview optimizado de archivo AI.

    Args:
        ai_file: Archivo AI (path o BytesIO)
        max_size: Tamaño máximo en píxeles (por defecto usa config.MAX_PREVIEW_SIZE)
        dpi: DPI para renderizar (150 para preview, más bajo que descarga)

    Returns:
        Tuple de (imagen_preview, dimensiones_originales)
    """
    if max_size is None:
        max_size = config.MAX_PREVIEW_SIZE

    doc = None

    try:
        # Abrir archivo AI como PDF
        if isinstance(ai_file, BytesIO):
            doc = fitz.open(stream=ai_file.read(), filetype="pdf")
        else:
            doc = fitz.open(ai_file)

        # Verificar que tiene al menos una página
        if len(doc) == 0:
            raise ValueError("El archivo AI no contiene páginas")

        # Obtener primera página
        page = doc[0]

        # Dimensiones originales (en puntos, convertir a píxeles)
        rect = page.rect
        original_size = (int(rect.width), int(rect.height))

        # Calcular matriz de transformación para preview
        # DPI más bajo para preview rápido
        zoom = dpi / 72  # 72 DPI es la base de PyMuPDF
        mat = fitz.Matrix(zoom, zoom)

        # Renderizar página a pixmap
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Convertir pixmap a PIL Image
        img_data = pix.samples
        img = Image.frombytes("RGB", [pix.width, pix.height], img_data)

        # Si es muy grande, reducir aún más
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        return img, original_size

    except fitz.FileDataError:
        raise RuntimeError(
            "No se pudo abrir el archivo AI. \n\n"
            "💡 Solución: En Illustrator, guarda el archivo con la opción:\n"
            "   ✓ Create PDF Compatible File\n\n"
            "Esto es necesario para que el visualizador pueda leerlo."
        )
    except Exception as e:
        raise RuntimeError(f"Error procesando archivo AI: {str(e)}")

    finally:
        # Limpieza de memoria
        if doc is not None:
            doc.close()
        del doc
        gc.collect()


def process_ai_for_download(ai_file, format: str = 'PNG', dpi: int = None) -> BytesIO:
    """
    Genera imagen de alta resolución del archivo AI para descarga.

    Args:
        ai_file: Archivo AI (path o BytesIO)
        format: Formato de salida ('PNG' o 'JPEG')
        dpi: DPI para renderizar (por defecto usa config.DOWNLOAD_DPI)

    Returns:
        BytesIO con la imagen en el formato especificado
    """
    if dpi is None:
        dpi = config.DOWNLOAD_DPI

    doc = None

    try:
        # Abrir archivo AI como PDF
        if isinstance(ai_file, BytesIO):
            doc = fitz.open(stream=ai_file.read(), filetype="pdf")
        else:
            doc = fitz.open(ai_file)

        if len(doc) == 0:
            raise ValueError("El archivo AI no contiene páginas")

        # Obtener primera página
        page = doc[0]

        # Calcular matriz de transformación para alta resolución
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        # Renderizar página a pixmap
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Convertir pixmap a PIL Image
        img_data = pix.samples
        img = Image.frombytes("RGB", [pix.width, pix.height], img_data)

        # Guardar en BytesIO
        output = BytesIO()

        if format.upper() == 'PNG':
            img.save(output, format='PNG', optimize=True)
        elif format.upper() in ('JPEG', 'JPG'):
            img.save(output, format='JPEG', quality=config.JPG_QUALITY, optimize=True)
        else:
            raise ValueError(f"Formato no soportado: {format}")

        output.seek(0)
        return output

    except fitz.FileDataError:
        raise RuntimeError(
            "No se pudo abrir el archivo AI. \n\n"
            "💡 Solución: En Illustrator, guarda el archivo con la opción:\n"
            "   ✓ Create PDF Compatible File\n\n"
            "Esto es necesario para que el visualizador pueda leerlo."
        )
    except Exception as e:
        raise RuntimeError(f"Error generando descarga: {str(e)}")

    finally:
        # Limpieza de memoria
        if doc is not None:
            doc.close()
        del doc
        gc.collect()


def get_ai_info(ai_file) -> dict:
    """
    Extrae información básica del archivo AI.

    Args:
        ai_file: Archivo AI (path o BytesIO)

    Returns:
        Dict con información del archivo (width, height, pages)
    """
    doc = None

    try:
        # Abrir archivo AI como PDF
        if isinstance(ai_file, BytesIO):
            doc = fitz.open(stream=ai_file.read(), filetype="pdf")
        else:
            doc = fitz.open(ai_file)

        if len(doc) == 0:
            raise ValueError("El archivo AI no contiene páginas")

        # Obtener información de la primera página
        page = doc[0]
        rect = page.rect

        info = {
            'width': int(rect.width),
            'height': int(rect.height),
            'pages': len(doc),
            'format': 'AI (PDF-compatible)',
        }

        return info

    except fitz.FileDataError:
        raise RuntimeError(
            "No se pudo abrir el archivo AI. "
            "Probablemente sea un archivo AI legacy (< CS) sin PDF embebido."
        )
    except Exception as e:
        raise RuntimeError(f"Error leyendo información del AI: {str(e)}")

    finally:
        if doc is not None:
            doc.close()
        del doc
        gc.collect()

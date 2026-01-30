"""
Utilidades comunes para manipulación de imágenes
"""
from io import BytesIO
from PIL import Image
import config


def image_to_bytes(img: Image.Image, format: str = 'PNG') -> BytesIO:
    """
    Convierte una imagen PIL a bytes.

    Args:
        img: Imagen PIL
        format: Formato de salida ('PNG' o 'JPEG')

    Returns:
        BytesIO con la imagen
    """
    output = BytesIO()

    # Preparar imagen según formato
    if format.upper() in ('JPEG', 'JPG'):
        # JPG no soporta transparencia, convertir a RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            # Crear fondo blanco
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if 'A' in img.mode:  # Tiene canal alpha
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(output, format='JPEG', quality=config.JPG_QUALITY, optimize=True)

    else:  # PNG
        # Asegurar que tenga modo adecuado
        if img.mode not in ('RGB', 'RGBA', 'L', 'LA'):
            if 'A' in img.mode or img.mode == 'P':
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')

        img.save(output, format='PNG', optimize=True)

    output.seek(0)
    return output


def resize_image(img: Image.Image, max_size: int) -> Image.Image:
    """
    Redimensiona una imagen manteniendo aspect ratio.

    Args:
        img: Imagen PIL
        max_size: Tamaño máximo en píxeles (para el lado más largo)

    Returns:
        Imagen redimensionada
    """
    if max(img.size) <= max_size:
        return img

    ratio = max_size / max(img.size)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def add_white_background(img: Image.Image) -> Image.Image:
    """
    Agrega fondo blanco a una imagen con transparencia.

    Args:
        img: Imagen PIL (puede tener alpha)

    Returns:
        Imagen RGB con fondo blanco
    """
    if img.mode not in ('RGBA', 'LA'):
        return img.convert('RGB')

    background = Image.new('RGB', img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[-1])
    return background


def format_file_size(size_bytes: int) -> str:
    """
    Formatea el tamaño de archivo en formato legible.

    Args:
        size_bytes: Tamaño en bytes

    Returns:
        String formateado (ej: "2.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

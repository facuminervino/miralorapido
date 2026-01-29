"""
Configuración centralizada de la aplicación
"""

# Límites de archivo
MAX_FILE_SIZE_MB = 100  # Aumentado a 100MB
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'.psd', '.ai'}

# Configuración de procesamiento
MAX_PREVIEW_SIZE = 1200  # Máximo tamaño en píxeles para preview (optimizado para Streamlit Cloud)
DOWNLOAD_DPI = 300  # DPI para archivos AI al descargar

# Configuración de cache
CACHE_TTL_SECONDS = 300  # 5 minutos (agresivo para Streamlit Cloud)

# Calidad de exportación
JPG_QUALITY = 85  # Calidad por defecto para JPG (0-100)

# Magic numbers para validación
MAGIC_NUMBERS = {
    'psd': b'8BPS',  # Adobe Photoshop
    'ai': b'%PDF',   # AI moderno (PDF-compatible)
}

# Timeout de procesamiento
PROCESSING_TIMEOUT_SECONDS = 30

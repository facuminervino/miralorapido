"""
Configuración de Analytics y Tracking
Google Analytics 4 + Hotjar
"""

# ============================================
# CONFIGURACIÓN DE GOOGLE ANALYTICS 4
# ============================================
# Instrucciones para obtener el Measurement ID:
# 1. Ve a https://analytics.google.com/
# 2. Crea una cuenta y propiedad para "Miralo Rápido"
# 3. Copia el Measurement ID (formato: G-XXXXXXXXXX)
# 4. Reemplaza el valor abajo

GA4_MEASUREMENT_ID = "G-9NWVH8V2NY"  # Google Analytics 4 Measurement ID


# ============================================
# CONFIGURACIÓN DE HOTJAR
# ============================================
# Instrucciones para obtener el Site ID:
# 1. Ve a https://www.hotjar.com/
# 2. Registrate gratis (hasta 35 sesiones/día)
# 3. Agrega tu sitio: miralorapido.streamlit.app
# 4. Copia el Site ID (número, ej: 1234567)
# 5. Reemplaza el valor abajo

HOTJAR_SITE_ID = "8c89e971423b2"  # Hotjar/Contentsquare Site ID


# ============================================
# EVENTOS PERSONALIZADOS A TRACKEAR
# ============================================
TRACK_EVENTS = {
    "file_upload": True,          # Cuando se sube un archivo
    "file_processed": True,       # Cuando se procesa exitosamente
    "download_png": True,         # Cuando se descarga PNG
    "download_jpg": True,         # Cuando se descarga JPG
    "error_occurred": True,       # Cuando hay un error
    "file_size_exceeded": True,   # Cuando el archivo es muy grande
}


# ============================================
# MÉTRICAS A MEDIR
# ============================================
# Estas métricas se trackean automáticamente:
# - Usuarios únicos/día
# - Sesiones/día
# - Archivos procesados/día
# - Tipos de archivo (PSD vs AI)
# - Tamaño promedio de archivos
# - Formatos de descarga (PNG vs JPG)
# - Tasa de error
# - Tasa de retorno (usuarios recurrentes)
# - Tiempo en página
# - Bounce rate

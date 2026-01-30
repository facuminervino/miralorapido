"""
Utilidades para Analytics y Tracking de Eventos
Integración con Google Analytics 4
"""
import streamlit as st
from datetime import datetime
import analytics_config


def inject_google_analytics():
    """
    Inyecta el código de Google Analytics 4 en la página
    """
    ga_id = analytics_config.GA4_MEASUREMENT_ID

    # Solo inyectar si hay un ID válido configurado
    if ga_id and ga_id != "G-XXXXXXXXXX":
        ga_code = f"""
        <!-- Google Analytics 4 -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{ga_id}', {{
            'send_page_view': true,
            'cookie_flags': 'SameSite=None;Secure'
          }});
        </script>
        """
        st.markdown(ga_code, unsafe_allow_html=True)


def inject_hotjar():
    """
    Inyecta el código de Hotjar para heatmaps y grabaciones
    """
    hotjar_id = analytics_config.HOTJAR_SITE_ID

    # Solo inyectar si hay un ID válido configurado
    if hotjar_id and hotjar_id != "0000000":
        hotjar_code = f"""
        <!-- Hotjar Tracking Code -->
        <script>
            (function(h,o,t,j,a,r){{
                h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
                h._hjSettings={{hjid:{hotjar_id},hjsv:6}};
                a=o.getElementsByTagName('head')[0];
                r=o.createElement('script');r.async=1;
                r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                a.appendChild(r);
            }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        </script>
        """
        st.markdown(hotjar_code, unsafe_allow_html=True)


def track_event(event_name, event_params=None):
    """
    Trackea un evento personalizado en Google Analytics 4

    Args:
        event_name: Nombre del evento (ej: 'file_upload', 'download_png')
        event_params: Diccionario con parámetros adicionales del evento
    """
    # Verificar si el evento está habilitado en la configuración
    if not analytics_config.TRACK_EVENTS.get(event_name, False):
        return

    ga_id = analytics_config.GA4_MEASUREMENT_ID

    # Solo trackear si GA4 está configurado
    if ga_id and ga_id != "G-XXXXXXXXXX":
        params = event_params or {}

        # Convertir parámetros a formato JavaScript
        params_str = ", ".join([f"'{k}': '{v}'" for k, v in params.items()])

        event_code = f"""
        <script>
          if (typeof gtag !== 'undefined') {{
            gtag('event', '{event_name}', {{{params_str}}});
          }}
        </script>
        """
        st.markdown(event_code, unsafe_allow_html=True)


def track_file_upload(file_type, file_size_mb):
    """
    Trackea cuando un archivo es subido

    Args:
        file_type: Tipo de archivo ('psd' o 'ai')
        file_size_mb: Tamaño del archivo en MB
    """
    track_event('file_upload', {
        'file_type': file_type,
        'file_size_mb': f'{file_size_mb:.2f}',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def track_file_processed(file_type, file_size_mb, processing_time_seconds):
    """
    Trackea cuando un archivo es procesado exitosamente

    Args:
        file_type: Tipo de archivo ('psd' o 'ai')
        file_size_mb: Tamaño del archivo en MB
        processing_time_seconds: Tiempo de procesamiento en segundos
    """
    track_event('file_processed', {
        'file_type': file_type,
        'file_size_mb': f'{file_size_mb:.2f}',
        'processing_time': f'{processing_time_seconds:.2f}',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def track_download(download_format, file_type, file_size_mb):
    """
    Trackea cuando se descarga un archivo

    Args:
        download_format: Formato de descarga ('png' o 'jpg')
        file_type: Tipo de archivo original ('psd' o 'ai')
        file_size_mb: Tamaño del archivo original en MB
    """
    event_name = f'download_{download_format.lower()}'
    track_event(event_name, {
        'download_format': download_format,
        'original_file_type': file_type,
        'original_file_size_mb': f'{file_size_mb:.2f}',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def track_error(error_type, error_message, file_type=None):
    """
    Trackea cuando ocurre un error

    Args:
        error_type: Tipo de error (ej: 'processing_error', 'file_too_large')
        error_message: Mensaje de error
        file_type: Tipo de archivo (opcional)
    """
    params = {
        'error_type': error_type,
        'error_message': error_message[:100],  # Limitar a 100 caracteres
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if file_type:
        params['file_type'] = file_type

    track_event('error_occurred', params)


def track_file_size_exceeded(file_size_mb, max_size_mb):
    """
    Trackea cuando un archivo excede el límite de tamaño

    Args:
        file_size_mb: Tamaño del archivo subido en MB
        max_size_mb: Límite máximo permitido en MB
    """
    track_event('file_size_exceeded', {
        'file_size_mb': f'{file_size_mb:.2f}',
        'max_size_mb': f'{max_size_mb}',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def initialize_analytics():
    """
    Inicializa todos los servicios de analytics
    Debe ser llamado al inicio de la aplicación
    """
    inject_google_analytics()
    inject_hotjar()

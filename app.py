"""
Visualizador de Archivos PSD y AI
Aplicación web para previsualizar y convertir archivos de Adobe Photoshop e Illustrator
"""
import streamlit as st
from io import BytesIO
import time
import config
from utils.file_validator import validate_uploaded_file, get_file_type, sanitize_filename
from utils.cache_manager import force_garbage_collection
from utils.analytics import initialize_analytics, track_file_upload, track_file_processed, track_download, track_error, track_file_size_exceeded
from processors.psd_processor import process_psd_for_preview, process_psd_for_download
from processors.ai_processor import process_ai_for_preview, process_ai_for_download
from processors.image_utils import format_file_size


# Configuración de la página con SEO optimizado
st.set_page_config(
    page_title="Miralo Rápido ⚡ Convertir PSD y AI a PNG/JPG Online Gratis | Sin Photoshop",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Convertí archivos PSD de Photoshop y AI de Illustrator a PNG/JPG sin instalar Adobe. Gratis, online, hasta 100MB."
    }
)

# Inicializar Analytics (Google Analytics 4 + Hotjar)
initialize_analytics()

# Meta tags SEO
st.markdown("""
<meta name="description" content="Convertí archivos PSD de Photoshop y AI de Illustrator a PNG o JPG gratis. Sin instalar software. Hasta 100MB. Visualizador online instantáneo para diseñadores, PMs y brand managers.">
<meta name="keywords" content="convertir psd a png, convertir ai a jpg, abrir psd sin photoshop, abrir ai sin illustrator, visualizador psd online, convertidor illustrator gratis, psd to png, ai to jpg, photoshop online gratis, illustrator online gratis">
<meta name="author" content="Miralo Rápido">
<meta name="robots" content="index, follow">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://miralorapido.streamlit.app/">
<meta property="og:title" content="Miralo Rápido ⚡ Convertir PSD y AI a PNG/JPG Online Gratis">
<meta property="og:description" content="Convertí archivos de Photoshop (.psd) e Illustrator (.ai) a PNG/JPG sin instalar nada. Gratis, rápido, hasta 100MB.">
<meta property="og:image" content="https://miralorapido.streamlit.app/~/+/media/og-image.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://miralorapido.streamlit.app/">
<meta property="twitter:title" content="Miralo Rápido ⚡ Convertir PSD y AI Online Gratis">
<meta property="twitter:description" content="Convertí PSD y AI a PNG/JPG sin Photoshop ni Illustrator. Gratis, online, hasta 100MB.">
<meta property="twitter:image" content="https://miralorapido.streamlit.app/~/+/media/og-image.png">

<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Miralo Rápido",
  "url": "https://miralorapido.streamlit.app/",
  "description": "Convertidor online gratuito de archivos PSD de Photoshop y AI de Illustrator a PNG/JPG. Sin registro, hasta 100MB.",
  "applicationCategory": "DesignApplication",
  "operatingSystem": "Web Browser",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "featureList": "Convertir PSD a PNG, Convertir AI a JPG, Visualizar archivos Photoshop, Visualizar archivos Illustrator, Sin instalación, Gratis",
  "browserRequirements": "Requires JavaScript. Requires HTML5.",
  "softwareVersion": "1.0",
  "creator": {
    "@type": "Organization",
    "name": "Miralo Rápido"
  }
}
</script>
""", unsafe_allow_html=True)

# CSS personalizado - Estética Retro 00s
st.markdown("""
<style>
    /* Fuentes retro - Tahoma/Verdana style */
    @import url('https://fonts.googleapis.com/css2?family=Tahoma:wght@400;700&family=Courier+Prime:wght@400;700&display=swap');

    * {
        font-family: 'Tahoma', 'Verdana', sans-serif;
    }

    body {
        background: #ece9d8; /* Windows XP Luna background */
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><path d="M0,0 L0,13 L4,9 L6,13 L8,12 L6,8 L11,8 Z" fill="white" stroke="black" stroke-width="1"/></svg>'), auto !important;
    }

    /* Cursor pointer para elementos clickeables */
    button, a, [role="button"] {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="20"><path d="M6,0 L6,6 L0,6 L0,9 L6,9 L6,15 L9,15 L9,9 L15,9 L15,6 L9,6 L9,0 Z" fill="white" stroke="black" stroke-width="1"/></svg>'), pointer !important;
    }

    /* Patrón de fondo retro (sutil) */
    .stApp {
        background-image:
            repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,.03) 2px, rgba(0,0,0,.03) 4px);
    }

    /* Header estilo ventana XP */
    .main-header {
        background: linear-gradient(180deg, #0054e3 0%, #4e98dd 5%, #0054e3 95%, #003db3 100%);
        padding: 0.3rem;
        border-radius: 8px 8px 0 0;
        margin-bottom: 0;
        color: white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        border: 1px solid #0039a6;
    }

    .window-title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.3rem 0.5rem;
        font-size: 0.85rem;
        font-weight: bold;
    }

    .window-content {
        background: #ece9d8;
        border: 2px solid #0039a6;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 2rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }

    .big-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #003db3;
        text-shadow: 2px 2px 0px rgba(255,255,255,0.5);
        margin: 1rem 0;
        font-family: 'Courier Prime', monospace;
    }

    .tagline {
        text-align: center;
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }

    /* Feature cards estilo Windows XP */
    .feature-card {
        background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%);
        padding: 1.2rem;
        border-radius: 6px;
        border: 2px solid #b0b0b0;
        border-right-color: #606060;
        border-bottom-color: #606060;
        margin: 0.8rem 0;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.8), 2px 2px 3px rgba(0,0,0,0.2);
    }

    .feature-card:active {
        border-top-color: #606060;
        border-left-color: #606060;
        border-right-color: #b0b0b0;
        border-bottom-color: #b0b0b0;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.2);
    }

    .feature-card h3 {
        margin-top: 0;
        color: #003db3;
        font-size: 1rem;
    }

    /* Buttons estilo Windows XP */
    .stButton>button {
        background: linear-gradient(180deg, #ffffff 0%, #ece9d8 50%, #d8d0c4 100%);
        border: 2px solid #b0b0b0;
        border-right-color: #606060;
        border-bottom-color: #606060;
        border-radius: 4px;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        font-size: 0.95rem;
        color: #000;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.8), 1px 1px 2px rgba(0,0,0,0.2);
    }

    .stButton>button:hover {
        background: linear-gradient(180deg, #fff8dc 0%, #f0e8d8 50%, #dcd0c4 100%);
    }

    .stButton>button:active {
        border-top-color: #606060;
        border-left-color: #606060;
        border-right-color: #b0b0b0;
        border-bottom-color: #b0b0b0;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.2);
    }

    /* Primary button (estilo botón azul XP) */
    .stButton>button[kind="primary"] {
        background: linear-gradient(180deg, #5fa5ff 0%, #3d8eeb 50%, #0054e3 100%);
        border: 2px solid #003db3;
        color: white;
        font-weight: bold;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.4), 1px 1px 3px rgba(0,0,0,0.3);
    }

    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(180deg, #6fb5ff 0%, #4d9efb 50%, #1064f3 100%);
    }

    /* Upload zone estilo cuadro de diálogo */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 2px solid #b0b0b0;
        border-right-color: #606060;
        border-bottom-color: #606060;
        border-radius: 4px;
        padding: 1.5rem;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.8);
        position: relative;
    }

    /* Agregar texto personalizado en argentino ENCIMA del uploader */
    [data-testid="stFileUploader"]::before {
        content: "📂 ARRASTRÁ TU ARCHIVO ACÁ";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -80px);
        font-size: 1.2rem;
        font-weight: bold;
        color: #003db3;
        pointer-events: none;
        z-index: 10;
        text-align: center;
        width: 100%;
    }

    [data-testid="stFileUploader"]::after {
        content: "o hacé click en 'Browse files'";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -40px);
        font-size: 0.9rem;
        color: #666;
        pointer-events: none;
        z-index: 10;
        text-align: center;
        width: 100%;
    }

    /* Ocultar texto en inglés del uploader */
    [data-testid="stFileUploader"] section > div:first-child {
        visibility: hidden;
        height: 0;
        margin: 0;
        padding: 0;
    }

    /* Estilizar el área de drop */
    [data-testid="stFileUploader"] section {
        border: 3px dashed #003db3 !important;
        border-radius: 8px !important;
        padding: 3rem 2rem !important;
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%) !important;
        min-height: 180px !important;
    }

    /* Botón Browse files */
    [data-testid="stFileUploader"] button {
        margin-top: 3rem !important;
    }

    /* Info boxes estilo XP */
    .stInfo, .stSuccess, .stError {
        border-radius: 4px;
        border: 2px solid;
        padding: 0.8rem;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .stInfo {
        background: #e7f3ff;
        border-color: #5fa5ff;
    }

    .stSuccess {
        background: #dff0d8;
        border-color: #5cb85c;
    }

    .stError {
        background: #f8d7da;
        border-color: #dc3545;
    }

    /* Cards de info con efecto 3D */
    .info-card {
        background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%);
        border: 3px solid #b0b0b0;
        border-right-color: #505050;
        border-bottom-color: #505050;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.9), 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    }

    .info-card-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }

    .info-card-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        font-weight: bold;
    }

    .info-card-value {
        font-size: 1rem;
        color: #003db3;
        font-weight: bold;
        margin-top: 0.2rem;
    }

    /* Separadores estilo barra de herramientas */
    hr {
        border: none;
        border-top: 1px solid #b0b0b0;
        border-bottom: 1px solid #ffffff;
        margin: 1.5rem 0;
    }

    /* Expander estilo menú colapsable XP */
    .streamlit-expanderHeader {
        background: linear-gradient(180deg, #ffffff 0%, #ece9d8 100%);
        border: 2px solid #b0b0b0;
        border-radius: 4px;
        font-weight: bold;
        color: #003db3;
        padding: 0.5rem;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* Dark Mode - Modo Oscuro Retro (Windows Vista/7 Aero Dark) */
    @media (prefers-color-scheme: dark) {
        body {
            background: #1a1a1a !important;
            cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><path d="M0,0 L0,13 L4,9 L6,13 L8,12 L6,8 L11,8 Z" fill="black" stroke="white" stroke-width="1"/></svg>'), auto !important;
        }

        .stApp {
            background: #1a1a1a !important;
            background-image:
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,.03) 2px, rgba(255,255,255,.03) 4px);
        }

        /* Header dark */
        .main-header {
            background: linear-gradient(180deg, #1e3a5f 0%, #2a5a8f 5%, #1e3a5f 95%, #0d1e3a 100%);
            border-color: #2a5a8f;
        }

        .window-content {
            background: #2a2a2a !important;
            border-color: #2a5a8f !important;
        }

        .big-title {
            color: #5fa5ff !important;
            text-shadow: 2px 2px 0px rgba(0,0,0,0.5) !important;
        }

        .tagline {
            color: #ccc !important;
        }

        /* Feature cards dark */
        .feature-card {
            background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%) !important;
            border-color: #4a4a4a !important;
            border-right-color: #1a1a1a !important;
            border-bottom-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }

        .feature-card h3, .feature-card h4 {
            color: #5fa5ff !important;
        }

        .feature-card p {
            color: #ccc !important;
        }

        /* Buttons dark */
        .stButton>button {
            background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 50%, #1a1a1a 100%) !important;
            border-color: #4a4a4a !important;
            border-right-color: #0a0a0a !important;
            border-bottom-color: #0a0a0a !important;
            color: #e0e0e0 !important;
        }

        .stButton>button:hover {
            background: linear-gradient(180deg, #4a4a4a 0%, #3a3a3a 50%, #2a2a2a 100%) !important;
        }

        .stButton>button[kind="primary"] {
            background: linear-gradient(180deg, #3d8eeb 0%, #2a6fbb 50%, #1e5a9f 100%) !important;
            border-color: #2a5a8f !important;
        }

        /* Upload zone dark */
        [data-testid="stFileUploader"] {
            background: #2a2a2a !important;
            border-color: #4a4a4a !important;
            border-right-color: #1a1a1a !important;
            border-bottom-color: #1a1a1a !important;
        }

        [data-testid="stFileUploader"]::before {
            color: #5fa5ff !important;
        }

        [data-testid="stFileUploader"]::after {
            color: #999 !important;
        }

        [data-testid="stFileUploader"] section {
            border-color: #5fa5ff !important;
            background: linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%) !important;
        }

        /* Info cards dark */
        .info-card {
            background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%) !important;
            border-color: #4a4a4a !important;
            border-right-color: #1a1a1a !important;
            border-bottom-color: #1a1a1a !important;
        }

        .info-card-label {
            color: #999 !important;
        }

        .info-card-value {
            color: #5fa5ff !important;
        }

        /* Success/Error boxes dark */
        .stSuccess {
            background: #1a3a1a !important;
            border-color: #3a7a3a !important;
            color: #8fe88f !important;
        }

        .stError {
            background: #3a1a1a !important;
            border-color: #7a3a3a !important;
            color: #ff8f8f !important;
        }

        .stInfo {
            background: #1a2a3a !important;
            border-color: #3a5a7a !important;
            color: #8fc8ff !important;
        }

        /* Expander dark */
        .streamlit-expanderHeader {
            background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%) !important;
            border-color: #4a4a4a !important;
            color: #5fa5ff !important;
        }

        /* Separadores dark */
        hr {
            border-top-color: #3a3a3a !important;
            border-bottom-color: #1a1a1a !important;
        }

        /* Texto general */
        p, span, div {
            color: #e0e0e0;
        }

        /* Links */
        a {
            color: #5fa5ff !important;
        }
    }

    /* Responsive */
    @media (max-width: 768px) {
        .big-title {
            font-size: 1.8rem;
        }
        .tagline {
            font-size: 0.9rem;
        }
        .feature-card {
            padding: 0.8rem;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animación sutil de carga (estilo barra de progreso XP) */
    @keyframes xpLoad {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Función principal de la aplicación"""

    # Hero Header estilo Windows XP - COMPACTO
    st.markdown("""
    <div class="main-header">
        <div class="window-title-bar">
            <span>📁 miralorapido.exe</span>
            <span>□ ✕</span>
        </div>
    </div>
    <div class="window-content" style="padding: 1.5rem;">
        <div class="big-title" style="font-size: 2.2rem; margin: 0.5rem 0;">⚡ MIRALO RÁPIDO</div>
        <div class="tagline" style="margin-bottom: 1rem;">Convertí archivos PSD y AI al toque</div>
    </div>
    """, unsafe_allow_html=True)

    # File uploader INMEDIATAMENTE VISIBLE - sin separador
    uploaded_file = st.file_uploader(
        label="uploader",
        type=['psd', 'ai'],
        help=f"Archivos PSD o AI hasta {config.MAX_FILE_SIZE_MB}MB",
        label_visibility="collapsed"
    )

    # Mostrar formatos soportados estilo retro con íconos
    col_format1, col_format2 = st.columns(2)
    with col_format1:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 0.5rem;'>
            <span style='font-size: 1.5rem;'>🎨</span>
            <span><strong>Photoshop</strong> (.psd)</span>
        </div>
        """, unsafe_allow_html=True)
    with col_format2:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 0.5rem;'>
            <span style='font-size: 1.5rem;'>✒️</span>
            <span><strong>Illustrator</strong> (.ai)</span>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file is None:
        # Value proposition DESPUÉS del uploader - 3 columnas COMPACTAS
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card" style="padding: 0.8rem;">
                <h3>⚡ Velocidad</h3>
                <p style="font-size: 0.85rem;">Preview al toque. Como abrir un .txt</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card" style="padding: 0.8rem;">
                <h3>🌐 Universal</h3>
                <p style="font-size: 0.85rem;">En tu navegador. Sin instalar nada.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card" style="padding: 0.8rem;">
                <h3>💾 Gratis</h3>
                <p style="font-size: 0.85rem;">Sin registro. Sin vueltas.</p>
            </div>
            """, unsafe_allow_html=True)
        # Instrucciones compactas
        st.markdown("---")
        st.markdown("### 📋 CÓMO FUNCIONA")

        step1, step2, step3 = st.columns(3)

        with step1:
            st.markdown("""
            <div class='feature-card' style='text-align: center; padding: 0.8rem;'>
                <div style='font-size: 2rem;'>📂</div>
                <h4 style='color: #003db3; font-size: 0.9rem;'>1. SUBÍS</h4>
                <p style='font-size: 0.85rem;'>Tu archivo<br>.PSD o .AI</p>
            </div>
            """, unsafe_allow_html=True)

        with step2:
            st.markdown("""
            <div class='feature-card' style='text-align: center; padding: 0.8rem;'>
                <div style='font-size: 2rem;'>👀</div>
                <h4 style='color: #003db3; font-size: 0.9rem;'>2. VES</h4>
                <p style='font-size: 0.85rem;'>Preview<br>al instante</p>
            </div>
            """, unsafe_allow_html=True)

        with step3:
            st.markdown("""
            <div class='feature-card' style='text-align: center; padding: 0.8rem;'>
                <div style='font-size: 2rem;'>💾</div>
                <h4 style='color: #003db3; font-size: 0.9rem;'>3. BAJÁS</h4>
                <p style='font-size: 0.85rem;'>PNG o<br>JPEG</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # FAQ estilo Help retro
        with st.expander("❔ PREGUNTAS FRECUENTES"):
            st.markdown("""
            **► ¿Qué archivos acepta?**
            • Photoshop (.psd) - Todas las versiones
            • Illustrator (.ai) - CS en adelante
            • Hasta 100MB por archivo

            **► ¿Es seguro?**
            • Se procesa y se borra automáticamente
            • No guardamos nada en el servidor
            • Conexión HTTPS

            **► ¿Tengo que registrarme?**
            • No. Entrás y lo usás.

            **► Tip para archivos .AI:**
            Cuando guardes desde Illustrator, activá "Create PDF Compatible File"
            """)

        # CTA estilo diálogo de Windows
        st.markdown("---")
        st.markdown("""
        <div class='feature-card' style='text-align: center; padding: 1.2rem;'>
            <div style='font-size: 1.8rem; margin-bottom: 0.3rem;'>👆</div>
            <h3 style='color: #003db3; margin: 0.3rem 0; font-size: 1.1rem;'>¡EMPEZÁ AHORA!</h3>
            <p style='margin: 0.3rem 0; font-size: 0.9rem;'>Arrastrá tu archivo arriba ↑</p>
            <small style='color: #666;'>Sin instalar nada</small>
        </div>
        """, unsafe_allow_html=True)

        return

    # Validar archivo
    is_valid, error_msg = validate_uploaded_file(uploaded_file)

    if not is_valid:
        # Trackear error de validación
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > config.MAX_FILE_SIZE_MB:
            track_file_size_exceeded(file_size_mb, config.MAX_FILE_SIZE_MB)
        else:
            track_error('validation_error', error_msg)
        st.error(f"❌ {error_msg}")
        return

    # Información del archivo con diseño mejorado
    file_type = get_file_type(uploaded_file.name)
    file_size_str = format_file_size(uploaded_file.size)
    file_size_mb = uploaded_file.size / (1024 * 1024)

    # Trackear upload exitoso
    track_file_upload(file_type, file_size_mb)

    st.markdown("---")
    st.success("✓ Archivo cargado correctamente")

    # Info cards estilo panel de propiedades
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='info-card'>
            <div class='info-card-icon'>📄</div>
            <div class='info-card-label'>ARCHIVO</div>
            <div class='info-card-value'>{sanitize_filename(uploaded_file.name)[:18]}...</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='info-card'>
            <div class='info-card-icon'>🎨</div>
            <div class='info-card-label'>TIPO</div>
            <div class='info-card-value'>.{file_type.upper()}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='info-card'>
            <div class='info-card-icon'>💾</div>
            <div class='info-card-label'>TAMAÑO</div>
            <div class='info-card-value'>{file_size_str}</div>
        </div>
        """, unsafe_allow_html=True)

    # Procesar y mostrar preview
    st.markdown("---")
    st.markdown("### 👁️ VISTA PREVIA")

    try:
        with st.spinner("Procesando archivo..."):
            # Guardar bytes del archivo para descargas posteriores
            uploaded_file.seek(0)  # Asegurarse de estar al inicio
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)  # Volver al inicio para procesamiento

            # Medir tiempo de procesamiento
            start_time = time.time()

            # Procesar según tipo de archivo
            if file_type == 'psd':
                preview_img, original_size = process_psd_for_preview(uploaded_file)
            elif file_type == 'ai':
                preview_img, original_size = process_ai_for_preview(uploaded_file)
            else:
                st.error("Tipo de archivo no soportado")
                return

            # Calcular tiempo de procesamiento y trackear
            processing_time = time.time() - start_time
            track_file_processed(file_type, file_size_mb, processing_time)

            # Mostrar información de dimensiones con cuarto card
            st.markdown(f"""
            <div class='info-card' style='max-width: 300px; margin: 0 auto 1rem auto;'>
                <div class='info-card-icon'>📐</div>
                <div class='info-card-label'>RESOLUCIÓN</div>
                <div class='info-card-value'>{original_size[0]} × {original_size[1]} px</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Mostrar preview con marco retro
            st.image(
                preview_img,
                caption=f"Preview optimizado | Original: {original_size[0]}×{original_size[1]}px",
                width='stretch'
            )

            # Guardar en session state para descargas
            st.session_state['file_bytes'] = file_bytes
            st.session_state['file_name'] = uploaded_file.name
            st.session_state['file_type'] = file_type
            st.session_state['original_size'] = original_size

            # Limpieza de memoria después de mostrar preview
            force_garbage_collection()

    except MemoryError:
        track_error('memory_error', f'File too large: {file_size_mb:.2f}MB', file_type)
        st.error(
            f"⚠️ Archivo muy pesado para procesar. "
            f"Límite: {config.MAX_FILE_SIZE_MB}MB. "
            "Probá con una versión más chica."
        )
        return

    except Exception as e:
        track_error('processing_error', str(e), file_type)
        st.error(f"❌ Error procesando archivo: {str(e)}")
        return

    # Sección de descarga estilo guardado
    st.markdown("---")
    st.markdown("### 💾 GUARDAR COMO...")
    st.markdown("*Elegí el formato:*")

    col_png, col_jpg = st.columns(2)

    with col_png:
        if st.button("💾 GUARDAR PNG", width='stretch', type="primary"):
            with st.spinner("Generando PNG en alta resolución..."):
                try:
                    # Crear BytesIO desde los bytes guardados
                    from io import BytesIO
                    file_stream = BytesIO(st.session_state['file_bytes'])

                    # Generar archivo en resolución completa
                    if file_type == 'psd':
                        output_bytes = process_psd_for_download(
                            file_stream,
                            format='PNG'
                        )
                    else:  # ai
                        output_bytes = process_ai_for_download(
                            file_stream,
                            format='PNG'
                        )

                    # Preparar nombre de descarga
                    original_name = sanitize_filename(st.session_state['file_name'])
                    download_name = original_name.rsplit('.', 1)[0] + '.png'

                    # Trackear descarga PNG
                    track_download('PNG', st.session_state['file_type'], file_size_mb)

                    # Botón de descarga
                    st.download_button(
                        label="⬇️ DESCARGAR PNG AHORA",
                        data=output_bytes,
                        file_name=download_name,
                        mime="image/png"
                    )

                    st.success("✓ PNG listo para bajar")

                    # Limpieza de memoria
                    force_garbage_collection()

                except MemoryError:
                    st.error("⚠️ Archivo muy pesado. Probá con uno más chico.")
                except Exception as e:
                    st.error(f"❌ Error generando PNG: {str(e)}")

    with col_jpg:
        if st.button("💾 GUARDAR JPG", width='stretch'):
            with st.spinner("Generando JPG en alta resolución..."):
                try:
                    # Crear BytesIO desde los bytes guardados
                    from io import BytesIO
                    file_stream = BytesIO(st.session_state['file_bytes'])

                    # Generar archivo en resolución completa
                    if file_type == 'psd':
                        output_bytes = process_psd_for_download(
                            file_stream,
                            format='JPEG'
                        )
                    else:  # ai
                        output_bytes = process_ai_for_download(
                            file_stream,
                            format='JPEG'
                        )

                    # Preparar nombre de descarga
                    original_name = sanitize_filename(st.session_state['file_name'])
                    download_name = original_name.rsplit('.', 1)[0] + '.jpg'

                    # Trackear descarga JPG
                    track_download('JPG', st.session_state['file_type'], file_size_mb)

                    # Botón de descarga
                    st.download_button(
                        label="⬇️ DESCARGAR JPG AHORA",
                        data=output_bytes,
                        file_name=download_name,
                        mime="image/jpeg"
                    )

                    st.success("✓ JPG listo (con fondo blanco)")

                    # Limpieza de memoria
                    force_garbage_collection()

                except MemoryError:
                    st.error("⚠️ Archivo muy pesado. Probá con uno más chico.")
                except Exception as e:
                    st.error(f"❌ Error generando JPG: {str(e)}")

    # Nota sobre formatos estilo tooltip
    st.markdown("""
    <div class='feature-card' style='background: #fffacd; margin-top: 1rem; padding: 0.8rem;'>
        <strong style='font-size: 0.9rem;'>ℹ️ GUÍA RÁPIDA:</strong><br>
        <span style='font-size: 0.85rem;'><strong>PNG</strong> → Con transparencias | Más pesado<br>
        <strong>JPG</strong> → Fondo blanco | Más liviano</span>
    </div>
    """, unsafe_allow_html=True)

    # Footer estilo barra de estado Windows
    st.markdown("---")
    st.markdown("""
    <div class='feature-card' style='text-align: center; padding: 1.2rem; margin-top: 1.5rem;'>
        <h2 style='color: #003db3; margin-top: 0; font-size: 1.5rem;'>⚡ MIRALO RÁPIDO</h2>
        <p style='color: #666; margin-bottom: 0.8rem; font-size: 0.9rem;'>El conversor que no te olvidás</p>
        <div style='display: flex; justify-content: center; gap: 1.5rem; margin: 0.8rem 0; flex-wrap: wrap; font-size: 0.8rem;'>
            <div>📂 100MB</div>
            <div>⚡ Al toque</div>
            <div>🔒 Privado</div>
            <div>💾 Gratis</div>
        </div>
        <p style='margin-top: 1rem; font-size: 0.7rem; color: #999;'>
            Sin Adobe. Sin instalar. Sin vueltas.<br>
            Hecho para diseñadores y PMs que no tienen tiempo que perder.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Barra de estado estilo Windows
    st.markdown("""
    <div style='text-align: center; margin-top: 1rem; padding: 0.3rem;
                background: linear-gradient(180deg, #f0f0f0 0%, #d8d8d8 100%);
                border: 1px solid #999; border-radius: 4px;
                font-size: 0.7rem; color: #666; font-family: Courier Prime, monospace;'>
        miralorapido.exe | v1.0 | JPG Quality: {config.JPG_QUALITY}% | Ready
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

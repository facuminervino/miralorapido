"""
Visualizador de Archivos PSD y AI
Aplicación web para previsualizar y convertir archivos de Adobe Photoshop e Illustrator
"""
import streamlit as st
from io import BytesIO
import config
from utils.file_validator import validate_uploaded_file, get_file_type, sanitize_filename
from utils.cache_manager import force_garbage_collection
from processors.psd_processor import process_psd_for_preview, process_psd_for_download
from processors.ai_processor import process_ai_for_preview, process_ai_for_download
from processors.image_utils import format_file_size


# Configuración de la página
st.set_page_config(
    page_title="Visualizador PSD/AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    """Función principal de la aplicación"""

    # Header
    st.title("🎨 Visualizador de Archivos PSD y AI")
    st.markdown(
        "Previsualiza archivos de Adobe Photoshop (.psd) e Illustrator (.ai) "
        "sin necesidad de tener el software instalado. Descarga en PNG o JPG."
    )

    # File uploader
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo PSD o AI",
        type=['psd', 'ai'],
        help=f"Tamaño máximo: {config.MAX_FILE_SIZE_MB}MB"
    )

    if uploaded_file is None:
        # Mostrar información cuando no hay archivo
        st.info("👆 Sube un archivo .psd o .ai para comenzar")

        with st.expander("ℹ️ Información sobre formatos soportados"):
            st.markdown("""
            **Archivos PSD (Photoshop):**
            - Todas las versiones de Photoshop
            - Modos de color: RGB, CMYK, Grayscale
            - Se renderiza la imagen completa (todas las capas aplanadas)

            **Archivos AI (Illustrator):**
            - Versiones CS y superiores (con PDF embebido)
            - Solo se renderiza la primera página/artboard
            - Archivos AI legacy (< CS) pueden no ser compatibles

            **💡 Tip para archivos AI:**
            - Al guardar en Illustrator, asegúrate de activar "**Create PDF Compatible File**"
            - Esto garantiza máxima compatibilidad con el visualizador
            - Las fuentes se renderizan con las que estén disponibles en el sistema
            """)

        st.markdown("---")
        st.caption(f"Límite de tamaño: {config.MAX_FILE_SIZE_MB}MB | MVP v1.0")
        return

    # Validar archivo
    is_valid, error_msg = validate_uploaded_file(uploaded_file)

    if not is_valid:
        st.error(f"❌ {error_msg}")
        return

    # Información del archivo
    file_type = get_file_type(uploaded_file.name)
    file_size_str = format_file_size(uploaded_file.size)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info(f"📄 **{sanitize_filename(uploaded_file.name)}** ({file_size_str})")
    with col2:
        st.metric("Tipo", file_type.upper())

    # Procesar y mostrar preview
    st.markdown("---")
    st.subheader("👁️ Preview")

    try:
        with st.spinner("Procesando archivo..."):
            # Guardar bytes del archivo para descargas posteriores
            uploaded_file.seek(0)  # Asegurarse de estar al inicio
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)  # Volver al inicio para procesamiento

            # Procesar según tipo de archivo
            if file_type == 'psd':
                preview_img, original_size = process_psd_for_preview(uploaded_file)
            elif file_type == 'ai':
                preview_img, original_size = process_ai_for_preview(uploaded_file)
            else:
                st.error("Tipo de archivo no soportado")
                return

            # Mostrar información de dimensiones
            with col3:
                st.metric("Dimensiones", f"{original_size[0]}×{original_size[1]}px")

            # Mostrar preview
            st.image(
                preview_img,
                caption=f"Preview (optimizado para web - dimensiones originales: {original_size[0]}×{original_size[1]}px)",
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
        st.error(
            f"⚠️ Archivo muy grande para procesar. "
            f"Límite recomendado: {config.MAX_FILE_SIZE_MB}MB. "
            "Considera usar una versión reducida del archivo."
        )
        return

    except Exception as e:
        st.error(f"❌ Error procesando archivo: {str(e)}")
        return

    # Sección de descarga
    st.markdown("---")
    st.subheader("💾 Descargar")

    col_png, col_jpg = st.columns(2)

    with col_png:
        if st.button("⬇️ Descargar PNG", width='stretch', type="primary"):
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

                    # Botón de descarga
                    st.download_button(
                        label="📥 Hacer click aquí para descargar PNG",
                        data=output_bytes,
                        file_name=download_name,
                        mime="image/png"
                    )

                    st.success("✅ PNG generado correctamente")

                    # Limpieza de memoria
                    force_garbage_collection()

                except MemoryError:
                    st.error("⚠️ No hay suficiente memoria para generar el archivo completo. Intenta con un archivo más pequeño.")
                except Exception as e:
                    st.error(f"❌ Error generando PNG: {str(e)}")

    with col_jpg:
        if st.button("⬇️ Descargar JPG", width='stretch'):
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

                    # Botón de descarga
                    st.download_button(
                        label="📥 Hacer click aquí para descargar JPG",
                        data=output_bytes,
                        file_name=download_name,
                        mime="image/jpeg"
                    )

                    st.success("✅ JPG generado correctamente (con fondo blanco)")

                    # Limpieza de memoria
                    force_garbage_collection()

                except MemoryError:
                    st.error("⚠️ No hay suficiente memoria para generar el archivo completo. Intenta con un archivo más pequeño.")
                except Exception as e:
                    st.error(f"❌ Error generando JPG: {str(e)}")

    # Nota sobre formatos
    st.caption(
        "💡 **PNG** preserva transparencias | "
        "**JPG** es más liviano pero usa fondo blanco"
    )

    # Footer
    st.markdown("---")
    st.caption(
        f"Límite de tamaño: {config.MAX_FILE_SIZE_MB}MB | "
        f"Calidad JPG: {config.JPG_QUALITY}% | "
        "MVP v1.0"
    )


if __name__ == "__main__":
    main()

# 🎨 Visualizador de Archivos PSD y AI

Aplicación web para previsualizar y convertir archivos de Adobe Photoshop (.psd) e Illustrator (.ai) sin necesidad de tener el software instalado. Descarga tus archivos en formato PNG o JPG.

## ✨ Características

- 📁 **Soporte para PSD y AI**: Abre archivos de Photoshop e Illustrator
- 👁️ **Preview instantáneo**: Visualiza tus archivos en el navegador
- 💾 **Descarga en PNG/JPG**: Exporta en formato de imagen estándar
- ⚡ **Optimizado para archivos grandes**: Soporta archivos de hasta 50-100MB
- 🚀 **Sin instalación**: Funciona completamente en la nube (Streamlit Cloud)

## 🚀 Inicio Rápido

### Opción 1: Usar la App Online (Recomendado)

1. Visita [TU-URL-DE-STREAMLIT-CLOUD]
2. Sube tu archivo .psd o .ai
3. Visualiza y descarga

### Opción 2: Instalación Local

```bash
# Clonar repositorio
git clone <tu-repo-url>
cd visualizador-creatividades

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python test_app.py

# Ejecutar aplicación
streamlit run app.py
```

La aplicación se abrirá en http://localhost:8501

### Opción 3: Docker

```bash
# Build imagen
docker build -t visualizador-creatividades .

# Ejecutar contenedor
docker run -p 8501:8501 visualizador-creatividades
```

Accede en http://localhost:8501

## 📋 Requisitos

### Python
- Python 3.11 o superior
- Dependencias listadas en `requirements.txt`:
  - streamlit >= 1.30.0
  - psd-tools >= 1.9.0
  - Pillow >= 10.0.0
  - PyMuPDF >= 1.23.0

### Sistema (solo para instalación local)
- libgl1-mesa-glx (Linux)
- libglib2.0-0 (Linux)

En Windows y macOS, las dependencias del sistema ya están incluidas con Python.

## 🎯 Uso

### 1. Subir Archivo
- Arrastra y suelta o selecciona un archivo .psd o .ai
- Tamaño máximo: 50MB (configurable)

### 2. Visualizar
- El preview se genera automáticamente
- Se muestra optimizado para web (resolución reducida para velocidad)
- Información del archivo: nombre, tamaño, dimensiones

### 3. Descargar
- **PNG**: Preserva transparencias, ideal para uso en web
- **JPG**: Archivo más liviano con fondo blanco, ideal para impresión

## 🔧 Configuración

Edita `config.py` para ajustar:

```python
MAX_FILE_SIZE_MB = 50        # Límite de tamaño de archivo
MAX_PREVIEW_SIZE = 1200      # Tamaño máximo de preview (px)
DOWNLOAD_DPI = 300           # DPI para archivos AI
JPG_QUALITY = 85             # Calidad JPG (0-100)
CACHE_TTL_SECONDS = 300      # Tiempo de cache (5 min)
```

## 📦 Deploy en Streamlit Cloud

### 1. Preparar Repositorio

```bash
# Inicializar git (si no lo hiciste)
git init
git add .
git commit -m "Initial commit: PSD/AI Visualizer"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio
4. Especifica:
   - **Main file path**: `app.py`
   - **Python version**: 3.11
5. Click en "Deploy"

Tu app estará disponible en: `https://[tu-usuario]-visualizador-creatividades.streamlit.app`

### 3. Configuración de Secrets (opcional)

Si necesitas configurar secrets en Streamlit Cloud:
1. Ve a tu app en Streamlit Cloud
2. Settings > Secrets
3. Agrega configuraciones en formato TOML

## 🎨 Formatos Soportados

### Archivos PSD (Photoshop)
- ✅ Todas las versiones de Photoshop
- ✅ Modos de color: RGB, CMYK, Grayscale
- ✅ 8-bit y 16-bit depth
- ✅ Con o sin capas
- ℹ️ Se renderiza la imagen completa (todas las capas aplanadas)

### Archivos AI (Illustrator)
- ✅ Versiones CS y superiores (con PDF embebido)
- ✅ Solo se renderiza la primera página/artboard
- ⚠️ Archivos AI legacy (< CS) pueden no ser compatibles

## ⚠️ Limitaciones Conocidas

1. **Tamaño de archivo**: Límite de 50MB por defecto (ajustable en config.py)
2. **Archivos AI legacy**: AI < versión CS sin PDF embebido no son compatibles
3. **Fuentes personalizadas**: Pueden no renderizar exactamente igual
4. **Múltiples artboards**: Solo se renderiza el primero en archivos AI
5. **Efectos complejos**: Algunos efectos avanzados pueden verse diferentes

## 🐛 Troubleshooting

### "Archivo muy grande"
- Reduce el tamaño del archivo en Photoshop/Illustrator
- Aumenta `MAX_FILE_SIZE_MB` en `config.py` (solo local)
- En Streamlit Cloud, considera Streamlit Cloud Paid (4GB RAM)

### "No se pudo abrir el archivo AI"
- Asegúrate de que sea AI versión CS o superior
- Al guardar en Illustrator, activa "Create PDF Compatible File"
- Prueba exportar como PDF y usar ese archivo

### "Error de memoria"
- Reduce `MAX_PREVIEW_SIZE` en `config.py`
- Cierra otros archivos/pestañas para liberar RAM
- Considera usar Docker con más RAM asignada

### La app es lenta
- Es normal con archivos > 30MB
- El preview se genera primero (rápido)
- La descarga en full resolution toma más tiempo

## 🛠️ Desarrollo

### Estructura del Proyecto

```
visualizador-creatividades/
├── app.py                      # Aplicación principal Streamlit
├── config.py                   # Configuración
├── processors/                 # Lógica de procesamiento
│   ├── psd_processor.py       # Procesamiento PSD
│   ├── ai_processor.py        # Procesamiento AI
│   └── image_utils.py         # Utilidades de imagen
├── utils/                     # Utilidades
│   ├── file_validator.py     # Validación de archivos
│   └── cache_manager.py      # Gestión de cache
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Configuración Docker
├── packages.txt             # Dependencias sistema (Streamlit Cloud)
├── .streamlit/
│   └── config.toml         # Configuración Streamlit
└── README.md               # Este archivo
```

### Testing

```bash
# Verificar instalación y módulos
python test_app.py

# Ejecutar app en modo desarrollo
streamlit run app.py --server.runOnSave true
```

### Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 🗺️ Roadmap

### v2.0 (Próximas features)
- [ ] Batch processing (múltiples archivos)
- [ ] Zoom interactivo en preview
- [ ] Selector de fondo (transparente/blanco/negro)
- [ ] Slider de calidad JPG
- [ ] Exportar a PDF manteniendo vectores
- [ ] Historial de archivos procesados
- [ ] Comparación lado a lado de archivos
- [ ] Extracción de paleta de colores
- [ ] Soporte para SVG, EPS

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 💬 Soporte

Para reportar bugs o solicitar features:
- Abre un Issue en GitHub
- Email: [tu-email]

## 🙏 Créditos

Desarrollado con:
- [Streamlit](https://streamlit.io) - Framework web
- [psd-tools](https://github.com/psd-tools/psd-tools) - Procesamiento PSD
- [PyMuPDF](https://pymupdf.readthedocs.io/) - Procesamiento AI/PDF
- [Pillow](https://python-pillow.org/) - Manipulación de imágenes

---

**v1.0** - MVP Inicial | Optimizado para archivos grandes en Streamlit Cloud

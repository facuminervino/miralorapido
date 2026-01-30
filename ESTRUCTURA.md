# 📁 Estructura del Proyecto

```
visualizador-creatividades/
│
├── 📄 app.py                          # ⭐ APLICACIÓN PRINCIPAL STREAMLIT
│   └── UI, file upload, preview, descarga
│
├── 📄 config.py                       # ⚙️ CONFIGURACIÓN CENTRALIZADA
│   └── Límites, DPI, calidad, cache TTL
│
├── 📁 processors/                     # 🔧 MÓDULOS DE PROCESAMIENTO
│   ├── __init__.py
│   ├── psd_processor.py              # Procesamiento PSD
│   │   ├── process_psd_for_preview()     → Preview optimizado
│   │   ├── process_psd_for_download()    → Full resolution
│   │   └── get_psd_info()                → Metadata
│   │
│   ├── ai_processor.py               # Procesamiento AI
│   │   ├── process_ai_for_preview()      → Preview optimizado
│   │   ├── process_ai_for_download()     → Full resolution
│   │   └── get_ai_info()                 → Metadata
│   │
│   └── image_utils.py                # Utilidades de imagen
│       ├── image_to_bytes()              → Conversión a bytes
│       ├── resize_image()                → Redimensionar
│       ├── add_white_background()        → Fondo blanco para JPG
│       └── format_file_size()            → Formatear tamaño
│
├── 📁 utils/                          # 🛠️ UTILIDADES
│   ├── __init__.py
│   ├── file_validator.py             # Validación y seguridad
│   │   ├── validate_file_extension()     → Verifica extensión
│   │   ├── validate_file_size()          → Verifica tamaño
│   │   ├── validate_magic_number()       → Verifica magic bytes
│   │   ├── sanitize_filename()           → Sanitiza nombre
│   │   ├── validate_uploaded_file()      → Validación completa
│   │   └── get_file_type()               → Determina tipo
│   │
│   └── cache_manager.py              # Gestión de cache
│       ├── cleanup_old_files()           → Limpia temporales
│       ├── get_directory_size()          → Calcula tamaño
│       ├── force_garbage_collection()    → Libera memoria
│       └── cleanup_streamlit_cache()     → Limpia cache Streamlit
│
├── 📁 .streamlit/                     # ⚙️ CONFIGURACIÓN STREAMLIT
│   └── config.toml                   # Límites upload, CORS, browser
│
├── 📁 tests/                          # 🧪 TESTS (vacío, para futuro)
│
├── 📄 requirements.txt                # 📦 DEPENDENCIAS PYTHON
│   ├── streamlit >= 1.30.0
│   ├── psd-tools >= 1.9.0
│   ├── Pillow >= 10.0.0
│   └── PyMuPDF >= 1.23.0
│
├── 📄 packages.txt                    # 📦 DEPENDENCIAS SISTEMA (Streamlit Cloud)
│   ├── libgl1-mesa-glx
│   └── libglib2.0-0
│
├── 📄 Dockerfile                      # 🐳 CONFIGURACIÓN DOCKER
├── 📄 .dockerignore                   # Archivos ignorados en Docker
├── 📄 .gitignore                      # Archivos ignorados en Git
│
├── 📄 test_app.py                     # ✅ SCRIPT DE TESTING
│   └── Verifica imports, módulos y configuración
│
├── 📄 setup.bat / setup.sh           # 🚀 INSTALACIÓN AUTOMÁTICA
│   └── Crea venv, instala deps, verifica
│
├── 📄 run.bat / run.sh               # ▶️ EJECUTAR APP
│   └── Activa venv y lanza Streamlit
│
├── 📄 README.md                       # 📖 DOCUMENTACIÓN PRINCIPAL
├── 📄 PROXIMOS_PASOS.md              # 📝 GUÍA DE INICIO
├── 📄 ESTRUCTURA.md                   # 📁 ESTE ARCHIVO
└── 📄 LICENSE                         # ⚖️ LICENCIA MIT

```

## 🎯 Flujo de Ejecución

### 1. Usuario Sube Archivo
```
Usuario → app.py → file_validator.validate_uploaded_file()
                   ├── Extensión válida?
                   ├── Tamaño < límite?
                   └── Magic numbers correctos?
```

### 2. Procesar Archivo
```
app.py → get_file_type()
         ├── .psd → psd_processor.process_psd_for_preview()
         │          ├── Abrir con psd-tools
         │          ├── Extraer composite
         │          ├── Convertir color mode
         │          └── Resize si > MAX_PREVIEW_SIZE
         │
         └── .ai  → ai_processor.process_ai_for_preview()
                    ├── Abrir con PyMuPDF (como PDF)
                    ├── Renderizar primera página
                    ├── DPI = 150 (preview)
                    └── Resize si > MAX_PREVIEW_SIZE
```

### 3. Mostrar Preview
```
app.py → st.image(preview_img)
         └── Guardar en session_state para descargas
```

### 4. Usuario Descarga (PNG o JPG)
```
Usuario → Click "Descargar PNG/JPG"
          └── app.py
              ├── PNG → process_*_for_download(format='PNG')
              │         └── Genera full resolution con transparencia
              │
              └── JPG → process_*_for_download(format='JPEG')
                        ├── Genera full resolution
                        └── Agrega fondo blanco (no transparencia)
```

### 5. Limpieza
```
Después de procesar → cache_manager.force_garbage_collection()
                      └── gc.collect() x3 para liberar RAM
```

## 🔐 Seguridad

### Validación de Archivos
1. **Extensión**: Solo `.psd` y `.ai`
2. **Tamaño**: Máximo 50MB (configurable)
3. **Magic Numbers**: Verifica que el archivo sea realmente PSD/AI
4. **Path Traversal**: Sanitiza nombres de archivo
5. **Timeout**: Procesamiento limitado a 30 segundos

### Magic Numbers Verificados
- **PSD**: `8BPS` (0x38425053)
- **AI**: `%PDF` (0x25504446) - AI moderno con PDF embebido

## ⚡ Optimizaciones para Archivos Grandes

### 1. Preview Reducido
- Máximo 1200px → Reduce memoria de ~800MB a ~100MB
- DPI bajo para AI (150 vs 300 en descarga)

### 2. Lazy Loading
- Preview: Generado inmediatamente
- Full Resolution: Solo al hacer click en descargar

### 3. Garbage Collection Agresivo
- Después de procesar preview
- Después de cada descarga
- `gc.collect()` x3 para asegurar limpieza

### 4. Cache con TTL Corto
- 5 minutos (300s)
- Limpieza agresiva para Streamlit Cloud (1GB storage)

### 5. Conversión de Color
- CMYK → RGB automático
- 16-bit → 8-bit automático
- Reduce uso de memoria significativamente

## 📊 Límites de Configuración

| Parámetro | Valor por Defecto | Configurable en |
|-----------|------------------|-----------------|
| Tamaño máximo archivo | 50 MB | `config.py` |
| Preview max size | 1200 px | `config.py` |
| DPI descarga (AI) | 300 | `config.py` |
| Calidad JPG | 85% | `config.py` |
| Cache TTL | 5 min | `config.py` |
| Timeout procesamiento | 30 seg | `config.py` |
| Upload Streamlit | 100 MB | `.streamlit/config.toml` |

## 🎨 Formatos Soportados

### PSD (Photoshop)
- ✅ Todas las versiones
- ✅ RGB, CMYK, Grayscale
- ✅ 8-bit, 16-bit
- ✅ Con/sin capas
- ⚠️ Efectos complejos pueden verse diferentes

### AI (Illustrator)
- ✅ Versión CS y superior (con PDF embebido)
- ✅ Primera página/artboard
- ❌ AI legacy (< CS) sin PDF
- ⚠️ Fuentes custom pueden no renderizar igual

## 🚀 Deploy Options

### 1. Streamlit Cloud (Recomendado para MVP)
- ✅ Gratis
- ✅ HTTPS automático
- ✅ Deploy en ~5 min
- ⚠️ 1GB RAM (límite para archivos grandes)

### 2. Docker Local
- ✅ Control total
- ✅ Recursos personalizables
- ⚠️ Requiere servidor

### 3. Docker en Cloud (AWS/GCP/Azure)
- ✅ Escalable
- ✅ Sin límites de RAM
- ⚠️ Costo mensual

## 📈 Roadmap v2.0

### Alta Prioridad
- [ ] Batch processing
- [ ] Zoom interactivo
- [ ] Progress bar detallado
- [ ] Selector de fondo

### Media Prioridad
- [ ] Slider calidad JPG
- [ ] Historial de archivos
- [ ] Comparación lado a lado
- [ ] Compartir por link

### Baja Prioridad
- [ ] Exportar PDF vectorial
- [ ] Paleta de colores
- [ ] Soporte SVG/EPS
- [ ] API REST

---

**Última actualización:** 2026-01-28 | **Versión:** MVP 1.0

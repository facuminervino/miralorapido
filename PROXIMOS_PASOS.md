# 📝 Próximos Pasos - Visualizador PSD/AI

## ✅ Completado

1. ✅ Estructura del proyecto creada
2. ✅ Módulos de procesamiento PSD y AI implementados
3. ✅ Utilidades de validación y cache
4. ✅ Aplicación Streamlit con UI MVP
5. ✅ Configuración Docker
6. ✅ README completo
7. ✅ Script de testing

## 🚀 Para Empezar a Usar

### 1. Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Verificar Instalación

```bash
python test_app.py
```

Deberías ver:
```
✅ TODOS LOS TESTS PASARON
```

### 3. Ejecutar Localmente

```bash
streamlit run app.py
```

La aplicación se abrirá en http://localhost:8501

### 4. Probar con un Archivo

1. Consigue un archivo .psd o .ai de prueba (preferiblemente pequeño < 10MB para primera prueba)
2. Sube el archivo en la aplicación
3. Verifica que se muestra el preview
4. Prueba descargar en PNG y JPG

## 📤 Deploy a Streamlit Cloud

### Paso 1: Crear Repositorio en GitHub

```bash
# Inicializar git (si no lo hiciste)
git init

# Agregar archivos
git add .

# Primer commit
git commit -m "Initial commit: Visualizador PSD/AI MVP"

# Crear repositorio en GitHub (ve a github.com/new)
# Luego conectar:
git remote add origin https://github.com/TU-USUARIO/visualizador-creatividades.git
git branch -M main
git push -u origin main
```

### Paso 2: Deploy en Streamlit Cloud

1. Ve a https://share.streamlit.io
2. Click en "New app"
3. Conecta tu cuenta de GitHub
4. Selecciona:
   - Repository: `TU-USUARIO/visualizador-creatividades`
   - Branch: `main`
   - Main file path: `app.py`
   - Python version: `3.11`
5. Click "Deploy"

**Tiempo de deploy:** ~5-10 minutos

Tu app estará en: `https://TU-USUARIO-visualizador-creatividades.streamlit.app`

## 🧪 Testing con Archivos Grandes

### Archivos de Prueba Recomendados

1. **Pequeño (< 10MB)**: Para verificar funcionalidad básica
2. **Mediano (10-30MB)**: Testing normal
3. **Grande (30-50MB)**: Testing de límites
4. **Muy grande (> 50MB)**: Debería rechazarse

### Qué Probar

- [x] Upload de archivo PSD
- [x] Upload de archivo AI moderno (CS+)
- [x] Preview se genera correctamente
- [x] Dimensiones son correctas
- [x] Descarga PNG preserva transparencia
- [x] Descarga JPG tiene fondo blanco
- [x] Archivos muy grandes se rechazan
- [x] Mensajes de error son claros

### Métricas a Observar

- Tiempo de procesamiento
- Uso de memoria (especialmente en Streamlit Cloud)
- Calidad del preview vs original
- Tamaño de archivos descargados

## ⚠️ Consideraciones Importantes

### Límite de Archivo Actual: 50MB

Si necesitas aumentarlo:

1. Edita `config.py`:
   ```python
   MAX_FILE_SIZE_MB = 75  # o el valor que necesites
   ```

2. Edita `.streamlit/config.toml`:
   ```toml
   [server]
   maxUploadSize = 100  # debe ser >= a MAX_FILE_SIZE_MB
   ```

3. **IMPORTANTE**: En Streamlit Cloud (1GB RAM), archivos > 50MB pueden causar crashes

### Si Streamlit Cloud Crashea con Archivos Grandes

**Opción 1**: Reducir límite a 30-40MB
```python
MAX_FILE_SIZE_MB = 30
```

**Opción 2**: Upgrade a Streamlit Cloud Paid ($20/mes, 4GB RAM)

**Opción 3**: Deploy en Docker local o VPS con más RAM

## 🔧 Ajustes de Configuración

Edita `config.py` según tus necesidades:

```python
# Archivo más grande aceptado
MAX_FILE_SIZE_MB = 50

# Resolución del preview (menor = más rápido)
MAX_PREVIEW_SIZE = 1200  # píxeles

# DPI para archivos AI al descargar
DOWNLOAD_DPI = 300  # más alto = mejor calidad pero más lento

# Calidad JPG
JPG_QUALITY = 85  # 0-100, más alto = mejor calidad pero archivo más grande

# Tiempo de cache
CACHE_TTL_SECONDS = 300  # 5 minutos
```

## 🐛 Troubleshooting

### Error: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Error: "No se pudo abrir el archivo AI"
El archivo AI es probablemente legacy (< CS). Solución:
1. Abrir en Illustrator
2. Guardar con "Create PDF Compatible File" activado
3. Volver a intentar

### La app es muy lenta
- Reduce `MAX_PREVIEW_SIZE` a 800
- Usa archivos más pequeños
- Verifica tu conexión a internet (si estás en Streamlit Cloud)

### "Archivo muy grande" pero es < 50MB
Verifica que `.streamlit/config.toml` tenga:
```toml
maxUploadSize = 100
```

## 📊 Monitoreo Post-Deploy

### En Streamlit Cloud

1. Ve a tu app → "Manage app"
2. Revisa logs en tiempo real
3. Monitorea crashes
4. Ajusta configuración si es necesario

### Métricas a Vigilar

- **Tiempo de respuesta**: < 10s para archivos pequeños
- **Tasa de error**: < 5%
- **Crashes por memoria**: Si ocurren, reducir límite de archivo
- **Uso de ancho de banda**: Considerar límites si muchos usuarios

## 🎯 Mejoras Futuras (v2.0)

### Prioridad Alta
- [ ] Batch processing (múltiples archivos)
- [ ] Zoom interactivo
- [ ] Indicador de progreso más detallado

### Prioridad Media
- [ ] Selector de fondo (blanco/negro/transparente)
- [ ] Slider de calidad JPG
- [ ] Historial de archivos procesados
- [ ] Compartir por link

### Prioridad Baja
- [ ] Exportar a PDF vectorial
- [ ] Extracción de paleta de colores
- [ ] Comparación lado a lado
- [ ] Soporte SVG, EPS

## 📞 Contacto y Soporte

- **Issues/Bugs**: Abrir issue en GitHub
- **Features**: Crear discussion en GitHub
- **Email**: [tu-email]

---

**¡Éxito con tu aplicación!** 🚀

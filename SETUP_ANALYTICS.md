# 🚀 Setup de Analytics - Guía Rápida

## ✅ Checklist de Configuración (15 minutos)

---

## Paso 1: Google Analytics 4 (5 min)

### 1.1 Crear Cuenta
1. Ve a: https://analytics.google.com/
2. Click en **"Empezar a medir"** o **"Admin"** (si ya tenés cuenta)
3. Click en **"Crear cuenta"**

### 1.2 Configurar Propiedad
- **Nombre de cuenta:** Miralo Rápido
- **Nombre de propiedad:** Miralo Rápido
- **Zona horaria:** (GMT-03:00) Buenos Aires
- **Moneda:** Peso argentino (ARS)

### 1.3 Detalles del Negocio
- **Industria:** Technology / Software
- **Tamaño:** Pequeña (1-10 empleados)
- **Objetivo:** Generate leads

### 1.4 Configurar Flujo de Datos
- **Plataforma:** Web
- **URL del sitio web:** `https://miralorapido.streamlit.app`
- **Nombre del flujo:** Miralo Rápido Web
- **Medición mejorada:** ✅ Activar (default)

### 1.5 Copiar Measurement ID
- Después de crear, verás un **Measurement ID**
- Formato: `G-XXXXXXXXXX` (10 caracteres después de G-)
- **Copialo** (lo necesitás para el siguiente paso)

---

## Paso 2: Configurar Measurement ID en el Código (2 min)

### 2.1 Abrir archivo de configuración
```bash
# Navegar al proyecto
cd "C:\Users\facun\OneDrive - moiguer.com\Personal\Desarrollo\Visualizador de creatividades"

# Abrir analytics_config.py en VS Code (o tu editor favorito)
code analytics_config.py
```

### 2.2 Reemplazar el Measurement ID
Buscar esta línea:
```python
GA4_MEASUREMENT_ID = "G-XXXXXXXXXX"  # Reemplazar con tu ID real
```

Reemplazar con tu ID real:
```python
GA4_MEASUREMENT_ID = "G-ABC1234567"  # Tu ID real de GA4
```

**Guardar el archivo** (Ctrl+S)

---

## Paso 3: Hotjar (5 min)

### 3.1 Crear Cuenta
1. Ve a: https://www.hotjar.com/
2. Click en **"Sign up free"**
3. Registrate con email o Google
4. **Plan:** Free (hasta 35 sesiones/día - suficiente para empezar)

### 3.2 Agregar Sitio
- **URL del sitio:** `https://miralorapido.streamlit.app`
- **Nombre del sitio:** Miralo Rápido
- Click en **"Add site"**

### 3.3 Copiar Site ID
- Hotjar te mostrará un código de instalación
- Buscar esta línea en el código:
  ```javascript
  hjid:1234567
  ```
- **Copiar solo el número** (ej: `1234567`)

### 3.4 Configurar Site ID en el Código
Abrir `analytics_config.py` nuevamente:
```python
HOTJAR_SITE_ID = "1234567"  # Tu Site ID real de Hotjar
```

**Guardar el archivo** (Ctrl+S)

---

## Paso 4: Deploy a Producción (3 min)

### 4.1 Commit y Push
```bash
# Navegar al proyecto (si no estás ahí)
cd "C:\Users\facun\OneDrive - moiguer.com\Personal\Desarrollo\Visualizador de creatividades"

# Ver cambios
git status

# Agregar cambios
git add analytics_config.py

# Commit
git commit -m "Configure GA4 and Hotjar IDs for production"

# Push a GitHub
git push origin main
```

### 4.2 Verificar Deploy en Streamlit Cloud
1. Ve a: https://share.streamlit.io/
2. Abrir tu app: **miralorapido**
3. El deploy automático debería comenzar (~2-3 minutos)
4. Esperar a que el status sea **"Running"** (verde)

---

## Paso 5: Verificar que Funciona (2 min)

### 5.1 Testear en Producción
1. Abrir: https://miralorapido.streamlit.app/
2. Abrir **DevTools** en Chrome (F12)
3. Ir a la pestaña **Console**
4. Buscar mensajes de Google Analytics:
   - Deberías ver: `https://www.googletagmanager.com/gtag/js?id=G-...`
   - Si ves error 404 en esa URL → Verificar que el Measurement ID está bien

### 5.2 Verificar en Google Analytics
1. Ve a: https://analytics.google.com/
2. Ir a: **Reports > Realtime**
3. Abrir tu sitio en otra pestaña
4. Deberías ver **1 usuario activo** en el dashboard de Realtime

### 5.3 Verificar Hotjar
1. Ve a: https://www.hotjar.com/
2. Dashboard > **Recordings**
3. Interactuar con tu sitio (navegar, hacer click)
4. Esperar 1-2 minutos
5. Debería aparecer una grabación nueva

---

## ✅ Configuración Completa

Si ves:
- ✅ Tu visita en Google Analytics Realtime
- ✅ Grabación en Hotjar

**¡Todo está funcionando correctamente!**

---

## 📊 Próximos Pasos

### Hoy:
1. Compartir el link con 5 amigos/colegas
2. Pedirles feedback honesto
3. Ver sus sesiones en Hotjar

### Próximos 7 días:
1. Revisar Analytics diariamente (5 min/día)
2. Ver métricas:
   - Usuarios/día
   - Archivos procesados
   - Errores (si hay)

### Próximos 30 días:
1. Seguir la guía en `ANALYTICS_DASHBOARD.md`
2. Objetivo: **500 usuarios/mes**
3. Si llegás al objetivo → Preparar Fase 2 (Freemium)

---

## 🐛 Troubleshooting

### "No veo datos en Google Analytics"
**Posibles causas:**
1. Measurement ID incorrecto → Verificar `analytics_config.py`
2. No esperaste suficiente → Esperar 24-48 horas para datos históricos
3. AdBlocker activo → Probar en modo incógnito

**Solución:**
1. Verificar Realtime (datos inmediatos)
2. Esperar 24 horas para reportes completos

### "No veo grabaciones en Hotjar"
**Posibles causas:**
1. Site ID incorrecto → Verificar `analytics_config.py`
2. Plan free tiene límite de 35 sesiones/día → Verificar que no lo superaste
3. Hotjar tarda 1-2 minutos en procesar → Esperar

**Solución:**
1. Navegar en el sitio por 30 segundos
2. Esperar 2-3 minutos
3. Refrescar dashboard de Hotjar

### "El deploy no funciona"
**Posibles causas:**
1. Error de sintaxis en `analytics_config.py`
2. Olvidaste hacer push a GitHub

**Solución:**
```bash
# Verificar que el archivo está bien
python -c "import analytics_config; print('OK')"

# Verificar que está en GitHub
git status
git push origin main
```

---

## 📞 Recursos

- **Google Analytics 4 Help:** https://support.google.com/analytics
- **Hotjar Help:** https://help.hotjar.com/
- **Dashboard de Métricas:** Ver `ANALYTICS_DASHBOARD.md`

---

**¡Éxito con el tracking!** 📊

*Versión 1.0 - 2026-01-30*

# 📊 Dashboard de Analytics - Miralo Rápido

## 🎯 Objetivo de Fase 1: Validación

**Meta:** 500 usuarios únicos/mes

### Métricas Clave a Monitorear

---

## 📈 Métricas Principales

### 1. **Usuarios**
- **Usuarios únicos/día**
- **Usuarios únicos/mes**
- **Usuarios recurrentes** (volvieron después de 7+ días)
- **Tasa de retorno** = (Usuarios recurrentes / Total usuarios) × 100

**Objetivo Fase 1:**
- 500 usuarios/mes = ~17 usuarios/día
- Tasa de retorno > 15% (al menos 1 de cada 7 vuelve)

---

### 2. **Archivos Procesados**
- **Total archivos procesados/día**
- **PSD vs AI** (proporción)
- **Tamaño promedio** de archivos
- **Archivos rechazados** (exceden límite)

**Tracking personalizado:**
- Evento: `file_upload`
- Parámetros: `file_type`, `file_size_mb`

**Objetivo Fase 1:**
- 100+ archivos procesados/mes
- Tasa de éxito > 90% (menos de 10% errores)

---

### 3. **Descargas**
- **Total descargas/día**
- **PNG vs JPG** (preferencia)
- **Conversión Upload → Download** = (Descargas / Uploads) × 100

**Tracking personalizado:**
- Evento: `download_png`
- Evento: `download_jpg`
- Parámetros: `download_format`, `original_file_type`, `file_size_mb`

**Objetivo Fase 1:**
- Tasa de conversión > 70% (7 de cada 10 que suben, bajan)

---

### 4. **Performance**
- **Tiempo de procesamiento promedio**
- **Archivos < 10MB:** < 5 segundos
- **Archivos 10-30MB:** < 15 segundos
- **Archivos 30-100MB:** < 30 segundos

**Tracking personalizado:**
- Evento: `file_processed`
- Parámetros: `processing_time`, `file_size_mb`

---

### 5. **Errores**
- **Tasa de error total**
- **Tipos de error:**
  - `memory_error` (archivo muy grande)
  - `processing_error` (corrupción, formato incompatible)
  - `validation_error` (extensión incorrecta)
- **Archivos que exceden límite**

**Tracking personalizado:**
- Evento: `error_occurred`
- Evento: `file_size_exceeded`

**Objetivo Fase 1:**
- Tasa de error < 10%
- Si > 5% de archivos exceden límite → considerar aumentar a 150MB

---

## 🛠️ Cómo Acceder a las Métricas

### Google Analytics 4

1. **Dashboard Principal:**
   - Ve a: https://analytics.google.com/
   - Propiedad: "Miralo Rápido"
   - Dashboard > Reports > Engagement

2. **Ver Eventos Personalizados:**
   - Reports > Events
   - Buscar:
     - `file_upload`
     - `file_processed`
     - `download_png`
     - `download_jpg`
     - `error_occurred`
     - `file_size_exceeded`

3. **Explorar Datos Específicos:**
   - Explorations > Create new exploration
   - Agregar dimensiones:
     - Event name
     - `file_type`
     - `file_size_mb`
     - `download_format`
   - Agregar métricas:
     - Event count
     - Users
     - Sessions

4. **Ver Usuarios Recurrentes:**
   - Reports > Retention
   - Cohort analysis (usuarios que volvieron)

---

### Hotjar

1. **Heatmaps:**
   - Ve a: https://www.hotjar.com/
   - Dashboard > Heatmaps
   - Ver dónde hacen click los usuarios
   - **Analizar:**
     - ¿Usan el botón de drag & drop?
     - ¿Hacen click en PNG vs JPG?
     - ¿Leen el FAQ?

2. **Grabaciones de Sesiones:**
   - Dashboard > Recordings
   - Ver 10-20 grabaciones al azar cada semana
   - **Identificar:**
     - Puntos de confusión
     - Errores comunes
     - Flujos exitosos

3. **Feedback:**
   - Dashboard > Feedback
   - Ver comentarios de usuarios (si activaste widget)

---

## 📊 Reporte Semanal Recomendado

### Cada Lunes (revisar semana anterior):

1. **Usuarios:**
   - Total usuarios únicos
   - Usuarios/día promedio
   - Usuarios recurrentes
   - Tasa de retorno

2. **Archivos:**
   - Total archivos procesados
   - PSD vs AI (%)
   - Tamaño promedio
   - Archivos rechazados

3. **Descargas:**
   - Total descargas
   - PNG vs JPG (%)
   - Tasa de conversión Upload → Download

4. **Performance:**
   - Tiempo de procesamiento promedio
   - Por rango de tamaño

5. **Errores:**
   - Tasa de error total
   - Tipos de error más comunes
   - Acciones correctivas necesarias

---

## 🎯 KPIs de Fase 1 (Semana a Semana)

### Semana 1-2: **Baseline**
- Objetivo: Entender comportamiento inicial
- Meta: 50+ usuarios
- Acción: Solo observar, no optimizar aún

### Semana 3-4: **Primeros Insights**
- Objetivo: 100+ usuarios
- Analizar:
  - ¿Qué formato es más popular? (PSD vs AI)
  - ¿Qué tamaño de archivo es más común?
  - ¿Prefieren PNG o JPG?
- Acción: Ajustar copy según preferencias

### Semana 5-8: **Optimización**
- Objetivo: 200+ usuarios
- Analizar Hotjar heatmaps:
  - ¿Hay confusión en UX?
  - ¿Leen las instrucciones?
- Acción: Hacer pequeños ajustes UX

### Semana 9-12: **Crecimiento**
- Objetivo: 500+ usuarios/mes
- Si se alcanza: **Pasar a Fase 2 (Freemium)**
- Si no: Analizar qué falta (tráfico, conversión, retención)

---

## 🚨 Alertas Automáticas (Configurar en GA4)

### 1. **Tasa de Error Alta**
- Si error rate > 15% en 24 horas
- **Acción:** Revisar logs, identificar problema

### 2. **Caída de Tráfico**
- Si usuarios/día cae > 50% vs semana anterior
- **Acción:** Verificar que el sitio funciona

### 3. **Pico de Archivos Grandes**
- Si > 30% de archivos exceden 50MB
- **Acción:** Considerar aumentar límite o upgrade Streamlit Cloud

---

## 📋 Checklist de Análisis Mensual

- [ ] **Revisar KPIs principales:**
  - ¿Llegamos a 500 usuarios/mes?
  - ¿Tasa de conversión > 70%?
  - ¿Tasa de error < 10%?

- [ ] **Analizar tendencias:**
  - ¿El tráfico crece semana a semana?
  - ¿Los usuarios vuelven?
  - ¿Qué días/horarios hay más actividad?

- [ ] **Revisar Hotjar:**
  - Ver 20 grabaciones de sesión
  - Identificar 3 problemas UX comunes
  - Planear ajustes para próximo mes

- [ ] **Analizar eventos personalizados:**
  - ¿Qué tipo de archivo es más popular?
  - ¿Qué rango de tamaño es más común?
  - ¿Errores recurrentes?

- [ ] **Decisión de Fase:**
  - Si > 500 usuarios/mes → **Iniciar Fase 2 (Freemium)**
  - Si < 500 usuarios/mes → Analizar problema (tráfico, producto, UX)

---

## 🔍 Análisis de Cohortes (Mes 2+)

**Pregunta:** ¿Los usuarios que vinieron en Semana 1 vuelven en Semana 2, 3, 4?

**Cómo:**
1. GA4 > Reports > Retention
2. Seleccionar cohorte por semana
3. Ver % de usuarios que vuelven

**Objetivo:**
- Semana 1 → Semana 2: > 20% retención
- Semana 1 → Mes 1: > 10% retención

---

## 💡 Insights Esperados (Predicciones)

### Sobre Usuarios:
- Picos de tráfico: **Lunes a Viernes** (diseñadores trabajando)
- Horarios pico: **9-11am y 2-4pm** (horario laboral)
- Tráfico bajo: Fines de semana

### Sobre Archivos:
- **PSD será más popular** (80% vs 20% AI)
- Tamaño promedio: **15-25MB**
- Archivos muy grandes (50-100MB): < 5% del total

### Sobre Descargas:
- **PNG será más popular** (70% vs 30% JPG)
- Razón: Diseñadores prefieren preservar transparencias

### Sobre Errores:
- Errores de memoria: < 3%
- Errores de procesamiento: < 5%
- Archivos rechazados (> límite): < 2%

---

## 🎬 Próximos Pasos Después de Validación

### Si llegás a 500 usuarios/mes:

1. **Analizar costos:**
   - ¿Streamlit Cloud free es suficiente?
   - ¿Hay crashes por RAM?

2. **Preparar Fase 2:**
   - Implementar autenticación (Google OAuth)
   - Implementar límites para free tier (5 archivos/día)
   - Desarrollar features premium (Batch processing)

3. **Lanzar Freemium:**
   - Tier Free: 5 archivos/día
   - Tier Premium $4.99/mes: ilimitado

---

## 📞 Herramientas Adicionales (Opcional)

### Para análisis más avanzado:

1. **Google Search Console** (SEO)
   - Ver por qué keywords te encuentran
   - Mejorar meta descriptions según búsquedas

2. **Plausible Analytics** (Alternativa a GA4)
   - Más simple, enfocado en privacy
   - $9/mes (si querés dashboard más claro)

3. **PostHog** (Product analytics)
   - Funnels detallados
   - Feature flags
   - Gratis hasta 1M eventos/mes

---

## ✅ Resumen de Configuración

**Ya configurado en el código:**
- ✅ Google Analytics 4 injection
- ✅ Hotjar injection
- ✅ Tracking de file_upload
- ✅ Tracking de file_processed (con tiempo)
- ✅ Tracking de download_png
- ✅ Tracking de download_jpg
- ✅ Tracking de errores
- ✅ Tracking de file_size_exceeded

**Falta configurar (vos):**
- [ ] Crear cuenta Google Analytics 4
- [ ] Obtener Measurement ID (G-XXXXXXXXXX)
- [ ] Crear cuenta Hotjar
- [ ] Obtener Site ID (número)
- [ ] Editar `analytics_config.py` con los IDs
- [ ] Deploy a producción
- [ ] Esperar 24-48 horas para primeros datos

---

**¡Éxito con el análisis!** 📊

*Versión 1.0 - 2026-01-30*

# 🚀 Guía de Deployment - Miralo Rápido

## 📋 Pre-Deploy Checklist

Antes de hacer el deploy, verificá que:

- [x] ✅ Servidor local corriendo sin errores (`http://localhost:8501`)
- [x] ✅ Testeado con archivo PSD (descarga PNG y JPG funciona)
- [x] ✅ Testeado con archivo AI (descarga PNG y JPG funciona)
- [x] ✅ CSS retro renderiza correctamente
- [x] ✅ Dark mode funciona con `prefers-color-scheme`
- [x] ✅ Texto en español argentino (sin errores de inglés)
- [x] ✅ SEO meta tags agregados
- [x] ✅ README.md actualizado

---

## 🔄 Deploy a Streamlit Cloud

### Paso 1: Preparar Git

```bash
# Navegar al directorio del proyecto
cd "C:\Users\facun\OneDrive - moiguer.com\Personal\Desarrollo\Visualizador de creatividades"

# Ver el estado actual
git status

# Agregar todos los cambios
git add .

# Crear commit con mensaje descriptivo
git commit -m "v1.3: Retro design + UX argentino + SEO optimization

- Diseño retro Windows XP con Luna Theme
- UX optimizado: uploader above the fold
- Español argentino 100% (voseo)
- SEO: meta tags, Open Graph, Schema.org
- Dark mode responsive (Vista/7 Aero Dark)
- Cursor personalizado retro
- Fix descarga PNG/JPG (session_state bytes)
- Límite aumentado a 100MB"

# Push a GitHub
git push origin main
```

### Paso 2: Verificar en Streamlit Cloud

1. **Abrir Streamlit Cloud Dashboard:**
   - https://share.streamlit.io/
   - Login con tu cuenta

2. **Monitorear el Re-Deploy:**
   - Ir a tu app: **miralorapido**
   - Ver el log de deployment en tiempo real
   - Esperar ~2-3 minutos

3. **Verificar que el deploy fue exitoso:**
   - Estado: "Running" (verde)
   - No hay errores en los logs

### Paso 3: Testing en Producción

#### Tests Básicos
- [ ] Abrir https://miralorapido.streamlit.app/
- [ ] Verificar que el diseño retro se ve correctamente
- [ ] Verificar cursor personalizado funciona
- [ ] Verificar texto en español argentino (sin inglés)
- [ ] Probar dark mode (cambiar preferencia del sistema)

#### Tests Funcionales
- [ ] Subir archivo PSD pequeño (< 5MB)
  - [ ] Preview se genera correctamente
  - [ ] Descargar PNG funciona
  - [ ] Descargar JPG funciona
- [ ] Subir archivo AI pequeño (< 5MB)
  - [ ] Preview se genera correctamente
  - [ ] Descargar PNG funciona
  - [ ] Descargar JPG funciona

#### Tests Avanzados (Opcional)
- [ ] Subir archivo PSD grande (30-50MB)
  - [ ] Preview funciona sin crash
  - [ ] Descarga funciona sin MemoryError
- [ ] Verificar en mobile (responsive)
- [ ] Verificar en tablet (responsive)

### Paso 4: Verificar SEO

#### Google Search Console (Opcional)
1. Ir a https://search.google.com/search-console
2. Agregar propiedad: https://miralorapido.streamlit.app/
3. Verificar ownership
4. Solicitar indexación

#### Test de Meta Tags
1. Abrir https://www.opengraph.xyz/
2. Ingresar URL: https://miralorapido.streamlit.app/
3. Verificar que se muestran:
   - Title correcto
   - Description correcta
   - Image (placeholder por ahora)

#### Test de Schema.org
1. Abrir https://validator.schema.org/
2. Ingresar URL: https://miralorapido.streamlit.app/
3. Verificar que el JSON-LD es válido

---

## 🐛 Troubleshooting

### Error: "App is not deploying"
**Causa:** Puede haber error en algún archivo

**Solución:**
1. Ver logs en Streamlit Cloud
2. Buscar línea roja con el error
3. Revisar archivo mencionado
4. Hacer fix y push nuevamente

### Error: "Module not found"
**Causa:** Falta dependencia en `requirements.txt`

**Solución:**
1. Verificar que `requirements.txt` tenga todas las librerías
2. Verificar versiones compatibles
3. Push cambios

### Error: "MemoryError" en producción
**Causa:** Archivo muy grande para 1GB RAM de Streamlit Cloud

**Solución Inmediata:**
1. Reducir `MAX_FILE_SIZE_MB` en `config.py` a 50MB
2. Push cambios
3. Comunicar límite a usuarios

**Solución Permanente:**
- Upgrade a Streamlit Cloud Paid ($20/mes con 4GB RAM)

### Diseño retro no se ve
**Causa:** CSS no se aplicó correctamente

**Verificar:**
1. Ver source de la página (Ctrl+U)
2. Buscar `<style>` con "Windows XP"
3. Si no está, revisar `app.py` líneas 73-519

### Cursor personalizado no funciona
**Causa:** Navegador no soporta data URIs en cursor

**Verificar:**
1. Probar en Chrome/Edge (soportan)
2. Firefox y Safari también deberían funcionar
3. Si no funciona, cursor default se usa como fallback

---

## 📊 Monitoreo Post-Deploy

### Día 1-3
- [ ] Revisar logs diariamente en Streamlit Cloud
- [ ] Verificar que no hay crashes
- [ ] Testear con diferentes tamaños de archivos

### Semana 1
- [ ] Monitorear uso de RAM en dashboard
- [ ] Verificar si hay errores recurrentes
- [ ] Recopilar feedback de usuarios

### Mes 1
- [ ] Analizar estadísticas de uso (si disponible)
- [ ] Identificar archivos problemáticos
- [ ] Planear mejoras para v2.0

---

## 🔄 Rollback (Si algo sale mal)

Si el deploy tiene problemas críticos:

```bash
# Ver commits recientes
git log --oneline -5

# Volver al commit anterior (cambiar <hash> por el hash real)
git revert <hash-del-commit-problemático>

# Push del revert
git push origin main
```

Streamlit Cloud detectará el cambio y hará re-deploy automáticamente.

---

## 📝 Siguiente Deploy (Futuro)

### Para v1.4 o v2.0:

1. **Crear rama de feature:**
```bash
git checkout -b feature/nueva-funcionalidad
```

2. **Desarrollar y testear localmente**

3. **Merge a main cuando esté listo:**
```bash
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

4. **Streamlit Cloud hace auto-deploy**

---

## ✅ Deploy Completado

Una vez que todos los tests pasen:

- [x] URL de producción funciona: https://miralorapido.streamlit.app/
- [x] Diseño retro se ve correctamente
- [x] Funcionalidad de descarga funciona
- [x] No hay errores en logs
- [x] SEO meta tags presentes

**¡Listo para compartir!** 🎉

---

## 🔗 Links Útiles

- **App en producción:** https://miralorapido.streamlit.app/
- **Streamlit Cloud Dashboard:** https://share.streamlit.io/
- **GitHub Repo:** [Tu repo URL]
- **Logs de Streamlit Cloud:** Dashboard > Tu App > "Manage app" > "Logs"

---

**Última actualización:** 2026-01-30
**Versión actual:** v1.3
**Estado:** ✅ Listo para deploy

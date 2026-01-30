@echo off
echo ============================================================
echo SETUP: Visualizador PSD/AI
echo ============================================================
echo.

echo [1/4] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo OK
echo.

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo OK
echo.

echo [3/4] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo OK
echo.

echo [4/4] Verificando instalacion...
python test_app.py
if errorlevel 1 (
    echo.
    echo ADVERTENCIA: Algunos tests fallaron
    echo Revisa los errores arriba
    echo.
) else (
    echo.
    echo ============================================================
    echo INSTALACION COMPLETADA
    echo ============================================================
    echo.
    echo Para ejecutar la aplicacion:
    echo   1. venv\Scripts\activate
    echo   2. streamlit run app.py
    echo.
)

pause

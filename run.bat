@echo off
echo Iniciando Visualizador PSD/AI...
echo.

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecuta setup.bat primero
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
streamlit run app.py

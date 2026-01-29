#!/bin/bash

echo "============================================================"
echo "SETUP: Visualizador PSD/AI"
echo "============================================================"
echo ""

echo "[1/4] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi
echo "OK"
echo ""

echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
echo "OK"
echo ""

echo "[3/4] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo "OK"
echo ""

echo "[4/4] Verificando instalación..."
python test_app.py
if [ $? -ne 0 ]; then
    echo ""
    echo "ADVERTENCIA: Algunos tests fallaron"
    echo "Revisa los errores arriba"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "INSTALACIÓN COMPLETADA"
    echo "============================================================"
    echo ""
    echo "Para ejecutar la aplicación:"
    echo "  1. source venv/bin/activate"
    echo "  2. streamlit run app.py"
    echo ""
fi

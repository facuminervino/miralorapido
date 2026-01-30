#!/bin/bash

echo "Iniciando Visualizador PSD/AI..."
echo ""

if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Ejecuta ./setup.sh primero"
    exit 1
fi

source venv/bin/activate
streamlit run app.py

#!/bin/bash
# Script para ejecutar la interfaz gráfica de Data Sanitizer

echo "🚀 Iniciando Data Sanitizer GUI..."
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: Ejecute este script desde el directorio data-cleaner"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "   Ejecute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual y ejecutar GUI
echo "✅ Activando entorno virtual..."
source venv/bin/activate

echo "✅ Ejecutando interfaz gráfica..."
echo "   (Cierre la ventana para terminar)"
echo ""

python main.py

echo ""
echo "👋 Data Sanitizer GUI cerrado"
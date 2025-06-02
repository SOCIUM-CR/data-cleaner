#!/bin/bash
# Script para ejecutar la interfaz CLI de Data Sanitizer

echo "⌨️  Data Sanitizer CLI"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "cli.py" ]; then
    echo "❌ Error: Ejecute este script desde el directorio data-cleaner"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "   Ejecute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Si no hay argumentos, mostrar ayuda
if [ $# -eq 0 ]; then
    echo "📋 Comandos disponibles:"
    echo ""
    python cli.py --help
    echo ""
    echo "🚀 Ejemplos rápidos:"
    echo "   ./run_cli.sh demo                    # Demo completo"
    echo "   ./run_cli.sh test                    # Crear archivo de prueba"
    echo "   ./run_cli.sh process examples/input/test_file.txt"
    echo ""
else
    # Ejecutar comando con argumentos
    python cli.py "$@"
fi
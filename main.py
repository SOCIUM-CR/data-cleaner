#!/usr/bin/env python3
"""
Data Sanitizer - Aplicación de anonimización reversible de datos sensibles
Punto de entrada principal de la aplicación
"""

import sys
import os
import argparse
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import DataSanitizerGUI


def parse_arguments():
    """Parsear argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Data Sanitizer - Anonimización reversible de datos sensibles'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Archivo a procesar directamente (modo CLI)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Archivo de salida (modo CLI)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Ejecutar en modo línea de comandos (sin GUI)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Data Sanitizer 0.1.0'
    )
    
    return parser.parse_args()


def main():
    """Función principal"""
    args = parse_arguments()
    
    if args.cli or args.file:
        # Modo línea de comandos
        print("Modo CLI no implementado aún. Use la interfaz gráfica.")
        sys.exit(1)
    else:
        # Modo GUI
        try:
            app = DataSanitizerGUI()
            app.run()
        except KeyboardInterrupt:
            print("\nAplicación interrumpida por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"Error al ejecutar la aplicación: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
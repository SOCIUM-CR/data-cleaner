#!/usr/bin/env python3
"""
Test específico de la ventana de recuperación
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.recovery_window import RecoveryWindow
    
    print("🔄 Abriendo ventana de recuperación...")
    
    # Crear ventana independiente
    recovery_window = RecoveryWindow()
    recovery_window.run()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
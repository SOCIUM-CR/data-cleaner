#!/usr/bin/env python3
"""
Test simple de la GUI para diagnosticar problemas
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("✅ tkinter importado correctamente")
    
    # Test básico de tkinter
    root = tk.Tk()
    root.title("Test GUI - Data Sanitizer")
    root.geometry("400x300")
    
    # Frame principal
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    title_label = ttk.Label(main_frame, text="Test GUI Funcionando", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)
    
    # Mensaje
    msg_label = ttk.Label(main_frame, text="La GUI básica está funcionando correctamente.\nEl problema anterior era con los tipos de archivo.")
    msg_label.pack(pady=10)
    
    # Botón de prueba de diálogo
    def test_dialog():
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Test de diálogo - Seleccionar cualquier archivo",
                filetypes=[
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if filename:
                messagebox.showinfo("Éxito", f"Archivo seleccionado:\n{os.path.basename(filename)}")
            else:
                messagebox.showinfo("Info", "No se seleccionó archivo")
        except Exception as e:
            messagebox.showerror("Error", f"Error en diálogo: {e}")
    
    test_button = ttk.Button(main_frame, text="Probar Diálogo de Archivo", command=test_dialog)
    test_button.pack(pady=10)
    
    # Botón para abrir GUI principal
    def open_main_gui():
        try:
            root.destroy()
            from gui.main_window import DataSanitizerGUI
            app = DataSanitizerGUI()
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo GUI principal: {e}")
            print(f"Error detallado: {e}")
    
    main_gui_button = ttk.Button(main_frame, text="Abrir GUI Principal", command=open_main_gui)
    main_gui_button.pack(pady=10)
    
    # Botón de salir
    exit_button = ttk.Button(main_frame, text="Salir", command=root.quit)
    exit_button.pack(pady=10)
    
    print("✅ GUI de test creada, iniciando...")
    root.mainloop()
    
except ImportError as e:
    print(f"❌ Error importando tkinter: {e}")
    print("Ejecute: brew install python-tk")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
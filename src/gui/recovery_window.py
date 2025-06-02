"""
Ventana de recuperación de archivos
Interfaz dedicada para la recuperación de datos originales
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from typing import Optional

# Agregar el directorio src al path para imports cuando se ejecuta independientemente
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.recovery import RecoveryManager


class RecoveryWindow:
    """Ventana dedicada para recuperación de archivos"""
    
    def __init__(self, parent=None):
        """Inicializar ventana de recuperación"""
        self.parent = parent
        self.recovery_manager = RecoveryManager()
        
        # Crear ventana
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Data Sanitizer - Recuperación de Archivos")
        self.window.geometry("700x500")
        self.window.minsize(600, 400)
        
        # Variables
        self.processed_file_var = tk.StringVar()
        self.recovery_key_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        
        self._create_widgets()
        self._show_available_files()
        
        # Hacer la ventana modal si tiene padre
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
    
    def _create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Recuperación de Archivos Originales", 
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Archivo procesado
        ttk.Label(main_frame, text="Archivo procesado:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.processed_entry = ttk.Entry(file_frame, textvariable=self.processed_file_var)
        self.processed_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            file_frame, 
            text="Examinar...", 
            command=self._browse_processed_file
        ).grid(row=0, column=1)
        
        # Llave de recuperación
        ttk.Label(main_frame, text="Llave de recuperación:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        key_frame = ttk.Frame(main_frame)
        key_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        key_frame.columnconfigure(0, weight=1)
        
        self.key_entry = ttk.Entry(key_frame, textvariable=self.recovery_key_var)
        self.key_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            key_frame, 
            text="Examinar...", 
            command=self._browse_recovery_key
        ).grid(row=0, column=1)
        
        # Contraseña
        ttk.Label(main_frame, text="Contraseña:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        password_frame.columnconfigure(0, weight=1)
        
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(
            password_frame,
            text="Mostrar",
            variable=self.show_password_var,
            command=self._toggle_password_visibility
        ).grid(row=0, column=1)
        
        # Archivo de salida (opcional)
        ttk.Label(main_frame, text="Guardar como (opcional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            output_frame, 
            text="Examinar...", 
            command=self._browse_output_file
        ).grid(row=0, column=1)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(text_frame, wrap=tk.WORD, height=10, state="disabled")
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(
            button_frame, 
            text="Validar Archivos", 
            command=self._validate_files
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.recover_button = ttk.Button(
            button_frame, 
            text="Recuperar Archivo", 
            command=self._recover_file,
            state="disabled"
        )
        self.recover_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Cerrar", 
            command=self.window.destroy
        ).pack(side=tk.LEFT)
    
    def _browse_processed_file(self):
        """Seleccionar archivo procesado"""
        # Usar siempre sin filtros para evitar problemas en macOS
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo procesado (sanitizado - NO la llave .json)",
            initialdir="examples/output"
        )
        
        if filename:
            # Verificar que no sea una llave de recuperación
            if "_recovery_key" in filename:
                self._update_results("❌ Error: Ha seleccionado una llave de recuperación.\n"
                                   "Por favor seleccione el archivo PROCESADO (sanitizado), no la llave.\n"
                                   f"Archivo seleccionado: {os.path.basename(filename)}")
                return
                
            self.processed_file_var.set(filename)
            self._update_results("✅ Archivo procesado seleccionado: " + os.path.basename(filename) + "\n"
                               "Ahora seleccione la llave de recuperación correspondiente.")
    
    def _browse_recovery_key(self):
        """Seleccionar llave de recuperación"""
        # Usar siempre el fallback sin filtros para evitar problemas en macOS
        filename = filedialog.askopenfilename(
            title="Seleccionar llave de recuperación (archivos .json)",
            initialdir="examples/output"
        )
        
        if filename:
            # Verificar que sea una llave de recuperación
            if "_recovery_key" not in filename or not filename.endswith(".json"):
                self._update_results("❌ Error: El archivo seleccionado no parece ser una llave de recuperación.\n"
                                   "Las llaves deben contener '_recovery_key' y terminar en '.json'\n"
                                   f"Archivo seleccionado: {os.path.basename(filename)}")
                return
                
            self.recovery_key_var.set(filename)
            self._update_results("✅ Llave de recuperación seleccionada: " + os.path.basename(filename) + "\n"
                               "Ahora puede validar la compatibilidad o proceder con la recuperación.")
    
    def _browse_output_file(self):
        """Seleccionar archivo de salida"""
        # Usar sin filtros para evitar problemas en macOS
        filename = filedialog.asksaveasfilename(
            title="Guardar archivo recuperado como",
            initialdir="examples/output"
        )
        
        if filename:
            self.output_file_var.set(filename)
    
    def _toggle_password_visibility(self):
        """Alternar visibilidad de contraseña"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def _validate_files(self):
        """Validar compatibilidad entre archivos"""
        processed_file = self.processed_file_var.get()
        recovery_key = self.recovery_key_var.get()
        
        if not processed_file or not recovery_key:
            messagebox.showerror("Error", "Debe seleccionar tanto el archivo procesado como la llave de recuperación")
            return
        
        self._update_results("🔍 Validando compatibilidad de archivos...\n")
        self.window.update()
        
        try:
            validation = self.recovery_manager.validate_recovery_compatibility(
                processed_file, recovery_key
            )
            
            if validation["compatible"]:
                result_text = "✅ Archivos compatibles\n\n"
                
                metadata = validation["metadata"]
                result_text += f"📊 Información:\n"
                result_text += f"  - Hash del archivo: {metadata.get('file_hash', 'N/A')[:16]}...\n"
                result_text += f"  - Fecha de llave: {metadata.get('recovery_timestamp', 'N/A')}\n"
                result_text += f"  - Versión: {metadata.get('recovery_version', 'N/A')}\n"
                result_text += f"  - Tamaño: {metadata.get('file_size', 0):,} bytes\n"
                
                if validation["warnings"]:
                    result_text += f"\n⚠️  Advertencias:\n"
                    for warning in validation["warnings"]:
                        result_text += f"  - {warning}\n"
                
                result_text += f"\n✨ Listo para recuperar archivo\n"
                self.recover_button.config(state="normal")
                
            else:
                result_text = "❌ Archivos no compatibles\n\n"
                result_text += "🚫 Problemas encontrados:\n"
                for issue in validation["issues"]:
                    result_text += f"  - {issue}\n"
                
                self.recover_button.config(state="disabled")
            
            self._update_results(result_text)
            
        except Exception as e:
            self._update_results(f"❌ Error durante la validación: {e}")
            self.recover_button.config(state="disabled")
    
    def _recover_file(self):
        """Realizar recuperación del archivo"""
        processed_file = self.processed_file_var.get()
        recovery_key = self.recovery_key_var.get()
        password = self.password_var.get() if self.password_var.get() else None
        output_file = self.output_file_var.get() if self.output_file_var.get() else None
        
        if not processed_file or not recovery_key:
            messagebox.showerror("Error", "Debe seleccionar tanto el archivo procesado como la llave de recuperación")
            return
        
        self._update_results("🔄 Recuperando archivo original...\n")
        self.window.update()
        
        try:
            result = self.recovery_manager.recover_from_key_file(
                processed_file, recovery_key, password, output_file
            )
            
            if result["success"]:
                result_text = "✅ ¡Recuperación exitosa!\n\n"
                
                if output_file:
                    result_text += f"📁 Archivo guardado en: {output_file}\n"
                
                metadata = result["metadata"]
                result_text += f"\n📊 Información de recuperación:\n"
                result_text += f"  - Hash original: {metadata.get('original_file_hash', 'N/A')[:16]}...\n"
                result_text += f"  - Tamaño recuperado: {metadata.get('file_size', 0):,} bytes\n"
                result_text += f"  - Fecha de recuperación: {metadata.get('recovery_date', 'N/A')}\n"
                
                if result["warnings"]:
                    result_text += f"\n⚠️  Advertencias:\n"
                    for warning in result["warnings"]:
                        result_text += f"  - {warning}\n"
                
                # Mostrar preview del contenido recuperado
                if len(result["recovered_content"]) > 0:
                    preview = result["recovered_content"][:500]
                    if len(result["recovered_content"]) > 500:
                        preview += "..."
                    
                    result_text += f"\n📄 Preview del contenido recuperado:\n"
                    result_text += f"{'='*50}\n"
                    result_text += preview
                    result_text += f"\n{'='*50}\n"
                
                messagebox.showinfo("Éxito", "Archivo recuperado exitosamente")
                
            else:
                result_text = "❌ Error en la recuperación\n\n"
                result_text += "🚫 Errores encontrados:\n"
                for error in result["errors"]:
                    result_text += f"  - {error}\n"
                
                messagebox.showerror("Error", "La recuperación falló")
            
            self._update_results(result_text)
            
        except Exception as e:
            error_text = f"❌ Error inesperado durante la recuperación: {e}"
            self._update_results(error_text)
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def _show_available_files(self):
        """Mostrar archivos disponibles para recuperación"""
        output_dir = "examples/output"
        
        if not os.path.exists(output_dir):
            self._update_results("❌ Directorio examples/output no encontrado.")
            return
        
        try:
            # Buscar archivos
            sanitized_files = []
            recovery_keys = []
            
            for file in os.listdir(output_dir):
                if "_sanitized_" in file and "_recovery_key" not in file:
                    sanitized_files.append(file)
                elif "_recovery_key" in file and file.endswith(".json"):
                    recovery_keys.append(file)
            
            help_text = "🔄 VENTANA DE RECUPERACIÓN\n"
            help_text += "=" * 40 + "\n\n"
            
            if sanitized_files:
                help_text += f"📁 Archivos procesados disponibles ({len(sanitized_files)}):\n"
                for f in sorted(sanitized_files):
                    help_text += f"  • {f}\n"
                help_text += "\n"
                
                help_text += f"🔑 Llaves de recuperación disponibles ({len(recovery_keys)}):\n"
                for f in sorted(recovery_keys):
                    help_text += f"  • {f}\n"
                help_text += "\n"
                
                help_text += "📋 INSTRUCCIONES:\n"
                help_text += "1. Seleccione un archivo PROCESADO (sin '_recovery_key')\n"
                help_text += "2. Seleccione la llave CORRESPONDIENTE (con '_recovery_key')\n"
                help_text += "3. Introduzca la contraseña si la usó al procesar\n"
                help_text += "4. Valide compatibilidad (recomendado)\n"
                help_text += "5. Proceda con la recuperación\n"
                
            else:
                help_text += "❌ No se encontraron archivos procesados.\n"
                help_text += "   Ejecute primero: ./run_cli.sh demo\n"
                help_text += "   O procese un archivo desde la ventana principal.\n"
            
            self._update_results(help_text)
            
        except Exception as e:
            self._update_results(f"❌ Error listando archivos: {e}")
    
    def _update_results(self, text: str):
        """Actualizar texto de resultados"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        self.results_text.config(state="disabled")
    
    def run(self):
        """Ejecutar ventana (solo si no tiene padre)"""
        if not self.parent:
            self.window.mainloop()


def main():
    """Función principal para ejecutar ventana independiente"""
    app = RecoveryWindow()
    app.run()


if __name__ == "__main__":
    main()
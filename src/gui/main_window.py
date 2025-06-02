"""
Ventana principal de la aplicación Data Sanitizer
Interfaz gráfica principal con funcionalidad drag & drop
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Optional, List
from pathlib import Path

from core.processor import FileProcessor, ProcessingResult


class DataSanitizerGUI:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        """Inicializar interfaz gráfica"""
        self.root = tk.Tk()
        self.processor = FileProcessor()
        self.current_file = None
        self.processing_result = None
        
        self._setup_window()
        self._create_widgets()
        self._setup_drag_drop()
    
    def _setup_window(self):
        """Configurar ventana principal"""
        self.root.title("Data Sanitizer - Anonimización Reversible de Datos")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configurar estilos
        style = ttk.Style()
        style.theme_use('clam')
    
    def _create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Data Sanitizer", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Archivo a Procesar", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        self.browse_button = ttk.Button(file_frame, text="Examinar...", command=self._browse_file)
        self.browse_button.grid(row=0, column=2, sticky=tk.W)
        
        # Área de drag & drop
        self.drop_frame = tk.Frame(
            main_frame, 
            bg="lightgray", 
            height=100, 
            relief="ridge", 
            bd=2
        )
        self.drop_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        self.drop_frame.grid_propagate(False)
        
        drop_label = tk.Label(
            self.drop_frame,
            text="Arrastra y suelta un archivo aquí\no usa el botón Examinar",
            bg="lightgray",
            fg="gray",
            font=("Arial", 10)
        )
        drop_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Configuración de procesamiento
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Contraseña (opcional):").grid(row=0, column=0, sticky=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(config_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        self.preview_var = tk.BooleanVar(value=True)
        self.preview_check = ttk.Checkbutton(
            config_frame, 
            text="Mostrar vista previa antes de procesar",
            variable=self.preview_var
        )
        self.preview_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(text_frame, wrap=tk.WORD, state="disabled")
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        self.preview_button = ttk.Button(
            button_frame, 
            text="Vista Previa", 
            command=self._preview_file,
            state="disabled"
        )
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.process_button = ttk.Button(
            button_frame, 
            text="Procesar Archivo", 
            command=self._process_file,
            state="disabled"
        )
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(
            button_frame, 
            text="Guardar Resultado", 
            command=self._save_result,
            state="disabled"
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.recover_button = ttk.Button(
            button_frame, 
            text="Recuperar Archivo", 
            command=self._recover_file
        )
        self.recover_button.pack(side=tk.LEFT)
    
    def _setup_drag_drop(self):
        """Configurar funcionalidad drag & drop"""
        # Configurar eventos de drop
        self.drop_frame.bind("<Button-1>", self._on_drop_click)
        self.drop_frame.bind("<B1-Motion>", self._on_drop_drag)
        self.drop_frame.bind("<ButtonRelease-1>", self._on_drop_release)
        
        # Simular drag & drop básico (implementación completa requiere tkinterdnd2)
        self.drop_frame.bind("<Double-Button-1>", lambda e: self._browse_file())
        
        # Mejorar la apariencia visual del drop frame
        self.drop_frame.bind("<Enter>", self._on_drop_enter)
        self.drop_frame.bind("<Leave>", self._on_drop_leave)
    
    def _browse_file(self):
        """Abrir diálogo para seleccionar archivo"""
        try:
            # Usar formato más simple para evitar problemas en macOS
            filetypes = [
                ("Archivos de texto", "*.txt"),
                ("Archivos Markdown", "*.md"),
                ("Código Python", "*.py"),
                ("Código JavaScript", "*.js"),
                ("Configuración JSON", "*.json"),
                ("Archivos de log", "*.log"),
                ("Todos los archivos", "*.*")
            ]
            
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo a procesar",
                filetypes=filetypes
            )
        except Exception as e:
            # Fallback sin tipos de archivo si hay error
            print(f"Error con filetypes, usando fallback: {e}")
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo a procesar"
            )
        
        if filename:
            self._load_file(filename)
    
    def _load_file(self, file_path: str):
        """Cargar archivo seleccionado"""
        if not self.processor.is_file_supported(file_path):
            messagebox.showerror("Error", "Tipo de archivo no soportado")
            return
        
        self.current_file = file_path
        self.file_path_var.set(file_path)
        
        # Habilitar botones
        self.preview_button.config(state="normal")
        self.process_button.config(state="normal")
        
        # Mostrar información del archivo
        self._display_file_info(file_path)
    
    def _display_file_info(self, file_path: str):
        """Mostrar información del archivo cargado"""
        try:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            info = f"Archivo cargado: {file_name}\n"
            info += f"Tamaño: {file_size:,} bytes\n"
            info += f"Ruta: {file_path}\n\n"
            info += "Listo para procesar. Use 'Vista Previa' para ver los cambios propuestos.\n"
            
            self._update_results_text(info)
        except Exception as e:
            self._update_results_text(f"Error cargando archivo: {e}")
    
    def _preview_file(self):
        """Mostrar vista previa de cambios"""
        if not self.current_file:
            return
        
        self._update_results_text("Analizando archivo...\n")
        self.root.update()
        
        try:
            detections, stats = self.processor.preview_changes(self.current_file)
            
            if "error" in stats:
                self._update_results_text(f"Error: {stats['error']}")
                return
            
            # Mostrar estadísticas
            preview_text = "=== VISTA PREVIA DE CAMBIOS ===\n\n"
            preview_text += f"Total de detecciones: {stats.get('total_detections', 0)}\n"
            preview_text += f"Tamaño del archivo: {stats.get('file_size', 0):,} bytes\n\n"
            
            if stats.get('total_detections', 0) > 0:
                preview_text += "Tipos de datos detectados:\n"
                for data_type, count in stats.get('by_type', {}).items():
                    preview_text += f"  - {data_type}: {count} ocurrencias\n"
                
                preview_text += f"\nConfianza promedio: {stats.get('average_confidence', 0):.2%}\n\n"
                
                # Mostrar primeras detecciones
                preview_text += "Ejemplos de detecciones:\n"
                for i, detection in enumerate(detections[:10]):
                    preview_text += f"{i+1}. {detection.data_type.value}: '{detection.original_text}' "
                    preview_text += f"(confianza: {detection.confidence:.2%})\n"
                
                if len(detections) > 10:
                    preview_text += f"... y {len(detections) - 10} más\n"
            else:
                preview_text += "No se detectaron datos sensibles en este archivo.\n"
            
            self._update_results_text(preview_text)
            
        except Exception as e:
            self._update_results_text(f"Error en vista previa: {e}")
    
    def _process_file(self):
        """Procesar archivo completo"""
        if not self.current_file:
            return
        
        # Mostrar vista previa si está habilitada
        if self.preview_var.get():
            result = messagebox.askyesno(
                "Confirmar procesamiento",
                "¿Desea proceder con el procesamiento del archivo?"
            )
            if not result:
                return
        
        self._update_results_text("Procesando archivo...\n")
        self.root.update()
        
        try:
            password = self.password_var.get() if self.password_var.get() else None
            
            result = self.processor.process_file(
                self.current_file,
                password=password
            )
            
            self.processing_result = result
            
            if result.success:
                self._display_processing_success(result)
                self.save_button.config(state="normal")
            else:
                self._display_processing_errors(result)
                
        except Exception as e:
            self._update_results_text(f"Error durante el procesamiento: {e}")
    
    def _display_processing_success(self, result: ProcessingResult):
        """Mostrar resultado exitoso del procesamiento"""
        success_text = "=== PROCESAMIENTO COMPLETADO ===\n\n"
        success_text += f"Archivo original: {result.original_filename}\n"
        success_text += f"Archivo sanitizado: {result.sanitized_filename}\n\n"
        
        stats = result.statistics
        success_text += f"Detecciones totales: {stats.get('total_detections', 0)}\n"
        success_text += f"Mapeos creados: {stats.get('mappings_created', 0)}\n"
        success_text += f"Tamaño original: {stats.get('file_size_original', 0):,} bytes\n"
        success_text += f"Tamaño sanitizado: {stats.get('file_size_sanitized', 0):,} bytes\n\n"
        
        if stats.get('by_type'):
            success_text += "Datos reemplazados por tipo:\n"
            for data_type, count in stats['by_type'].items():
                success_text += f"  - {data_type}: {count}\n"
        
        success_text += f"\nLlave de recuperación: {'Generada' if result.recovery_key else 'No generada'}\n"
        success_text += "\nUse 'Guardar Resultado' para exportar los archivos.\n"
        
        self._update_results_text(success_text)
    
    def _display_processing_errors(self, result: ProcessingResult):
        """Mostrar errores del procesamiento"""
        error_text = "=== ERRORES EN EL PROCESAMIENTO ===\n\n"
        for error in result.errors:
            error_text += f"• {error}\n"
        
        self._update_results_text(error_text)
    
    def _save_result(self):
        """Guardar resultado del procesamiento"""
        if not self.processing_result or not self.processing_result.success:
            messagebox.showerror("Error", "No hay resultado válido para guardar")
            return
        
        # Seleccionar directorio de salida
        output_dir = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if not output_dir:
            return
        
        try:
            # Guardar archivo sanitizado
            sanitized_path = os.path.join(output_dir, self.processing_result.sanitized_filename)
            with open(sanitized_path, 'w', encoding='utf-8') as f:
                f.write(self.processing_result.sanitized_content)
            
            # Guardar llave de recuperación si existe
            recovery_saved = False
            if self.processing_result.recovery_key:
                recovery_filename = self.processing_result.sanitized_filename.replace('.', '_recovery_key.')
                if not recovery_filename.endswith('.json'):
                    recovery_filename += '.json'
                
                recovery_path = os.path.join(output_dir, recovery_filename)
                recovery_saved = self.processor.security_manager.save_recovery_key(
                    self.processing_result.recovery_key, recovery_path
                )
            
            # Mostrar confirmación
            message = f"Archivos guardados en:\n{output_dir}\n\n"
            message += f"• Archivo sanitizado: {self.processing_result.sanitized_filename}\n"
            if recovery_saved:
                message += f"• Llave de recuperación: {recovery_filename}\n"
            
            messagebox.showinfo("Guardado completado", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando archivos: {e}")
    
    def _recover_file(self):
        """Recuperar archivo usando llave de recuperación"""
        try:
            from .recovery_window import RecoveryWindow
            recovery_window = RecoveryWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de recuperación: {e}")
            print(f"Error importando recovery_window: {e}")  # Para debug
    
    def _update_results_text(self, text: str):
        """Actualizar texto de resultados"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        self.results_text.config(state="disabled")
    
    def _on_drop_click(self, event):
        """Manejar clic en área de drop"""
        self._browse_file()
    
    def _on_drop_drag(self, event):
        """Manejar arrastre en área de drop"""
        pass
    
    def _on_drop_release(self, event):
        """Manejar liberación en área de drop"""
        pass
    
    def _on_drop_enter(self, event):
        """Cambiar apariencia al entrar al área de drop"""
        self.drop_frame.config(bg="lightblue")
    
    def _on_drop_leave(self, event):
        """Restaurar apariencia al salir del área de drop"""
        self.drop_frame.config(bg="lightgray")
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DataSanitizerGUI()
    app.run()
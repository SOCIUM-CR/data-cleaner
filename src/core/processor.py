"""
Módulo principal de procesamiento
Coordina la detección, reemplazo y generación de archivos sanitizados
"""

import os
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

from .detector import SensitiveDataDetector, Detection
from .security import SecurityManager, MappingEntry, RecoveryKey


@dataclass
class ProcessingResult:
    """Resultado del procesamiento de un archivo"""
    success: bool
    sanitized_content: str
    recovery_key: Optional[RecoveryKey]
    statistics: Dict[str, Any]
    errors: List[str]
    original_filename: str
    sanitized_filename: str


class FileProcessor:
    """Procesador principal de archivos"""
    
    def __init__(self):
        """Inicializar procesador"""
        self.detector = SensitiveDataDetector()
        self.security_manager = SecurityManager()
        self.supported_extensions = {
            '.txt', '.md', '.rst', '.py', '.js', '.java', '.cpp', '.c', '.h',
            '.json', '.yaml', '.yml', '.xml', '.ini', '.conf', '.log', '.csv'
        }
    
    def process_file(self, file_path: str, 
                    output_dir: Optional[str] = None,
                    password: Optional[str] = None,
                    custom_patterns: Optional[Dict] = None) -> ProcessingResult:
        """Procesar un archivo completo"""
        
        errors = []
        
        try:
            # Validar archivo de entrada
            if not self._validate_input_file(file_path):
                return ProcessingResult(
                    success=False,
                    sanitized_content="",
                    recovery_key=None,
                    statistics={},
                    errors=[f"Archivo no válido o no soportado: {file_path}"],
                    original_filename=os.path.basename(file_path),
                    sanitized_filename=""
                )
            
            # Leer contenido del archivo
            original_content = self._read_file_content(file_path)
            if original_content is None:
                return ProcessingResult(
                    success=False,
                    sanitized_content="",
                    recovery_key=None,
                    statistics={},
                    errors=[f"No se pudo leer el archivo: {file_path}"],
                    original_filename=os.path.basename(file_path),
                    sanitized_filename=""
                )
            
            # Configurar patrones personalizados si se proporcionan
            if custom_patterns:
                self._update_detector_patterns(custom_patterns)
            
            # Detectar datos sensibles
            detections = self.detector.detect_all(original_content)
            
            if not detections:
                return ProcessingResult(
                    success=True,
                    sanitized_content=original_content,
                    recovery_key=None,
                    statistics={"total_detections": 0, "message": "No se encontraron datos sensibles"},
                    errors=[],
                    original_filename=os.path.basename(file_path),
                    sanitized_filename=""
                )
            
            # Crear mapeos de reemplazo
            mappings = self.security_manager.create_dummy_replacements(detections)
            
            # Aplicar reemplazos
            sanitized_content = self._apply_replacements(original_content, mappings)
            
            # Generar llave de recuperación
            recovery_key = self.security_manager.generate_recovery_key(
                mappings, original_content, password
            )
            
            # Generar nombre de archivo sanitizado
            original_filename = os.path.basename(file_path)
            sanitized_filename = self.security_manager.generate_secure_filename(original_filename)
            
            # Guardar archivos si se especifica directorio de salida
            if output_dir:
                self._save_output_files(
                    output_dir, sanitized_filename, sanitized_content, recovery_key
                )
            
            # Generar estadísticas
            statistics = self.detector.get_statistics(detections)
            statistics.update({
                'mappings_created': len(mappings),
                'file_size_original': len(original_content),
                'file_size_sanitized': len(sanitized_content),
                'recovery_key_generated': recovery_key is not None
            })
            
            return ProcessingResult(
                success=True,
                sanitized_content=sanitized_content,
                recovery_key=recovery_key,
                statistics=statistics,
                errors=errors,
                original_filename=original_filename,
                sanitized_filename=sanitized_filename
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                sanitized_content="",
                recovery_key=None,
                statistics={},
                errors=[f"Error durante el procesamiento: {str(e)}"],
                original_filename=os.path.basename(file_path) if file_path else "",
                sanitized_filename=""
            )
    
    def recover_file(self, processed_file_path: str, 
                    recovery_key_path: str,
                    password: Optional[str] = None,
                    output_path: Optional[str] = None) -> Tuple[bool, str, List[str]]:
        """Recuperar archivo original usando llave de recuperación"""
        
        errors = []
        
        try:
            # Cargar llave de recuperación
            recovery_key = self.security_manager.load_recovery_key(recovery_key_path)
            if not recovery_key:
                return False, "", ["No se pudo cargar la llave de recuperación"]
            
            # Validar llave de recuperación
            if not self.security_manager.validate_recovery_key(recovery_key):
                return False, "", ["Llave de recuperación inválida"]
            
            # Leer archivo procesado
            processed_content = self._read_file_content(processed_file_path)
            if processed_content is None:
                return False, "", ["No se pudo leer el archivo procesado"]
            
            # Recuperar contenido original
            recovered_content = self.security_manager.recover_original_data(
                processed_content, recovery_key, password
            )
            
            if recovered_content is None:
                return False, "", ["Error durante la recuperación de datos"]
            
            # Guardar archivo recuperado si se especifica ruta
            if output_path:
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(recovered_content)
                except Exception as e:
                    errors.append(f"Error guardando archivo recuperado: {e}")
            
            return True, recovered_content, errors
            
        except Exception as e:
            return False, "", [f"Error durante la recuperación: {str(e)}"]
    
    def preview_changes(self, file_path: str, 
                       custom_patterns: Optional[Dict] = None) -> Tuple[List[Detection], Dict[str, Any]]:
        """Previsualizar cambios que se harían sin procesar el archivo"""
        
        try:
            # Leer contenido
            content = self._read_file_content(file_path)
            if content is None:
                return [], {"error": "No se pudo leer el archivo"}
            
            # Configurar patrones personalizados
            if custom_patterns:
                self._update_detector_patterns(custom_patterns)
            
            # Detectar datos sensibles
            detections = self.detector.detect_all(content)
            
            # Generar estadísticas de preview
            stats = self.detector.get_statistics(detections)
            stats.update({
                'file_size': len(content),
                'preview_mode': True
            })
            
            return detections, stats
            
        except Exception as e:
            return [], {"error": f"Error en preview: {str(e)}"}
    
    def _validate_input_file(self, file_path: str) -> bool:
        """Validar que el archivo de entrada es procesable"""
        try:
            path_obj = Path(file_path)
            
            # Verificar que existe
            if not path_obj.exists():
                return False
            
            # Verificar que es un archivo
            if not path_obj.is_file():
                return False
            
            # Verificar extensión soportada
            if path_obj.suffix.lower() not in self.supported_extensions:
                return False
            
            # Verificar tamaño (máximo 50MB)
            if path_obj.stat().st_size > 50 * 1024 * 1024:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _read_file_content(self, file_path: str) -> Optional[str]:
        """Leer contenido de archivo con manejo de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception:
                break
        
        return None
    
    def _apply_replacements(self, content: str, mappings: List[MappingEntry]) -> str:
        """Aplicar reemplazos de datos sensibles"""
        # Ordenar por posición (de final a inicio para evitar problemas de índices)
        sorted_mappings = sorted(mappings, key=lambda x: x.position[0], reverse=True)
        
        result = content
        for mapping in sorted_mappings:
            start, end = mapping.position
            # Reemplazar usando posiciones exactas
            result = result[:start] + mapping.dummy + result[end:]
        
        return result
    
    def _update_detector_patterns(self, custom_patterns: Dict):
        """Actualizar patrones del detector con patrones personalizados"""
        # Esta implementación es básica - en el futuro se puede expandir
        for data_type, patterns in custom_patterns.items():
            if hasattr(self.detector.patterns, data_type):
                self.detector.patterns[data_type].extend(patterns)
    
    def _save_output_files(self, output_dir: str, sanitized_filename: str, 
                          sanitized_content: str, recovery_key: RecoveryKey):
        """Guardar archivos de salida"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo sanitizado
        sanitized_path = output_path / sanitized_filename
        with open(sanitized_path, 'w', encoding='utf-8') as f:
            f.write(sanitized_content)
        
        # Guardar llave de recuperación
        recovery_filename = sanitized_filename.replace('.', '_recovery_key.')
        if not recovery_filename.endswith('.json'):
            recovery_filename += '.json'
        
        recovery_path = output_path / recovery_filename
        self.security_manager.save_recovery_key(recovery_key, str(recovery_path))
    
    def get_supported_extensions(self) -> List[str]:
        """Obtener lista de extensiones soportadas"""
        return list(self.supported_extensions)
    
    def is_file_supported(self, file_path: str) -> bool:
        """Verificar si un archivo es soportado"""
        return Path(file_path).suffix.lower() in self.supported_extensions
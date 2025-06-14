"""
Módulo de recuperación de datos
Maneja la restauración de datos originales y validación de integridad
"""

import json
import os
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime

from .security import SecurityManager, RecoveryKey


class RecoveryManager:
    """Gestor de recuperación de datos originales"""
    
    def __init__(self):
        """Inicializar gestor de recuperación"""
        self.security_manager = SecurityManager()
        self.recovery_history = []
    
    def recover_from_key_file(self, processed_file_path: str, 
                             recovery_key_path: str,
                             password: Optional[str] = None,
                             output_path: Optional[str] = None) -> Dict[str, Any]:
        """Recuperar archivo desde archivo de llave de recuperación"""
        
        result = {
            "success": False,
            "recovered_content": "",
            "errors": [],
            "warnings": [],
            "metadata": {}
        }
        
        try:
            # Validar archivos de entrada
            if not os.path.exists(processed_file_path):
                result["errors"].append("Archivo procesado no encontrado")
                return result
            
            if not os.path.exists(recovery_key_path):
                result["errors"].append("Archivo de llave de recuperación no encontrado")
                return result
            
            # Cargar llave de recuperación
            recovery_key = self.security_manager.load_recovery_key(recovery_key_path)
            if not recovery_key:
                result["errors"].append("No se pudo cargar la llave de recuperación")
                return result
            
            # Validar llave de recuperación
            if not self.security_manager.validate_recovery_key(recovery_key):
                result["errors"].append("Llave de recuperación inválida o corrupta")
                return result
            
            # Leer archivo procesado
            try:
                with open(processed_file_path, 'r', encoding='utf-8') as f:
                    processed_content = f.read()
            except Exception as e:
                result["errors"].append(f"Error leyendo archivo procesado: {e}")
                return result
            
            # Verificar integridad básica
            integrity_check = self._perform_integrity_check(processed_content, recovery_key)
            if not integrity_check["valid"]:
                result["warnings"].extend(integrity_check["warnings"])
            
            # Recuperar contenido original
            recovered_content = self.security_manager.recover_original_data(
                processed_content, recovery_key, password
            )
            
            if recovered_content is None:
                result["errors"].append("Error durante la recuperación de datos")
                return result
            
            # Guardar archivo recuperado si se especifica ruta
            if output_path:
                try:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(recovered_content)
                    result["output_path"] = output_path
                except Exception as e:
                    result["warnings"].append(f"Error guardando archivo: {e}")
            
            # Registrar en historial
            self._add_to_recovery_history(recovery_key_path, processed_file_path, True)
            
            # Preparar resultado exitoso
            result.update({
                "success": True,
                "recovered_content": recovered_content,
                "metadata": {
                    "original_file_hash": recovery_key.file_hash,
                    "recovery_timestamp": recovery_key.timestamp,
                    "recovery_version": recovery_key.version,
                    "file_size": len(recovered_content),
                    "recovery_date": datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            result["errors"].append(f"Error inesperado durante la recuperación: {str(e)}")
            self._add_to_recovery_history(recovery_key_path, processed_file_path, False)
        
        return result
    
    def batch_recovery(self, recovery_requests: List[Dict[str, str]],
                      password: Optional[str] = None,
                      output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Recuperar múltiples archivos en lote"""
        
        results = {
            "total_files": len(recovery_requests),
            "successful_recoveries": 0,
            "failed_recoveries": 0,
            "file_results": [],
            "overall_errors": []
        }
        
        for i, request in enumerate(recovery_requests):
            try:
                processed_file = request.get("processed_file")
                recovery_key_file = request.get("recovery_key")
                
                if not processed_file or not recovery_key_file:
                    results["file_results"].append({
                        "index": i,
                        "success": False,
                        "error": "Archivos requeridos no especificados"
                    })
                    results["failed_recoveries"] += 1
                    continue
                
                # Determinar archivo de salida
                output_path = None
                if output_dir:
                    filename = os.path.basename(processed_file)
                    # Remover sufijos de sanitización si existen
                    if "_sanitized_" in filename:
                        filename = filename.split("_sanitized_")[0] + ".txt"
                    output_path = os.path.join(output_dir, f"recovered_{filename}")
                
                # Realizar recuperación
                recovery_result = self.recover_from_key_file(
                    processed_file, recovery_key_file, password, output_path
                )
                
                if recovery_result["success"]:
                    results["successful_recoveries"] += 1
                else:
                    results["failed_recoveries"] += 1
                
                results["file_results"].append({
                    "index": i,
                    "processed_file": processed_file,
                    "recovery_key": recovery_key_file,
                    "success": recovery_result["success"],
                    "errors": recovery_result["errors"],
                    "warnings": recovery_result["warnings"],
                    "output_path": output_path if recovery_result["success"] else None
                })
                
            except Exception as e:
                results["file_results"].append({
                    "index": i,
                    "success": False,
                    "error": f"Error procesando archivo {i}: {str(e)}"
                })
                results["failed_recoveries"] += 1
        
        return results
    
    def validate_recovery_compatibility(self, processed_file_path: str,
                                      recovery_key_path: str) -> Dict[str, Any]:
        """Validar compatibilidad entre archivo procesado y llave de recuperación"""
        
        validation = {
            "compatible": False,
            "issues": [],
            "warnings": [],
            "metadata": {}
        }
        
        try:
            # Cargar llave de recuperación
            recovery_key = self.security_manager.load_recovery_key(recovery_key_path)
            if not recovery_key:
                validation["issues"].append("No se pudo cargar la llave de recuperación")
                return validation
            
            # Validar estructura de la llave
            if not self.security_manager.validate_recovery_key(recovery_key):
                validation["issues"].append("Llave de recuperación inválida")
                return validation
            
            # Verificar que el archivo procesado existe
            if not os.path.exists(processed_file_path):
                validation["issues"].append("Archivo procesado no encontrado")
                return validation
            
            # Leer archivo procesado
            try:
                with open(processed_file_path, 'r', encoding='utf-8') as f:
                    processed_content = f.read()
            except Exception as e:
                validation["issues"].append(f"Error leyendo archivo procesado: {e}")
                return validation
            
            # Verificar compatibilidad de versiones
            if recovery_key.version != self.security_manager.version:
                validation["warnings"].append(
                    f"Versión de llave ({recovery_key.version}) "
                    f"diferente a versión actual ({self.security_manager.version})"
                )
            
            # Verificar integridad
            integrity_check = self._perform_integrity_check(processed_content, recovery_key)
            validation["warnings"].extend(integrity_check["warnings"])
            
            # Si llegamos aquí sin errores críticos, es compatible
            validation["compatible"] = True
            validation["metadata"] = {
                "file_hash": recovery_key.file_hash,
                "recovery_timestamp": recovery_key.timestamp,
                "recovery_version": recovery_key.version,
                "file_size": len(processed_content)
            }
            
        except Exception as e:
            validation["issues"].append(f"Error durante validación: {str(e)}")
        
        return validation
    
    def _perform_integrity_check(self, content: str, recovery_key: RecoveryKey) -> Dict[str, Any]:
        """Realizar verificación de integridad básica"""
        
        check_result = {
            "valid": True,
            "warnings": []
        }
        
        try:
            # Verificar que el contenido no esté vacío
            if not content.strip():
                check_result["warnings"].append("El archivo procesado está vacío")
                check_result["valid"] = False
            
            # Verificar fecha de la llave (advertir si es muy antigua)
            try:
                key_date = datetime.fromisoformat(recovery_key.timestamp)
                days_old = (datetime.now() - key_date).days
                if days_old > 365:
                    check_result["warnings"].append(
                        f"La llave de recuperación tiene {days_old} días de antigüedad"
                    )
            except Exception:
                check_result["warnings"].append("Formato de fecha de llave inválido")
            
            # Verificar que el checksum existe
            if not recovery_key.checksum:
                check_result["warnings"].append("Llave sin checksum de integridad")
            
        except Exception as e:
            check_result["warnings"].append(f"Error en verificación de integridad: {e}")
            check_result["valid"] = False
        
        return check_result
    
    def _add_to_recovery_history(self, recovery_key_path: str, 
                               processed_file_path: str, success: bool):
        """Agregar entrada al historial de recuperaciones"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "recovery_key_path": recovery_key_path,
            "processed_file_path": processed_file_path,
            "success": success
        }
        
        self.recovery_history.append(entry)
        
        # Mantener solo las últimas 100 entradas
        if len(self.recovery_history) > 100:
            self.recovery_history = self.recovery_history[-100:]
    
    def get_recovery_history(self) -> List[Dict[str, Any]]:
        """Obtener historial de recuperaciones"""
        return self.recovery_history.copy()
    
    def export_recovery_report(self, file_path: str) -> bool:
        """Exportar reporte de recuperaciones a archivo"""
        try:
            report = {
                "generated_at": datetime.now().isoformat(),
                "total_recoveries": len(self.recovery_history),
                "successful_recoveries": sum(1 for entry in self.recovery_history if entry["success"]),
                "failed_recoveries": sum(1 for entry in self.recovery_history if not entry["success"]),
                "history": self.recovery_history
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
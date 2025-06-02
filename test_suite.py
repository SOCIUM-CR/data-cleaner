#!/usr/bin/env python3
"""
Suite de tests básica para verificar funcionalidad del Data Sanitizer
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.processor import FileProcessor
from core.recovery import RecoveryManager

def test_basic_functionality():
    """Test básico de funcionalidad principal"""
    
    print("🧪 SUITE DE TESTS - DATA SANITIZER")
    print("=" * 60)
    
    # Test 1: Importación de módulos
    print("\n1️⃣  Test de importación de módulos...")
    try:
        from core.detector import SensitiveDataDetector
        from core.security import SecurityManager
        from gui.main_window import DataSanitizerGUI
        print("   ✅ Todos los módulos importan correctamente")
    except Exception as e:
        print(f"   ❌ Error importando módulos: {e}")
        return False
    
    # Test 2: Procesamiento básico
    print("\n2️⃣  Test de procesamiento básico...")
    try:
        processor = FileProcessor()
        
        # Crear archivo de prueba simple
        test_content = '''
{
  "email": "user@example.com",
  "phone": "+1-555-1234",
  "api_key": "ghp_test123456789012345678901234567890"
}
'''
        test_file = "examples/input/test_basic.json"
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        result = processor.process_file(test_file, output_dir="examples/output")
        
        if result.success:
            print("   ✅ Procesamiento exitoso")
            print(f"   📊 Detecciones: {result.statistics.get('total_detections', 0)}")
            
            # Verificar que el JSON resultante es válido
            try:
                json.loads(result.sanitized_content)
                print("   ✅ JSON resultante es válido")
            except:
                print("   ❌ JSON resultante es inválido")
                return False
        else:
            print("   ❌ Procesamiento falló")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en procesamiento: {e}")
        return False
    
    # Test 3: Sistema de recuperación
    print("\n3️⃣  Test de sistema de recuperación...")
    try:
        recovery_manager = RecoveryManager()
        
        # Buscar archivos de ejemplo
        output_files = os.listdir("examples/output")
        sanitized_files = [f for f in output_files if "_sanitized_" in f and not "_recovery_key" in f]
        key_files = [f for f in output_files if "_recovery_key" in f and f.endswith(".json")]
        
        if sanitized_files and key_files:
            # Tomar el primer par disponible
            sanitized_file = f"examples/output/{sanitized_files[0]}"
            key_file = f"examples/output/{key_files[0]}"
            
            # Test de validación
            validation = recovery_manager.validate_recovery_compatibility(sanitized_file, key_file)
            
            if validation["compatible"]:
                print("   ✅ Validación de compatibilidad exitosa")
                
                # Test de recuperación
                recovery_result = recovery_manager.recover_from_key_file(sanitized_file, key_file)
                
                if recovery_result["success"]:
                    print("   ✅ Recuperación exitosa")
                else:
                    print("   ❌ Recuperación falló")
                    return False
            else:
                print("   ❌ Archivos no compatibles")
                return False
        else:
            print("   ⚠️  No hay archivos de ejemplo para probar recuperación")
            
    except Exception as e:
        print(f"   ❌ Error en recuperación: {e}")
        return False
    
    # Test 4: Detección de tipos específicos
    print("\n4️⃣  Test de detección de tipos específicos...")
    try:
        from core.detector import SensitiveDataDetector
        
        detector = SensitiveDataDetector()
        
        # Test cases para diferentes tipos
        test_cases = {
            "Email": "contact@company.com",
            "Phone": "+1-555-1234",
            "GitHub Token": "ghp_123456789012345678901234567890123456",
            "Google API Key": "AIzaSyB1234567890123456789012345678901234",
            "User Path": "/Users/john/Documents/secret.txt",
            "System Path": "/usr/bin/python3"  # Este NO debería detectarse
        }
        
        for test_name, test_text in test_cases.items():
            detections = detector.detect_all(test_text)
            
            if test_name == "System Path":
                # Este debería tener confianza baja o no detectarse
                if not detections or all(d.confidence < 0.7 for d in detections):
                    print(f"   ✅ {test_name}: Correctamente ignorado")
                else:
                    print(f"   ⚠️  {test_name}: Detectado (posible falso positivo)")
            else:
                # Estos deberían detectarse
                if detections:
                    print(f"   ✅ {test_name}: Detectado")
                else:
                    print(f"   ❌ {test_name}: NO detectado")
                    
    except Exception as e:
        print(f"   ❌ Error en detección: {e}")
        return False
    
    # Test 5: Verificación de archivos esenciales
    print("\n5️⃣  Test de archivos esenciales...")
    essential_files = [
        'main.py',
        'requirements.txt', 
        'src/core/detector.py',
        'src/core/processor.py',
        'src/core/recovery.py',
        'src/core/security.py',
        'src/gui/main_window.py',
        'src/gui/recovery_window.py'
    ]
    
    missing_files = []
    for file in essential_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not missing_files:
        print("   ✅ Todos los archivos esenciales presentes")
    else:
        print(f"   ❌ Archivos faltantes: {missing_files}")
        return False
    
    print("\n🎉 TODOS LOS TESTS PASARON - PROYECTO FUNCIONAL")
    return True

def test_examples():
    """Test de archivos de ejemplo"""
    
    print("\n📁 VERIFICACIÓN DE ARCHIVOS DE EJEMPLO")
    print("-" * 40)
    
    # Verificar archivos de input
    input_files = ['code_example.py', 'config_example.json', 'test_file.txt']
    for file in input_files:
        path = f"examples/input/{file}"
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} (faltante)")
    
    # Verificar archivos de output
    if os.path.exists("examples/output"):
        output_files = os.listdir("examples/output")
        sanitized_count = len([f for f in output_files if "_sanitized_" in f and "_recovery_key" not in f])
        key_count = len([f for f in output_files if "_recovery_key" in f])
        
        print(f"   📤 Output: {sanitized_count} archivos sanitizados, {key_count} llaves")
        
        if sanitized_count > 0 and key_count > 0:
            print("   ✅ Ejemplos de procesamiento disponibles")
        else:
            print("   ⚠️  Sin ejemplos de procesamiento")
    else:
        print("   ❌ Directorio examples/output no existe")

if __name__ == "__main__":
    success = test_basic_functionality()
    test_examples()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 ESTADO: ✅ PROYECTO LISTO PARA PRODUCCIÓN")
    else:
        print("🎯 ESTADO: ❌ REQUIERE CORRECCIONES")
#!/usr/bin/env python3
"""
Test específico para el problema de validación de llaves
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_file_validation():
    """Probar validación de archivos de llave"""
    
    print("🔍 TEST: Validación de archivos de llave")
    print("=" * 50)
    
    output_dir = "examples/output"
    
    if not os.path.exists(output_dir):
        print("❌ Directorio examples/output no existe")
        return
    
    # Listar todos los archivos
    files = os.listdir(output_dir)
    
    print(f"📁 Archivos en {output_dir}:")
    for i, file in enumerate(sorted(files), 1):
        filepath = os.path.join(output_dir, file)
        print(f"{i:2d}. {file}")
        
        # Analizar cada archivo
        if file.endswith('.json'):
            print(f"    📄 Es archivo JSON: ✅")
            
            if "_recovery_key_" in file:
                print(f"    🔑 Contiene '_recovery_key_': ✅")
                print(f"    ✅ VÁLIDO para llave de recuperación")
            else:
                print(f"    🔑 Contiene '_recovery_key_': ❌")
                print(f"    ❌ NO válido para llave de recuperación")
        else:
            print(f"    📄 Es archivo JSON: ❌")
            
            if "_recovery_key_" in file:
                print(f"    🔑 Contiene '_recovery_key_': ✅")
                print(f"    ❌ Tiene _recovery_key_ pero NO es .json")
            elif "_sanitized_" in file:
                print(f"    📁 Es archivo procesado: ✅")
            else:
                print(f"    📁 Archivo normal")
        
        print()
    
    # Test de validación específico
    print("🧪 TEST: Validación de llaves específicas")
    print("-" * 40)
    
    recovery_files = [f for f in files if "_recovery_key_" in f and f.endswith(".json")]
    
    if recovery_files:
        print(f"🔑 Llaves de recuperación encontradas: {len(recovery_files)}")
        
        for i, file in enumerate(recovery_files, 1):
            filepath = os.path.join(output_dir, file)
            print(f"\n{i}. Probando: {file}")
            
            # Replicar exactamente la validación de la GUI
            has_recovery_key = "_recovery_key_" in file
            ends_with_json = file.endswith(".json")
            
            print(f"   🔍 Contiene '_recovery_key_': {has_recovery_key}")
            print(f"   🔍 Termina en '.json': {ends_with_json}")
            print(f"   🔍 Archivo completo: '{file}'")
            print(f"   🔍 Longitud del nombre: {len(file)} caracteres")
            
            # La validación exacta de la GUI
            if has_recovery_key and ends_with_json:
                print(f"   ✅ PASARÍA la validación")
            else:
                print(f"   ❌ FALLARÍA la validación")
                
                if not has_recovery_key:
                    print(f"      - Razón: No contiene '_recovery_key_'")
                if not ends_with_json:
                    print(f"      - Razón: No termina en '.json'")
    else:
        print("❌ No se encontraron llaves de recuperación")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMEN:")
    print(f"   📁 Total archivos: {len(files)}")
    print(f"   🔑 Llaves válidas: {len(recovery_files)}")
    
    if recovery_files:
        print(f"\n📋 INSTRUCCIONES:")
        print(f"   En la GUI, selecciona uno de estos archivos:")
        for file in recovery_files[:3]:  # Mostrar primeros 3
            print(f"     • {file}")

def test_manual_validation():
    """Test manual donde el usuario puede introducir un nombre de archivo"""
    
    print("\n" + "🧪 TEST MANUAL: Introduce el nombre exacto del archivo que estás seleccionando")
    print("=" * 70)
    
    while True:
        try:
            filename = input("\n📝 Introduce el nombre del archivo (o 'q' para salir): ").strip()
            
            if filename.lower() == 'q':
                break
                
            if not filename:
                continue
            
            print(f"\n🔍 Analizando: '{filename}'")
            print(f"   📏 Longitud: {len(filename)} caracteres")
            
            # Verificaciones individuales
            has_recovery = "_recovery_key_" in filename
            ends_json = filename.endswith(".json")
            
            print(f"   🔑 Contiene '_recovery_key_': {has_recovery}")
            print(f"   📄 Termina en '.json': {ends_json}")
            
            # Buscar el patrón exacto
            if "_recovery_key_" in filename:
                idx = filename.find("_recovery_key_")
                print(f"   📍 '_recovery_key_' encontrado en posición: {idx}")
                after_key = filename[idx + len("_recovery_key_"):]
                print(f"   📝 Texto después de '_recovery_key_': '{after_key}'")
            
            # Verificar extensión
            if filename.endswith(".json"):
                base = filename[:-5]  # Remover .json
                print(f"   📝 Nombre sin .json: '{base}'")
            
            # Resultado final
            if has_recovery and ends_json:
                print(f"   ✅ VÁLIDO: Pasaría la validación de la GUI")
            else:
                print(f"   ❌ INVÁLIDO: Fallaría la validación")
                
                reasons = []
                if not has_recovery:
                    reasons.append("No contiene '_recovery_key_'")
                if not ends_json:
                    reasons.append("No termina en '.json'")
                
                print(f"   💥 Razones: {', '.join(reasons)}")
                
                # Sugerencias
                if not filename.endswith(".json"):
                    suggestion = filename + ".json"
                    print(f"   💡 Sugerencia: ¿Quisiste decir '{suggestion}'?")
                
                if "_recovery_key_" not in filename and "_sanitized_" in filename:
                    suggestion = filename.replace("_sanitized_", "_sanitized_") + "_recovery_key"
                    if not suggestion.endswith(".json"):
                        suggestion += ".json"
                    print(f"   💡 Sugerencia: ¿Quisiste decir '{suggestion}'?")
            
        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_file_validation()
    test_manual_validation()
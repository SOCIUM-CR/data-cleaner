#!/usr/bin/env python3
"""
Data Sanitizer - Versión de línea de comandos
Versión CLI para probar funcionalidad sin GUI
"""

import sys
import os
import argparse
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.processor import FileProcessor
from core.recovery import RecoveryManager


def create_test_file():
    """Crear archivo de prueba con datos sensibles"""
    test_content = """# Documento de ejemplo con datos sensibles

Mi nombre es Juan Pérez y trabajo en TechCorp Inc.
Mi email es juan.perez@techcorp.com
Mi teléfono es +1-555-0123
Mi dirección IP de desarrollo es 192.168.1.100

Configuración del servidor:
- Host: https://api.ejemplo.com/v1
- Base de datos: /home/usuario/db/production.db
- Logs: /var/log/application.log

Información adicional:
- Fecha de nacimiento: 15/03/1985
- Tarjeta de crédito: 4000-1234-5678-9012
- Dirección: 123 Main Street, Springfield

Este archivo contiene información confidencial que debe ser anonimizada.
"""
    
    # Crear directorio si no existe
    os.makedirs("examples/input", exist_ok=True)
    
    with open("examples/input/test_file.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ Archivo de prueba creado: examples/input/test_file.txt")


def process_file_cli(file_path: str, output_dir: str = "examples/output", password: str = None):
    """Procesar archivo usando CLI"""
    processor = FileProcessor()
    
    print(f"🔍 Procesando archivo: {file_path}")
    
    # Vista previa
    print("\n--- VISTA PREVIA ---")
    detections, stats = processor.preview_changes(file_path)
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return False
    
    print(f"📊 Detecciones encontradas: {stats.get('total_detections', 0)}")
    if stats.get('by_type'):
        for data_type, count in stats['by_type'].items():
            print(f"   - {data_type}: {count}")
    
    if stats.get('total_detections', 0) == 0:
        print("ℹ️  No se encontraron datos sensibles")
        return True
    
    # Procesar
    print(f"\n🔄 Procesando archivo...")
    result = processor.process_file(file_path, output_dir, password)
    
    if result.success:
        print(f"✅ Procesamiento exitoso!")
        print(f"📁 Archivo sanitizado: {os.path.join(output_dir, result.sanitized_filename)}")
        
        if result.recovery_key:
            recovery_filename = result.sanitized_filename.replace('.', '_recovery_key.')
            if not recovery_filename.endswith('.json'):
                recovery_filename += '.json'
            print(f"🔑 Llave de recuperación: {os.path.join(output_dir, recovery_filename)}")
        
        print(f"\n📈 Estadísticas:")
        stats = result.statistics
        print(f"   - Total detecciones: {stats.get('total_detections', 0)}")
        print(f"   - Mapeos creados: {stats.get('mappings_created', 0)}")
        print(f"   - Tamaño original: {stats.get('file_size_original', 0)} bytes")
        print(f"   - Tamaño sanitizado: {stats.get('file_size_sanitized', 0)} bytes")
        
        return True
    else:
        print(f"❌ Error en el procesamiento:")
        for error in result.errors:
            print(f"   - {error}")
        return False


def recover_file_cli(processed_file: str, recovery_key_file: str, password: str = None, output_file: str = None):
    """Recuperar archivo usando CLI"""
    recovery_manager = RecoveryManager()
    
    print(f"🔄 Recuperando archivo: {processed_file}")
    print(f"🔑 Usando llave: {recovery_key_file}")
    
    result = recovery_manager.recover_from_key_file(
        processed_file, recovery_key_file, password, output_file
    )
    
    if result["success"]:
        print(f"✅ Recuperación exitosa!")
        if output_file:
            print(f"📁 Archivo recuperado guardado en: {output_file}")
        
        metadata = result["metadata"]
        print(f"\n📈 Información:")
        print(f"   - Hash original: {metadata.get('original_file_hash', 'N/A')[:16]}...")
        print(f"   - Tamaño recuperado: {metadata.get('file_size', 0)} bytes")
        print(f"   - Fecha de recuperación: {metadata.get('recovery_date', 'N/A')}")
        
        if result["warnings"]:
            print(f"\n⚠️  Advertencias:")
            for warning in result["warnings"]:
                print(f"   - {warning}")
        
        return True
    else:
        print(f"❌ Error en la recuperación:")
        for error in result["errors"]:
            print(f"   - {error}")
        return False


def demo_complete_workflow():
    """Demostración completa del flujo de trabajo"""
    print("🚀 DEMO: Flujo completo de Data Sanitizer\n")
    
    # 1. Crear archivo de prueba
    print("1️⃣ Creando archivo de prueba...")
    create_test_file()
    
    # 2. Procesar archivo
    print("\n2️⃣ Procesando archivo...")
    success = process_file_cli("examples/input/test_file.txt", "examples/output", "demo123")
    
    if not success:
        print("❌ Error en el procesamiento, abortando demo")
        return
    
    # 3. Verificar archivos de salida
    output_dir = Path("examples/output")
    sanitized_files = list(output_dir.glob("*_sanitized_*.txt"))
    recovery_files = list(output_dir.glob("*_recovery_key_*.json"))
    
    if not sanitized_files or not recovery_files:
        print("❌ No se encontraron archivos de salida")
        return
    
    sanitized_file = sanitized_files[0]
    recovery_file = recovery_files[0]
    
    print(f"\n3️⃣ Archivos generados:")
    print(f"   📄 Sanitizado: {sanitized_file}")
    print(f"   🔑 Llave: {recovery_file}")
    
    # 4. Mostrar contenido sanitizado
    print(f"\n4️⃣ Contenido sanitizado (primeras 3 líneas):")
    with open(sanitized_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:3]
        for line in lines:
            print(f"   {line.strip()}")
    
    # 5. Recuperar archivo
    print(f"\n5️⃣ Recuperando archivo original...")
    recovered_file = "examples/output/recovered_file.txt"
    success = recover_file_cli(str(sanitized_file), str(recovery_file), "demo123", recovered_file)
    
    if success:
        print(f"\n6️⃣ Verificando recuperación...")
        # Comparar archivos
        with open("examples/input/test_file.txt", 'r') as f:
            original = f.read()
        with open(recovered_file, 'r') as f:
            recovered = f.read()
        
        if original.strip() == recovered.strip():
            print("✅ ¡Recuperación perfecta! Los archivos son idénticos.")
        else:
            print("⚠️  Los archivos difieren ligeramente")
    
    print(f"\n🎉 ¡Demo completado! Revisa los archivos en examples/output/")


def main():
    """Función principal CLI"""
    parser = argparse.ArgumentParser(description="Data Sanitizer - CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando process
    process_parser = subparsers.add_parser('process', help='Procesar archivo')
    process_parser.add_argument('file', help='Archivo a procesar')
    process_parser.add_argument('--output', '-o', default='examples/output', help='Directorio de salida')
    process_parser.add_argument('--password', '-p', help='Contraseña para encriptación')
    
    # Comando recover
    recover_parser = subparsers.add_parser('recover', help='Recuperar archivo')
    recover_parser.add_argument('processed_file', help='Archivo procesado')
    recover_parser.add_argument('recovery_key', help='Archivo de llave de recuperación')
    recover_parser.add_argument('--password', '-p', help='Contraseña para desencriptación')
    recover_parser.add_argument('--output', '-o', help='Archivo de salida')
    
    # Comando demo
    demo_parser = subparsers.add_parser('demo', help='Ejecutar demostración completa')
    
    # Comando test
    test_parser = subparsers.add_parser('test', help='Crear archivo de prueba')
    
    args = parser.parse_args()
    
    if args.command == 'process':
        process_file_cli(args.file, args.output, args.password)
    elif args.command == 'recover':
        recover_file_cli(args.processed_file, args.recovery_key, args.password, args.output)
    elif args.command == 'demo':
        demo_complete_workflow()
    elif args.command == 'test':
        create_test_file()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
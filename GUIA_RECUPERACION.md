# 🔄 Guía de Recuperación de Archivos

## ❌ Problema Identificado

**El usuario reporta**: "la recuperación no me deja cargar un archivo procesado, no se si es la extension o que es un JSON"

## ✅ Solución Implementada

### 🔍 **Problema Real:**
El problema era la **confusión entre archivos procesados y llaves de recuperación**:

- **Archivos procesados (sanitizados)**: `archivo_sanitized_123.txt`, `codigo_sanitized_456.py`
- **Llaves de recuperación**: `archivo_sanitized_123_recovery_key.txt.json`, `codigo_sanitized_456_recovery_key.py.json`

### 🛠️ **Arreglos Implementados:**

#### 1. **Filtros de Archivo Mejorados**
- **Para archivo procesado**: Solo muestra `.txt`, `.py`, `.md`, `.json`, `.log`
- **Para llave de recuperación**: Solo muestra archivos `.json`

#### 2. **Validación Automática**
- Si seleccionas una llave como archivo procesado → **Error claro**
- Si seleccionas un archivo normal como llave → **Error claro**

#### 3. **Ayuda Visual**
- La ventana muestra **automáticamente** todos los archivos disponibles
- **Instrucciones paso a paso** en la pantalla

## 📋 Cómo Usar la Recuperación

### **Paso 1: Abrir Ventana de Recuperación**
```bash
# Opción A: Desde GUI principal
./run_gui.sh
# Luego clic en "Recuperar Archivo"

# Opción B: Ventana independiente
source venv/bin/activate && python test_recovery.py
```

### **Paso 2: Identificar los Archivos Correctos**

**En `examples/output/` verás:**
```
📁 ARCHIVOS PROCESADOS (seleccionar para "Archivo procesado"):
  • test_file_sanitized_20250605_232208_c42fa1f4.txt
  • code_example_sanitized_20250605_230139_b765f11d.py

🔑 LLAVES DE RECUPERACIÓN (seleccionar para "Llave de recuperación"):
  • test_file_sanitized_20250605_232208_c42fa1f4_recovery_key.txt.json
  • code_example_sanitized_20250605_230139_b765f11d_recovery_key.py.json
```

### **Paso 3: Seleccionar Correctamente**

1. **📄 "Archivo procesado"** → Selecciona: `test_file_sanitized_*.txt` (SIN "_recovery_key_")
2. **🔑 "Llave de recuperación"** → Selecciona: `test_file_sanitized_*_recovery_key.txt.json` (CON "_recovery_key_")
3. **🔒 "Contraseña"** → Introduce: `demo123` (o la que usaste)

### **Paso 4: Validar y Recuperar**

1. **Clic en "Validar Archivos"** → Debe decir "✅ Archivos compatibles"
2. **Clic en "Recuperar Archivo"** → Debe mostrar "✅ Recuperación exitosa"

## 🧪 Prueba Paso a Paso

### **Test Completo:**
```bash
# 1. Crear archivo de prueba
./run_cli.sh test

# 2. Procesar con contraseña
./run_cli.sh process examples/input/test_file.txt --password demo123

# 3. Abrir ventana de recuperación
source venv/bin/activate && python test_recovery.py

# 4. En la ventana:
#    - Archivo procesado: test_file_sanitized_[timestamp].txt
#    - Llave: test_file_sanitized_[timestamp]_recovery_key.txt.json
#    - Contraseña: demo123
#    - Clic "Validar" → Clic "Recuperar"
```

## 🔍 Diferencias Clave

| Tipo | Nombre de Archivo | Extensión | Para qué se usa |
|------|------------------|-----------|-----------------|
| **Archivo Procesado** | `archivo_sanitized_123.txt` | `.txt`, `.py`, etc. | Campo "Archivo procesado" |
| **Llave de Recuperación** | `archivo_sanitized_123_recovery_key.txt.json` | `.json` | Campo "Llave de recuperación" |

## ❌ Errores Comunes

### **Error**: "No se puede cargar archivo"
**Causa**: Estás intentando seleccionar una llave (`.json`) como archivo procesado
**Solución**: Selecciona el archivo SIN "_recovery_key_"

### **Error**: "Llave inválida"  
**Causa**: Estás intentando seleccionar un archivo procesado como llave
**Solución**: Selecciona el archivo CON "_recovery_key_" y extensión `.json`

### **Error**: "Archivos incompatibles"
**Causa**: El archivo procesado y la llave no coinciden
**Solución**: Asegúrate de que ambos tengan el mismo timestamp/código

## 🚀 Resultado Esperado

**Al completar correctamente:**
```
✅ Recuperación exitosa!
📁 Archivo guardado en: examples/output/archivo_recuperado.txt
📊 Información:
   - Hash original: abc123...
   - Tamaño recuperado: 566 bytes
   - Fecha de recuperación: 2025-01-06T23:22:08
```

## 📞 Si Sigue Sin Funcionar

**Ejecuta el diagnóstico:**
```bash
python debug_recovery.py
```

**O usa CLI directamente:**
```bash
./run_cli.sh recover archivo_sanitized.txt llave_recovery.json --password tu_contraseña
```
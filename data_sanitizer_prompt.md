# Prompt para Desarrollo de Aplicación de Anonimización Reversible de Datos Sensibles

## Contexto y Objetivo

Desarrolla una aplicación de escritorio multiplataforma que permita procesar archivos de texto en múltiples formatos, identificar y reemplazar datos sensibles con información dummy, y generar un sistema de recuperación que permita restaurar los datos originales después de que el archivo haya sido procesado externamente (por ejemplo, por modelos de IA en la nube).

## Especificaciones Técnicas

### Arquitectura Principal
```
├── Core Engine (Python)
├── GUI Interface (Tkinter/PyQt)
├── Security Module (Cryptography)
├── Pattern Detection (Regex + NLP)
├── File Processors (Multiple formats)
└── Recovery System (Key management)
```

### Funcionalidades Requeridas

#### 1. Detección de Datos Sensibles
La aplicación debe identificar automáticamente:

**Información Personal:**
- Nombres completos (patrones lingüísticos)
- Números de teléfono (todos los formatos internacionales)
- Direcciones (calles, ciudades, códigos postales)
- Emails y dominios corporativos
- Números de documento (DNI, pasaportes, licencias)
- Fechas de nacimiento y datos biométricos

**Información Técnica:**
- Direcciones IP (IPv4/IPv6)
- URLs y endpoints de API
- Contraseñas y tokens de autenticación
- Rutas de sistema (/home/user/, C:\Users\)
- Configuraciones de red y VPN
- Strings de conexión a bases de datos
- Claves SSH y certificados

**Información Corporativa:**
- Nombres de empresas y marcas
- Códigos de empleados
- Números de cuenta y datos financieros
- IDs de proyecto y códigos internos

#### 2. Sistema de Reemplazo Inteligente
```python
# Ejemplo de estructura de reemplazo
{
    "tipo": "nombre_persona",
    "original": "Juan Pérez",
    "dummy": "USER_001", 
    "contexto": "desarrollador senior",
    "posicion": [45, 55]
}
```

#### 3. Generación de Llaves de Recuperación
- Encriptación AES-256 de la tabla de mapeo
- Generación de hash único por archivo
- Metadatos de versión y timestamp
- Integridad verificable con checksums

#### 4. Formatos de Archivo Soportados
- Texto plano (.txt, .md, .rst)
- Documentos (.docx, .pdf, .odt)
- Código fuente (.py, .js, .java, .cpp, etc.)
- Configuración (.json, .yaml, .xml, .ini)
- Logs y reportes (.log, .csv)

## Implementación Detallada

### Módulo de Detección (detector.py)
```python
class SensitiveDataDetector:
    def __init__(self):
        self.patterns = {
            'phone': [
                r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            ],
            'email': [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            'ip_address': [
                r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'
            ],
            'file_path': [
                r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*',
                r'/(?:[^/\s]+/)*[^/\s]*'
            ]
        }
    
    def detect_sensitive_data(self, text):
        # Implementar lógica de detección
        pass
```

### Sistema de Encriptación (security.py)
```python
class SecurityManager:
    def generate_recovery_key(self, mapping_data):
        # Generar clave única y encriptar mapeo
        pass
    
    def create_dummy_replacements(self, detected_data):
        # Crear reemplazos coherentes y realistas
        pass
    
    def recover_original_data(self, processed_file, recovery_key):
        # Restaurar datos originales
        pass
```

### Interfaz de Usuario
```python
class DataSanitizerGUI:
    def __init__(self):
        # Ventana principal con drag & drop
        # Configuración de tipos de datos a detectar
        # Preview de cambios antes de procesar
        # Generación y gestión de llaves
        pass
```

## Características Avanzadas

### 1. Modo Inteligente
- Aprendizaje de patrones específicos del usuario
- Whitelist de términos que no deben ser reemplazados
- Detección contextual (no reemplazar "Python" en código)

### 2. Validación y Preview
- Vista lado a lado (original vs. sanitizado)
- Resaltado de cambios propuestos
- Estadísticas de datos detectados y reemplazados

### 3. Gestión de Llaves
- Base de datos local de llaves de recuperación
- Backup y restauración de llaves
- Expiración automática por seguridad

### 4. Modo Batch
- Procesamiento de múltiples archivos
- Mantenimiento de consistencia entre archivos relacionados
- Reportes de procesamiento

## Consideraciones de Seguridad

### Protección Local
- Las llaves nunca abandonan el sistema local
- Encriptación en reposo de toda la base de datos
- Borrado seguro de archivos temporales

### Integridad
- Verificación de integridad antes de recuperación
- Detección de manipulación en archivos procesados
- Logging de todas las operaciones críticas

## Flujo de Trabajo Típico

```
1. Usuario arrastra archivo → Aplicación
2. Detección automática de datos sensibles
3. Preview de cambios propuestos
4. Confirmación y procesamiento
5. Generación de archivo sanitizado + llave de recuperación
6. [Usuario procesa archivo externamente]
7. Usuario trae archivo procesado + llave
8. Recuperación automática de datos sensibles
9. Archivo final con datos originales restaurados
```

## Entregables Esperados

1. **Aplicación ejecutable** para Windows, macOS y Linux
2. **Documentación completa** de instalación y uso
3. **Código fuente modular** y bien documentado
4. **Tests unitarios** para todas las funcionalidades críticas
5. **Manual de usuario** con ejemplos prácticos
6. **Configuraciones predefinidas** para casos de uso comunes

## Criterios de Éxito

- **Precisión**: >95% en detección de datos sensibles comunes
- **Seguridad**: Imposibilidad de recuperar datos sin la llave
- **Usabilidad**: Procesamiento completo en <5 clics
- **Performance**: Archivos de hasta 50MB procesados en <30 segundos
- **Compatibilidad**: Funcionamiento en Python 3.8+

## Especificaciones Técnicas Adicionales

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Memoria RAM**: Mínimo 512MB, recomendado 2GB
- **Espacio en disco**: 100MB para instalación + espacio para archivos procesados
- **Dependencias principales**:
  - `cryptography` para encriptación
  - `regex` para detección de patrones
  - `tkinter/PyQt5` para interfaz gráfica
  - `python-docx`, `PyPDF2` para manejo de documentos

### Estructura de Archivos de Salida
```
proyecto_sanitizado/
├── archivo_sanitizado.txt
├── recovery_key.enc
├── metadata.json
└── backup/
    └── original_hash.sha256
```

### API Interna Sugerida
```python
# Ejemplo de uso programático
sanitizer = DataSanitizer()
result = sanitizer.process_file(
    input_path="documento_original.txt",
    output_path="documento_sanitizado.txt",
    sensitivity_level="high",
    generate_preview=True
)
```

---

**Nota Importante**: La aplicación debe ser completamente offline y no requerir conexión a internet para su funcionamiento, garantizando que los datos sensibles nunca abandonen el entorno local del usuario.

## Próximos Pasos Sugeridos

1. **Prototipo MVP**: Comenzar con detección básica de emails, teléfonos e IPs
2. **Interfaz mínima**: Línea de comandos antes que GUI completa
3. **Pruebas de concepto**: Validar el sistema de encriptación/recuperación
4. **Iteración**: Expandir tipos de datos detectados progresivamente
5. **Testing**: Casos de prueba con archivos reales anonimizados
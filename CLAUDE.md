# Data Sanitizer - Anonimización Reversible de Datos Sensibles

## Descripción del Proyecto
Aplicación de escritorio multiplataforma para anonimización reversible de datos sensibles. Permite procesar archivos de texto, identificar y reemplazar datos sensibles con información dummy, y generar un sistema de recuperación que permite restaurar los datos originales.

## Arquitectura del Sistema
```
├── Core Engine (Python)
├── GUI Interface (Tkinter)
├── Security Module (Cryptography)
├── Pattern Detection (Regex + NLP)
├── File Processors (Multiple formats)
└── Recovery System (Key management)
```

## Estructura del Proyecto
```
data-cleaner/
├── src/                        # Código fuente principal
│   ├── core/
│   │   ├── detector.py          # Detección de datos sensibles
│   │   ├── security.py          # Encriptación y manejo de llaves
│   │   ├── processor.py         # Procesamiento de archivos
│   │   └── recovery.py          # Sistema de recuperación
│   ├── gui/
│   │   ├── main_window.py       # Ventana principal
│   │   ├── preview_window.py    # Vista previa de cambios
│   │   └── key_manager.py       # Gestión de llaves
│   ├── utils/
│   │   ├── file_handlers.py     # Manejo de diferentes formatos
│   │   ├── patterns.py          # Patrones de detección
│   │   └── dummy_generator.py   # Generación de datos dummy
│   └── tests/
│       ├── test_detector.py
│       ├── test_security.py
│       └── test_processor.py
├── examples/                   # Archivos de ejemplo y pruebas
│   ├── input/                  # Archivos de entrada para testing
│   └── output/                 # Resultados de procesamiento
├── data/                       # Datos de la aplicación
│   ├── patterns/               # Patrones de detección personalizados
│   └── keys/                   # Almacenamiento local de llaves
├── config/                     # Archivos de configuración
├── temp/                       # Archivos temporales
├── logs/                       # Logs de la aplicación
├── docs/                       # Documentación
│   ├── user_manual.md
│   └── api_reference.md
├── venv/                       # Entorno virtual Python
├── requirements.txt
├── setup.py
├── main.py                     # Entrada principal GUI
├── cli.py                      # Entrada CLI
├── README.md                   # Documentación principal
├── CLAUDE.md                   # Información técnica del proyecto
├── TASKS.md                    # Seguimiento de tareas
└── data_sanitizer_prompt.md    # Especificaciones originales
```

## Tecnologías Principales
- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica multiplataforma  
- **cryptography**: Encriptación AES-256
- **regex**: Detección avanzada de patrones
- **python-docx, PyPDF2**: Manejo de documentos
- **pytest**: Testing unitario

## Tipos de Datos Detectados

### Información Personal
- Nombres completos
- Números de teléfono (formatos internacionales)
- Direcciones postales
- Emails y dominios corporativos
- Números de documento (DNI, pasaportes)
- Fechas de nacimiento

### Información Técnica
- Direcciones IP (IPv4/IPv6)
- URLs y endpoints de API
- Tokens de autenticación
- Rutas de sistema
- Configuraciones de red
- Strings de conexión a BD
- Claves SSH y certificados

### Información Corporativa
- Nombres de empresas
- Códigos de empleados
- Datos financieros
- IDs de proyecto

## Formatos Soportados
- Texto plano (.txt, .md, .rst)
- Documentos (.docx, .pdf, .odt)
- Código fuente (.py, .js, .java, .cpp, etc.)
- Configuración (.json, .yaml, .xml, .ini)
- Logs y reportes (.log, .csv)

## Flujo de Trabajo
1. Usuario arrastra archivo → Aplicación
2. Detección automática de datos sensibles
3. Preview de cambios propuestos
4. Confirmación y procesamiento
5. Generación de archivo sanitizado + llave de recuperación
6. [Usuario procesa archivo externamente]
7. Usuario trae archivo procesado + llave
8. Recuperación automática de datos sensibles
9. Archivo final con datos originales restaurados

## Comandos de Desarrollo

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar aplicación
```bash
python main.py
```

### Ejecutar tests
```bash
pytest src/tests/
```

### Lint y formato
```bash
flake8 src/
black src/
```

## Criterios de Éxito
- **Precisión**: >95% en detección de datos sensibles comunes
- **Seguridad**: Imposibilidad de recuperar datos sin la llave
- **Usabilidad**: Procesamiento completo en <5 clics
- **Performance**: Archivos de hasta 50MB procesados en <30 segundos
- **Compatibilidad**: Funcionamiento en Python 3.8+

## Consideraciones de Seguridad
- Las llaves nunca abandonan el sistema local
- Encriptación en reposo de toda la base de datos
- Borrado seguro de archivos temporales
- Verificación de integridad antes de recuperación
- Logging de todas las operaciones críticas

## Estado del Proyecto
- **Versión actual**: 0.1.0 (En desarrollo)
- **Última actualización**: Enero 2025
- **Próximo milestone**: MVP con detección básica

## Notas Importantes
- La aplicación funciona completamente offline
- No requiere conexión a internet
- Los datos sensibles nunca abandonan el entorno local
- Sistema de backup automático de llaves de recuperación
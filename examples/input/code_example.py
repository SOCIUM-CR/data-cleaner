# Archivo de código Python con datos sensibles

import requests
import os

# Configuración de desarrollo
DB_HOST = "192.168.1.50"
DB_USER = "admin"
DB_PASS = "my_secret_password123"
API_KEY = "sk-abcd1234567890efghij"

# Información del desarrollador
DEVELOPER_EMAIL = "developer@example.com"
DEVELOPER_PHONE = "+1-555-0199"

def connect_to_database():
    """Conectar a la base de datos de producción"""
    connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/production_db"
    print(f"Conectando a: {connection_string}")
    return connection_string

def send_notification(message):
    """Enviar notificación al equipo"""
    webhook_url = "https://hooks.example.com/services/T123456/B123456/abc123def456"
    data = {
        "text": message,
        "channel": "#alerts",
        "username": "Production Bot"
    }
    
    # Log de debug
    log_file = "/var/log/myapp/notifications.log"
    print(f"Enviando notificación desde {DEVELOPER_EMAIL}")
    print(f"Log guardado en: {log_file}")
    
    return requests.post(webhook_url, json=data)

# Datos de prueba
TEST_USERS = [
    {"name": "Juan Pérez", "email": "juan.perez@example.com", "phone": "555-0123"},
    {"name": "María García", "email": "maria.garcia@example.com", "phone": "555-0124"},
]

if __name__ == "__main__":
    print("Iniciando aplicación...")
    print(f"Contacto de soporte: {DEVELOPER_EMAIL}")
    connect_to_database()
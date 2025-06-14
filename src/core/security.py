"""
Módulo de seguridad y encriptación
Maneja la generación de llaves, encriptación de mapeos y recuperación de datos
"""

import json
import hashlib
import secrets
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


@dataclass
class MappingEntry:
    """Entrada de mapeo entre dato original y dummy"""
    original: str
    dummy: str
    data_type: str
    position: tuple
    context: str
    confidence: float


@dataclass
class RecoveryKey:
    """Llave de recuperación con metadatos"""
    file_hash: str
    mapping_data: str  # Datos encriptados
    timestamp: str
    version: str
    salt: str
    checksum: str
    encryption_key: Optional[str] = None  # Clave de encriptación (solo cuando no hay password)


class SecurityManager:
    """Gestor de seguridad para encriptación y recuperación"""
    
    def __init__(self):
        """Inicializar gestor de seguridad"""
        self.version = "1.0.0"
        self.key_derivation_iterations = 100000
    
    def generate_recovery_key(self, mapping_data: List[MappingEntry], 
                            original_file_content: str, 
                            password: Optional[str] = None) -> RecoveryKey:
        """Generar llave de recuperación encriptada"""
        
        # Generar hash del archivo original
        file_hash = self._generate_file_hash(original_file_content)
        
        # Convertir mapeos a formato serializable
        serializable_mappings = [asdict(mapping) for mapping in mapping_data]
        mapping_json = json.dumps(serializable_mappings, ensure_ascii=False, indent=2)
        
        # Generar salt único
        salt = secrets.token_bytes(32)
        
        # Generar clave de encriptación
        stored_key = None
        if password:
            encryption_key = self._derive_key_from_password(password, salt)
        else:
            encryption_key = Fernet.generate_key()
            stored_key = base64.b64encode(encryption_key).decode('utf-8')
        
        # Encriptar datos de mapeo
        fernet = Fernet(encryption_key)
        encrypted_mapping = fernet.encrypt(mapping_json.encode('utf-8'))
        
        # Generar checksum de integridad
        checksum = self._generate_checksum(mapping_json, file_hash)
        
        # Crear llave de recuperación
        recovery_key = RecoveryKey(
            file_hash=file_hash,
            mapping_data=base64.b64encode(encrypted_mapping).decode('utf-8'),
            timestamp=datetime.now().isoformat(),
            version=self.version,
            salt=base64.b64encode(salt).decode('utf-8'),
            checksum=checksum,
            encryption_key=stored_key
        )
        
        return recovery_key
    
    def save_recovery_key(self, recovery_key: RecoveryKey, filepath: str) -> bool:
        """Guardar llave de recuperación en archivo"""
        try:
            recovery_data = asdict(recovery_key)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(recovery_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando llave de recuperación: {e}")
            return False
    
    def load_recovery_key(self, filepath: str) -> Optional[RecoveryKey]:
        """Cargar llave de recuperación desde archivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Backward compatibility: si no existe encryption_key, añadirla como None
            if 'encryption_key' not in data:
                data['encryption_key'] = None
                
            return RecoveryKey(**data)
        except Exception as e:
            print(f"Error cargando llave de recuperación: {e}")
            return None
    
    def recover_original_data(self, processed_content: str, 
                            recovery_key: RecoveryKey, 
                            password: Optional[str] = None) -> Optional[str]:
        """Recuperar datos originales usando la llave de recuperación"""
        
        try:
            # Verificar integridad del archivo procesado
            if not self._verify_file_integrity(processed_content, recovery_key):
                print("Advertencia: El archivo procesado puede haber sido modificado")
            
            # Desencriptar datos de mapeo
            salt = base64.b64decode(recovery_key.salt.encode('utf-8'))
            
            if password:
                encryption_key = self._derive_key_from_password(password, salt)
            elif recovery_key.encryption_key:
                # Usar la clave almacenada (archivo sin contraseña)
                encryption_key = base64.b64decode(recovery_key.encryption_key.encode('utf-8'))
            else:
                print("Error: No se puede recuperar el archivo. Se requiere contraseña o clave de encriptación.")
                return None
            
            # Desencriptar mapeos
            fernet = Fernet(encryption_key)
            encrypted_mapping = base64.b64decode(recovery_key.mapping_data.encode('utf-8'))
            decrypted_mapping = fernet.decrypt(encrypted_mapping)
            
            # Deserializar mapeos
            mapping_data = json.loads(decrypted_mapping.decode('utf-8'))
            mappings = [MappingEntry(**mapping) for mapping in mapping_data]
            
            # Aplicar recuperación en orden inverso (de final a inicio)
            recovered_content = processed_content
            mappings.sort(key=lambda x: x.position[0], reverse=True)
            
            for mapping in mappings:
                start, end = mapping.position
                # Buscar y reemplazar dummy con original
                recovered_content = recovered_content.replace(
                    mapping.dummy, mapping.original, 1
                )
            
            return recovered_content
            
        except Exception as e:
            print(f"Error durante la recuperación: {e}")
            return None
    
    def create_dummy_replacements(self, detections: List[Any]) -> List[MappingEntry]:
        """Crear reemplazos dummy para las detecciones"""
        mappings = []
        dummy_counters = {}
        
        for detection in detections:
            data_type = detection.data_type.value
            
            # Incrementar contador para este tipo
            if data_type not in dummy_counters:
                dummy_counters[data_type] = 0
            dummy_counters[data_type] += 1
            
            # Generar reemplazo dummy
            dummy_text = self._generate_dummy_text(data_type, dummy_counters[data_type])
            
            mapping = MappingEntry(
                original=detection.original_text,
                dummy=dummy_text,
                data_type=data_type,
                position=(detection.start_position, detection.end_position),
                context=detection.context,
                confidence=detection.confidence
            )
            
            mappings.append(mapping)
        
        return mappings
    
    def _generate_dummy_text(self, data_type: str, counter: int) -> str:
        """Generar texto dummy realista según el tipo de dato"""
        dummy_patterns = {
            'email': f'user{counter:03d}@example.com',
            'phone': f'+1-555-{counter:04d}',
            'ip_address': f'192.168.1.{counter % 254 + 1}',
            'file_path': f'/home/user{counter}/document{counter}.txt',
            'url': f'https://example{counter}.com/path',
            'person_name': f'Person{counter:03d}',
            'credit_card': f'4000-0000-0000-{counter:04d}',
            'date': f'2024-01-{counter % 28 + 1:02d}',
            'address': f'{counter} Example Street, City{counter}',
            'api_key': f'DUMMY_API_KEY_{counter:06d}_{"a" * 32}',
            'access_token': f'DUMMY_ACCESS_TOKEN_{counter:06d}_{"b" * 40}'
        }
        
        return dummy_patterns.get(data_type, f'DUMMY_{data_type.upper()}_{counter:03d}')
    
    def _generate_file_hash(self, content: str) -> str:
        """Generar hash SHA-256 del contenido del archivo"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _generate_checksum(self, mapping_data: str, file_hash: str) -> str:
        """Generar checksum de integridad"""
        combined = mapping_data + file_hash + self.version
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def _derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """Derivar clave de encriptación desde contraseña"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.key_derivation_iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key
    
    def _verify_file_integrity(self, content: str, recovery_key: RecoveryKey) -> bool:
        """Verificar que el archivo no ha sido comprometido"""
        # Esta es una verificación básica
        # En una implementación completa, se podría usar checksums más sofisticados
        return True
    
    def generate_secure_filename(self, original_filename: str) -> str:
        """Generar nombre de archivo seguro para archivos sanitizados"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(4)
        name_part = original_filename.rsplit('.', 1)[0] if '.' in original_filename else original_filename
        extension = original_filename.rsplit('.', 1)[1] if '.' in original_filename else 'txt'
        
        return f"{name_part}_sanitized_{timestamp}_{random_suffix}.{extension}"
    
    def validate_recovery_key(self, recovery_key: RecoveryKey) -> bool:
        """Validar que una llave de recuperación es válida"""
        try:
            # Verificar que tiene todos los campos requeridos
            required_fields = ['file_hash', 'mapping_data', 'timestamp', 'version', 'salt', 'checksum']
            recovery_dict = asdict(recovery_key)
            
            for field in required_fields:
                if field not in recovery_dict or not recovery_dict[field]:
                    return False
            
            # Verificar que los datos base64 son válidos
            base64.b64decode(recovery_key.mapping_data)
            base64.b64decode(recovery_key.salt)
            
            # Si hay encryption_key, también debe ser base64 válido
            if recovery_key.encryption_key:
                base64.b64decode(recovery_key.encryption_key)
            
            # Verificar formato de timestamp
            datetime.fromisoformat(recovery_key.timestamp)
            
            return True
            
        except Exception:
            return False
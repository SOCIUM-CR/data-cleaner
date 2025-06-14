"""
Módulo de detección de datos sensibles
Identifica automáticamente diferentes tipos de información sensible en texto
"""

import re
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class SensitiveDataType(Enum):
    """Tipos de datos sensibles detectables"""
    EMAIL = "email"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    FILE_PATH = "file_path"
    URL = "url"
    PERSON_NAME = "person_name"
    CREDIT_CARD = "credit_card"
    SSN = "ssn"
    DATE = "date"
    ADDRESS = "address"
    API_KEY = "api_key"
    ACCESS_TOKEN = "access_token"


@dataclass
class Detection:
    """Representa una detección de dato sensible"""
    data_type: SensitiveDataType
    original_text: str
    start_position: int
    end_position: int
    confidence: float
    context: str = ""
    

class SensitiveDataDetector:
    """Detector principal de datos sensibles"""
    
    def __init__(self):
        """Inicializar detector con patrones predefinidos"""
        self.patterns = self._load_patterns()
        self.min_confidence = 0.7
    
    def _load_patterns(self) -> Dict[SensitiveDataType, List[str]]:
        """Cargar patrones regex para cada tipo de dato"""
        return {
            SensitiveDataType.EMAIL: [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            
            SensitiveDataType.PHONE: [
                # Más específicos para evitar puertos/números normales
                r'\+\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{4,9}',  # Internacional con +
                r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',  # (XXX) XXX-XXXX
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b(?=\s|$|[^\d])'  # XXX-XXX-XXXX (no parte de número más largo)
            ],
            
            SensitiveDataType.IP_ADDRESS: [
                r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'
            ],
            
            SensitiveDataType.FILE_PATH: [
                # Rutas específicas que SÍ son sensibles (no rutas del sistema)
                r'/(?:home|Users)/[^/\s"\']+(?:/[^/\s"\']+)*',  # Rutas de usuario
                r'[A-Za-z]:\\(?:Users|Documents)\\(?:[^\\/:*?"<>|\r\n\'"]+\\)*[^\\/:*?"<>|\r\n\'"]*',  # Windows user paths
                r'~[/\\](?:[^/\\\s"\']+[/\\])*[^/\\\s"\']*'  # Home paths
            ],
            
            SensitiveDataType.URL: [
                r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            ],
            
            SensitiveDataType.CREDIT_CARD: [
                r'\b4[0-9]{12}(?:[0-9]{3})?\b',  # Visa
                r'\b5[1-5][0-9]{14}\b',          # MasterCard
                r'\b3[47][0-9]{13}\b'            # American Express
            ],
            
            SensitiveDataType.DATE: [
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',
                r'\b\d{1,2}-\d{1,2}-\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b'
            ],
            
            SensitiveDataType.API_KEY: [
                # GitHub tokens
                r'\bghp_[A-Za-z0-9]{36}\b',
                r'\bgho_[A-Za-z0-9]{36}\b',
                r'\bghu_[A-Za-z0-9]{36}\b',
                r'\bghs_[A-Za-z0-9]{36}\b',
                r'\bghr_[A-Za-z0-9]{36}\b',
                # Google API keys
                r'\bAIza[A-Za-z0-9_-]{35}\b',
                # AWS keys
                r'\bAKIA[A-Z0-9]{16}\b',
                # Generic API key patterns
                r'\b[A-Za-z0-9]{32,64}\b(?=\s|$|["\',}])',  # 32-64 char strings
            ],
            
            SensitiveDataType.ACCESS_TOKEN: [
                # HubSpot tokens
                r'\bpat-[a-z0-9]{2}\d-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b',
                # Notion tokens
                r'\bntn_[A-Za-z0-9]{40,50}\b',
                # JWT tokens
                r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b',
                # Bearer tokens
                r'\b[A-Za-z0-9+/]{40,}\b(?=\s|$|["\',}])',
            ]
        }
    
    def detect_all(self, text: str) -> List[Detection]:
        """Detectar todos los tipos de datos sensibles en el texto"""
        detections = []
        
        for data_type, patterns in self.patterns.items():
            detections.extend(self._detect_type(text, data_type, patterns))
        
        # Ordenar por posición en el texto
        detections.sort(key=lambda x: x.start_position)
        
        # Resolver conflictos de superposición
        return self._resolve_overlaps(detections)
    
    def _detect_type(self, text: str, data_type: SensitiveDataType, patterns: List[str]) -> List[Detection]:
        """Detectar un tipo específico de dato sensible"""
        detections = []
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                context = self._extract_context(text, match.start(), match.end())
                detection = Detection(
                    data_type=data_type,
                    original_text=match.group(),
                    start_position=match.start(),
                    end_position=match.end(),
                    confidence=self._calculate_confidence(match.group(), data_type, context),
                    context=context
                )
                
                if detection.confidence >= self.min_confidence:
                    detections.append(detection)
        
        return detections
    
    def _calculate_confidence(self, text: str, data_type: SensitiveDataType, context: str = "") -> float:
        """Calcular confianza de la detección"""
        # Implementación básica - puede ser mejorada con ML
        base_confidence = 0.8
        
        # Ajustar confianza basado en características del texto
        if data_type == SensitiveDataType.EMAIL:
            if '@' in text and '.' in text.split('@')[1]:
                base_confidence = 0.95
        
        elif data_type == SensitiveDataType.PHONE:
            # Reducir confianza si parece un puerto o número pequeño
            if text.isdigit() and len(text) <= 4:
                base_confidence = 0.3  # Probablemente un puerto
            elif any(char in text for char in ['(', ')', '-', '.', '+']):
                base_confidence = 0.9
            elif len(text) < 10:  # Números muy cortos probablemente no son teléfonos
                base_confidence = 0.4
        
        elif data_type == SensitiveDataType.IP_ADDRESS:
            # Validar rangos de IP
            parts = text.split('.')
            if len(parts) == 4:
                try:
                    if all(0 <= int(part) <= 255 for part in parts):
                        base_confidence = 0.95
                    else:
                        base_confidence = 0.3  # Fuera de rango válido
                except ValueError:
                    base_confidence = 0.5
        
        elif data_type == SensitiveDataType.FILE_PATH:
            # Reducir confianza para rutas del sistema que no deberían ser reemplazadas
            if len(text) < 5:
                base_confidence = 0.4
            elif text.startswith('http'):
                base_confidence = 0.2  # Probablemente parte de URL
            elif any(sys_path in text.lower() for sys_path in ['/usr/', '/bin/', '/sbin/', '/opt/', '/etc/', '/var/log']):
                base_confidence = 0.3  # Rutas del sistema, menor confianza
            elif 'node_modules' in text or '.nvm' in text:
                base_confidence = 0.4  # Rutas de herramientas, menor confianza
            elif text.startswith('/home/') or text.startswith('/Users/') or '~/' in text:
                base_confidence = 0.9  # Rutas de usuario, alta confianza
        
        elif data_type == SensitiveDataType.API_KEY:
            # Alta confianza para patrones específicos de API keys
            if text.startswith(('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_')):
                base_confidence = 0.98  # GitHub tokens
            elif text.startswith('AIza'):
                base_confidence = 0.98  # Google API keys
            elif text.startswith('AKIA'):
                base_confidence = 0.98  # AWS keys
            elif len(text) >= 32:
                base_confidence = 0.85  # Generic long keys
            
        elif data_type == SensitiveDataType.ACCESS_TOKEN:
            # Alta confianza para tokens específicos
            if text.startswith('pat-'):
                base_confidence = 0.98  # HubSpot tokens
            elif text.startswith('ntn_'):
                base_confidence = 0.98  # Notion tokens
            elif text.startswith('eyJ'):
                base_confidence = 0.95  # JWT tokens
            elif len(text) >= 40:
                base_confidence = 0.85  # Generic long tokens
        
        return min(base_confidence, 1.0)
    
    def _extract_context(self, text: str, start: int, end: int, context_size: int = 20) -> str:
        """Extraer contexto alrededor de la detección"""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:context_end].strip()
    
    def _resolve_overlaps(self, detections: List[Detection]) -> List[Detection]:
        """Resolver superposiciones entre detecciones"""
        if not detections:
            return detections
        
        resolved = []
        current = detections[0]
        
        for next_detection in detections[1:]:
            # Si no hay superposición, agregar el actual y continuar
            if current.end_position <= next_detection.start_position:
                resolved.append(current)
                current = next_detection
            else:
                # Hay superposición - mantener el de mayor confianza
                if next_detection.confidence > current.confidence:
                    current = next_detection
        
        resolved.append(current)
        return resolved
    
    def get_statistics(self, detections: List[Detection]) -> Dict[str, Any]:
        """Obtener estadísticas de las detecciones"""
        stats = {
            'total_detections': len(detections),
            'by_type': {},
            'average_confidence': 0.0
        }
        
        if detections:
            # Contar por tipo
            for detection in detections:
                type_name = detection.data_type.value
                stats['by_type'][type_name] = stats['by_type'].get(type_name, 0) + 1
            
            # Calcular confianza promedio
            total_confidence = sum(d.confidence for d in detections)
            stats['average_confidence'] = total_confidence / len(detections)
        
        return stats
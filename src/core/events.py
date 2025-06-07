"""
Définition des événements de sécurité Orion
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Any
from dataclasses import dataclass, field


class EventType(Enum):
    """Types d'événements de sécurité."""
    # Événements Active Directory
    AD_LOGON = "ad_logon"
    AD_LOGOFF = "ad_logoff"
    AD_ACCOUNT_CREATED = "ad_account_created"
    AD_ACCOUNT_MODIFIED = "ad_account_modified"
    AD_ACCOUNT_DELETED = "ad_account_deleted"
    AD_GROUP_MODIFIED = "ad_group_modified"
    AD_PRIVILEGE_ESCALATION = "ad_privilege_escalation"
    AD_PASSWORD_CHANGE = "ad_password_change"
    AD_GPO_MODIFIED = "ad_gpo_modified"
    
    # Événements réseau
    NETWORK_CONNECTION = "network_connection"
    NETWORK_DNS_QUERY = "network_dns_query"
    NETWORK_SUSPICIOUS_TRAFFIC = "network_suspicious_traffic"
    
    # Événements Kerberos
    KERBEROS_TGT_REQUEST = "kerberos_tgt_request"
    KERBEROS_TGS_REQUEST = "kerberos_tgs_request"
    KERBEROS_AUTHENTICATION_FAILURE = "kerberos_auth_failure"
    
    # Événements de déception (Hydra)
    DECOY_INTERACTION = "decoy_interaction"
    HONEYPOT_ACCESS = "honeypot_access"
    
    # Événements système
    PROCESS_CREATION = "process_creation"
    FILE_ACCESS = "file_access"
    REGISTRY_MODIFICATION = "registry_modification"


class RiskLevel(Enum):
    """Niveaux de risque."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class Severity(Enum):
    """Niveaux de sévérité."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class UserContext:
    """Contexte utilisateur pour un événement."""
    username: str
    domain: str
    user_id: Optional[str] = None
    email: Optional[str] = None
    groups: list[str] = field(default_factory=list)
    privileges: list[str] = field(default_factory=list)
    last_logon: Optional[datetime] = None
    risk_score: float = 0.0


@dataclass
class DeviceContext:
    """Contexte de l'appareil pour un événement."""
    hostname: str
    ip_address: str
    mac_address: Optional[str] = None
    operating_system: Optional[str] = None
    domain_joined: bool = False
    last_seen: Optional[datetime] = None
    risk_score: float = 0.0


@dataclass
class NetworkContext:
    """Contexte réseau pour un événement."""
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    bytes_transferred: Optional[int] = None
    duration: Optional[float] = None


@dataclass
class SecurityEvent:
    """Événement de sécurité principal d'Orion."""
    
    # Identifiants
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: EventType = EventType.AD_LOGON
    
    # Classification
    severity: Severity = Severity.INFO
    risk_level: RiskLevel = RiskLevel.LOW
    confidence: float = 1.0  # 0.0 à 1.0
    
    # Contextes
    user_context: Optional[UserContext] = None
    device_context: Optional[DeviceContext] = None
    network_context: Optional[NetworkContext] = None
    
    # Données de l'événement
    raw_data: Dict[str, Any] = field(default_factory=dict)
    enriched_data: Dict[str, Any] = field(default_factory=dict)
    
    # Métadonnées
    source: str = "unknown"  # Source de l'événement (agent, module, etc.)
    correlation_id: Optional[str] = None  # Pour grouper les événements liés
    parent_event_id: Optional[str] = None  # Événement parent si applicable
    
    # Tags et labels
    tags: list[str] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)
    
    # Traitement
    processed_by: list[str] = field(default_factory=list)  # Modules qui ont traité l'événement
    processing_time: Optional[float] = None  # Temps de traitement en secondes
    
    def __post_init__(self):
        """Validation et initialisation post-création."""
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("La confiance doit être entre 0.0 et 1.0")
        
        # Ajout de tags automatiques basés sur le type d'événement
        if self.event_type.value.startswith('ad_'):
            self.tags.append('active_directory')
        elif self.event_type.value.startswith('network_'):
            self.tags.append('network')
        elif self.event_type.value.startswith('kerberos_'):
            self.tags.append('kerberos')
        elif self.event_type.value.startswith('decoy_'):
            self.tags.append('deception')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'événement en dictionnaire pour sérialisation."""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type.value,
            'severity': self.severity.value,
            'risk_level': self.risk_level.value,
            'confidence': self.confidence,
            'user_context': self.user_context.__dict__ if self.user_context else None,
            'device_context': self.device_context.__dict__ if self.device_context else None,
            'network_context': self.network_context.__dict__ if self.network_context else None,
            'raw_data': self.raw_data,
            'enriched_data': self.enriched_data,
            'source': self.source,
            'correlation_id': self.correlation_id,
            'parent_event_id': self.parent_event_id,
            'tags': self.tags,
            'labels': self.labels,
            'processed_by': self.processed_by,
            'processing_time': self.processing_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityEvent':
        """Crée un événement à partir d'un dictionnaire."""
        # Conversion des énumérations
        event_type = EventType(data.get('event_type', 'ad_logon'))
        severity = Severity(data.get('severity', 'info'))
        risk_level = RiskLevel(data.get('risk_level', 2))
        
        # Conversion de la timestamp
        timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else datetime.now()
        
        # Reconstruction des contextes
        user_context = UserContext(**data['user_context']) if data.get('user_context') else None
        device_context = DeviceContext(**data['device_context']) if data.get('device_context') else None
        network_context = NetworkContext(**data['network_context']) if data.get('network_context') else None
        
        return cls(
            event_id=data.get('event_id', str(uuid.uuid4())),
            timestamp=timestamp,
            event_type=event_type,
            severity=severity,
            risk_level=risk_level,
            confidence=data.get('confidence', 1.0),
            user_context=user_context,
            device_context=device_context,
            network_context=network_context,
            raw_data=data.get('raw_data', {}),
            enriched_data=data.get('enriched_data', {}),
            source=data.get('source', 'unknown'),
            correlation_id=data.get('correlation_id'),
            parent_event_id=data.get('parent_event_id'),
            tags=data.get('tags', []),
            labels=data.get('labels', {}),
            processed_by=data.get('processed_by', []),
            processing_time=data.get('processing_time')
        )
    
    def add_processing_info(self, module_name: str, processing_time: float) -> None:
        """Ajoute des informations de traitement."""
        self.processed_by.append(module_name)
        if self.processing_time is None:
            self.processing_time = processing_time
        else:
            self.processing_time += processing_time
    
    def enrich(self, key: str, value: Any) -> None:
        """Enrichit l'événement avec des données supplémentaires."""
        self.enriched_data[key] = value
    
    def add_tag(self, tag: str) -> None:
        """Ajoute un tag à l'événement."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def add_label(self, key: str, value: str) -> None:
        """Ajoute un label à l'événement."""
        self.labels[key] = value
    
    def is_high_risk(self) -> bool:
        """Vérifie si l'événement est à haut risque."""
        return self.risk_level.value >= RiskLevel.HIGH.value
    
    def is_critical(self) -> bool:
        """Vérifie si l'événement est critique."""
        return self.risk_level == RiskLevel.CRITICAL or self.severity == Severity.CRITICAL
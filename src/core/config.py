"""
Configuration principale d'Orion
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class DatabaseConfig:
    """Configuration des bases de données."""
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_username: Optional[str] = None
    elasticsearch_password: Optional[str] = None
    elasticsearch_index_prefix: str = "orion"
    
    influxdb_url: str = "http://localhost:8086"
    influxdb_token: Optional[str] = None
    influxdb_org: str = "orion"
    influxdb_bucket: str = "security_metrics"
    
    redis_url: str = "redis://localhost:6379"
    redis_password: Optional[str] = None
    redis_db: int = 0


@dataclass
class HydraConfig:
    """Configuration du module Hydra (Déception)."""
    enabled: bool = True
    decoy_count: int = 50  # Nombre de leurres à créer
    decoy_refresh_interval: int = 3600  # Renouvellement en secondes
    
    # Types de leurres à créer
    create_user_decoys: bool = True
    create_computer_decoys: bool = True
    create_group_decoys: bool = True
    create_gpo_decoys: bool = False  # Plus risqué
    
    # Configuration de l'empoisonnement
    poison_injection_enabled: bool = True
    poison_injection_rate: float = 0.1  # 10% des interactions
    
    # Réalisme des leurres
    simulate_activity: bool = True
    activity_simulation_interval: int = 1800  # 30 minutes


@dataclass
class CassandraConfig:
    """Configuration du module Cassandra (IA)."""
    enabled: bool = True
    
    # Configuration ML
    model_path: str = "/opt/orion/models"
    retrain_interval: int = 86400  # 24 heures
    min_training_samples: int = 1000
    
    # Analyse comportementale
    baseline_learning_period: int = 604800  # 7 jours
    anomaly_threshold: float = 0.8
    risk_score_threshold: float = 0.7
    
    # Fenêtres d'analyse
    short_term_window: int = 300  # 5 minutes
    medium_term_window: int = 3600  # 1 heure
    long_term_window: int = 86400  # 24 heures
    
    # Features à analyser
    analyze_logon_patterns: bool = True
    analyze_access_patterns: bool = True
    analyze_network_patterns: bool = True
    analyze_privilege_usage: bool = True


@dataclass
class AegisConfig:
    """Configuration du module Aegis (Remédiation)."""
    enabled: bool = True
    
    # Actions automatiques
    auto_quarantine_enabled: bool = True
    auto_network_isolation_enabled: bool = True
    auto_rollback_enabled: bool = False  # Nécessite validation manuelle
    
    # Seuils d'action
    quarantine_risk_threshold: float = 0.9
    isolation_risk_threshold: float = 0.8
    rollback_risk_threshold: float = 0.95
    
    # Durées de quarantaine
    default_quarantine_duration: int = 3600  # 1 heure
    max_quarantine_duration: int = 86400  # 24 heures
    
    # Notifications
    notify_on_quarantine: bool = True
    notify_on_isolation: bool = True
    notify_on_rollback: bool = True
    
    # Intégrations
    siem_integration_enabled: bool = False
    email_notifications_enabled: bool = True
    slack_notifications_enabled: bool = False


@dataclass
class AgentConfig:
    """Configuration des agents de collecte."""
    # Agent AD
    ad_agent_enabled: bool = True
    ad_polling_interval: int = 30  # secondes
    ad_event_types: List[str] = field(default_factory=lambda: [
        "4624",  # Logon successful
        "4625",  # Logon failed
        "4634",  # Logoff
        "4648",  # Explicit credentials
        "4672",  # Special privileges assigned
        "4720",  # User account created
        "4722",  # User account enabled
        "4724",  # Password reset
        "4728",  # User added to group
        "4732",  # User added to local group
        "4756",  # User added to universal group
        "5136",  # Directory service object modified
        "5137",  # Directory service object created
        "5141",  # Directory service object deleted
    ])
    
    # Agent réseau
    network_agent_enabled: bool = True
    network_monitoring_interfaces: List[str] = field(default_factory=list)
    
    # Agent endpoint
    endpoint_agent_enabled: bool = True
    endpoint_monitoring_processes: bool = True
    endpoint_monitoring_files: bool = True
    endpoint_monitoring_registry: bool = True


@dataclass
class SecurityConfig:
    """Configuration de sécurité."""
    # Chiffrement
    encryption_enabled: bool = True
    encryption_algorithm: str = "AES-256-GCM"
    key_rotation_interval: int = 7776000  # 90 jours
    
    # Authentification
    jwt_secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_expiration_time: int = 3600  # 1 heure
    jwt_refresh_enabled: bool = True
    
    # TLS
    tls_enabled: bool = True
    tls_cert_path: str = "/opt/orion/certs/orion.crt"
    tls_key_path: str = "/opt/orion/certs/orion.key"
    tls_ca_path: str = "/opt/orion/certs/ca.crt"
    
    # Audit
    audit_enabled: bool = True
    audit_log_path: str = "/var/log/orion/audit.log"
    audit_retention_days: int = 365


@dataclass
class LoggingConfig:
    """Configuration du logging."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "/var/log/orion/orion.log"
    max_file_size: int = 100 * 1024 * 1024  # 100 MB
    backup_count: int = 5
    
    # Logging structuré
    structured_logging: bool = True
    json_format: bool = True
    
    # Logs de sécurité séparés
    security_log_path: str = "/var/log/orion/security.log"
    performance_log_path: str = "/var/log/orion/performance.log"


@dataclass
class MonitoringConfig:
    """Configuration du monitoring."""
    enabled: bool = True
    
    # Métriques
    prometheus_enabled: bool = True
    prometheus_port: int = 9090
    metrics_collection_interval: int = 60  # secondes
    
    # Health checks
    health_check_interval: int = 30  # secondes
    health_check_timeout: int = 10  # secondes
    
    # Alerting
    alerting_enabled: bool = True
    alert_webhook_url: Optional[str] = None
    alert_email_recipients: List[str] = field(default_factory=list)


@dataclass
class OrionConfig:
    """Configuration principale d'Orion."""
    # Informations générales
    environment: str = "development"  # development, staging, production
    debug: bool = False
    version: str = "0.1.0-alpha"
    
    # Configuration des modules
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    hydra: HydraConfig = field(default_factory=HydraConfig)
    cassandra: CassandraConfig = field(default_factory=CassandraConfig)
    aegis: AegisConfig = field(default_factory=AegisConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    
    # Active Directory
    ad_domain: str = "example.local"
    ad_domain_controllers: List[str] = field(default_factory=list)
    ad_service_account: Optional[str] = None
    ad_service_password: Optional[str] = None
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'OrionConfig':
        """Charge la configuration depuis un fichier YAML."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé : {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return cls.from_dict(config_data)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'OrionConfig':
        """Crée une configuration à partir d'un dictionnaire."""
        # Extraction des sous-configurations
        database_config = DatabaseConfig(**data.get('database', {}))
        hydra_config = HydraConfig(**data.get('hydra', {}))
        cassandra_config = CassandraConfig(**data.get('cassandra', {}))
        aegis_config = AegisConfig(**data.get('aegis', {}))
        agent_config = AgentConfig(**data.get('agent', {}))
        security_config = SecurityConfig(**data.get('security', {}))
        logging_config = LoggingConfig(**data.get('logging', {}))
        monitoring_config = MonitoringConfig(**data.get('monitoring', {}))
        
        return cls(
            environment=data.get('environment', 'development'),
            debug=data.get('debug', False),
            version=data.get('version', '0.1.0-alpha'),
            database=database_config,
            hydra=hydra_config,
            cassandra=cassandra_config,
            aegis=aegis_config,
            agent=agent_config,
            security=security_config,
            logging=logging_config,
            monitoring=monitoring_config,
            ad_domain=data.get('ad_domain', 'example.local'),
            ad_domain_controllers=data.get('ad_domain_controllers', []),
            ad_service_account=data.get('ad_service_account'),
            ad_service_password=data.get('ad_service_password')
        )
    
    @classmethod
    def load_from_env(cls) -> 'OrionConfig':
        """Charge la configuration depuis les variables d'environnement."""
        config_path = os.getenv('ORION_CONFIG_PATH', '/etc/orion/config.yaml')
        
        if os.path.exists(config_path):
            return cls.load_from_file(config_path)
        else:
            # Configuration par défaut avec surcharges d'environnement
            config = cls()
            
            # Surcharges depuis l'environnement
            config.environment = os.getenv('ORION_ENVIRONMENT', config.environment)
            config.debug = os.getenv('ORION_DEBUG', str(config.debug)).lower() == 'true'
            config.ad_domain = os.getenv('ORION_AD_DOMAIN', config.ad_domain)
            
            # Base de données
            config.database.elasticsearch_url = os.getenv('ORION_ELASTICSEARCH_URL', config.database.elasticsearch_url)
            config.database.influxdb_url = os.getenv('ORION_INFLUXDB_URL', config.database.influxdb_url)
            config.database.redis_url = os.getenv('ORION_REDIS_URL', config.database.redis_url)
            
            return config
    
    def to_dict(self) -> Dict:
        """Convertit la configuration en dictionnaire."""
        return {
            'environment': self.environment,
            'debug': self.debug,
            'version': self.version,
            'database': self.database.__dict__,
            'hydra': self.hydra.__dict__,
            'cassandra': self.cassandra.__dict__,
            'aegis': self.aegis.__dict__,
            'agent': self.agent.__dict__,
            'security': self.security.__dict__,
            'logging': self.logging.__dict__,
            'monitoring': self.monitoring.__dict__,
            'ad_domain': self.ad_domain,
            'ad_domain_controllers': self.ad_domain_controllers,
            'ad_service_account': self.ad_service_account,
            # Le mot de passe n'est pas exposé
        }
    
    def save_to_file(self, config_path: str) -> None:
        """Sauvegarde la configuration dans un fichier YAML."""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
    
    def validate(self) -> List[str]:
        """Valide la configuration et retourne les erreurs."""
        errors = []
        
        # Validation du domaine AD
        if not self.ad_domain:
            errors.append("Le domaine Active Directory doit être spécifié")
        
        if not self.ad_domain_controllers:
            errors.append("Au moins un contrôleur de domaine doit être spécifié")
        
        # Validation de sécurité
        if self.environment == 'production':
            if self.security.jwt_secret_key == "CHANGE_ME_IN_PRODUCTION":
                errors.append("La clé JWT doit être changée en production")
            
            if self.debug:
                errors.append("Le mode debug ne doit pas être activé en production")
        
        # Validation des seuils
        if self.cassandra.anomaly_threshold < 0 or self.cassandra.anomaly_threshold > 1:
            errors.append("Le seuil d'anomalie doit être entre 0 et 1")
        
        if self.aegis.quarantine_risk_threshold < 0 or self.aegis.quarantine_risk_threshold > 1:
            errors.append("Le seuil de quarantaine doit être entre 0 et 1")
        
        return errors
    
    def is_production(self) -> bool:
        """Vérifie si l'environnement est en production."""
        return self.environment.lower() == 'production'
    
    def is_development(self) -> bool:
        """Vérifie si l'environnement est en développement."""
        return self.environment.lower() == 'development'
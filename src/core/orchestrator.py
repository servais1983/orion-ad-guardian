"""
Orchestrator principal d'Orion

Coordonne tous les modules et gère le workflow de détection et de remédiation.
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from .events import SecurityEvent, EventType, RiskLevel
from .config import OrionConfig
from ..modules.hydra import HydraModule
from ..modules.cassandra import CassandraModule
from ..modules.aegis import AegisModule


@dataclass
class ModuleStatus:
    """Statut d'un module Orion."""
    name: str
    status: str  # 'running', 'stopped', 'error'
    last_heartbeat: datetime
    metrics: Dict[str, float]


class Orchestrator:
    """Orchestrateur principal coordonnant tous les modules Orion."""
    
    def __init__(self, config: OrionConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des modules
        self.hydra = HydraModule(config.hydra)
        self.cassandra = CassandraModule(config.cassandra)
        self.aegis = AegisModule(config.aegis)
        
        # État de l'orchestrateur
        self.is_running = False
        self.module_statuses: Dict[str, ModuleStatus] = {}
        self._start_time = datetime.now()
        
        # Queue des événements
        self.event_queue: asyncio.Queue[SecurityEvent] = asyncio.Queue()
        
        # Liste des alertes pour l'interface web
        self.alerts: List[Dict] = []
        
        self.logger.info("Orchestrateur Orion initialisé")
    
    async def start(self) -> None:
        """Démarre l'orchestrateur et tous les modules."""
        try:
            self.logger.info("Démarrage de l'orchestrateur Orion...")
            
            # Démarrage des modules
            await self.hydra.start()
            await self.cassandra.start()
            await self.aegis.start()
            
            # Démarrage des tâches de fond
            self.is_running = True
            await asyncio.gather(
                self._event_processor(),
                self._health_monitor(),
                self._metrics_collector()
            )
            
            self.logger.info("Orchestrateur Orion démarré avec succès")
            
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage : {e}")
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """Arrête l'orchestrateur et tous les modules."""
        self.logger.info("Arrêt de l'orchestrateur Orion...")
        
        self.is_running = False
        
        # Arrêt des modules
        await self.aegis.stop()
        await self.cassandra.stop()
        await self.hydra.stop()
        
        self.logger.info("Orchestrateur Orion arrêté")
    
    async def process_event(self, event: SecurityEvent) -> None:
        """Traite un événement de sécurité."""
        await self.event_queue.put(event)
    
    async def _event_processor(self) -> None:
        """Processeur principal des événements de sécurité."""
        self.logger.info("Démarrage du processeur d'événements")
        
        while self.is_running:
            try:
                # Récupération de l'événement avec timeout
                event = await asyncio.wait_for(
                    self.event_queue.get(), 
                    timeout=1.0
                )
                
                self.logger.debug(f"Traitement de l'événement : {event.event_id}")
                
                # Traitement parallèle par les modules
                await asyncio.gather(
                    self._process_with_hydra(event),
                    self._process_with_cassandra(event),
                    return_exceptions=True
                )
                
            except asyncio.TimeoutError:
                # Pas d'événement à traiter, on continue
                continue
            except Exception as e:
                self.logger.error(f"Erreur lors du traitement d'événement : {e}")
    
    def add_alert(self, alert_data: Dict) -> None:
        """Ajoute une alerte à la liste pour l'interface web."""
        alert_data['timestamp'] = datetime.now().isoformat()
        alert_data['id'] = f"alert_{len(self.alerts)}_{datetime.now().timestamp()}"
        self.alerts.append(alert_data)
        
        # Garder seulement les 100 dernières alertes
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    async def _process_with_hydra(self, event: SecurityEvent) -> None:
        """Traite un événement avec le module Hydra."""
        try:
            is_decoy = await self.hydra.is_decoy_interaction(event)
            if is_decoy:
                self.logger.critical(
                    f"ALERTE HYDRA : Interaction avec un leurre détectée ! Événement: {event.event_id}, Utilisateur: {event.user_context.username}"
                )
                
                # Créer une alerte pour l'interface web
                self.add_alert({
                    'event_id': event.event_id,
                    'source': 'Hydra',
                    'risk_level': 'CRITICAL',
                    'justification': f"Interaction détectée avec un leurre par l'utilisateur {event.user_context.username}",
                    'user': event.user_context.username,
                    'action_taken': 'quarantine_entity'
                })
                
                await self.aegis.handle_decoy_interaction(event)
        except Exception as e:
            self.logger.error(f"Erreur dans le module Hydra : {e}")
    
    async def _process_with_cassandra(self, event: SecurityEvent) -> None:
        """Traite un événement avec le module Cassandra."""
        try:
            # Analyse comportementale
            analysis_result = await self.cassandra.analyze_event(event)
            risk_score = analysis_result.risk_score if hasattr(analysis_result, 'risk_score') else analysis_result.get('risque', 1)
            justification = analysis_result.factors.get('justification') if hasattr(analysis_result, 'factors') else analysis_result.get('justification', '')

            # Si le risque est élevé ou critique, déclencher une action
            if risk_score >= 0.8:  # 0.8 = HIGH, 1.0 = CRITICAL
                risk_level = 'CRITICAL' if risk_score >= 0.9 else 'HIGH'
                self.logger.warning(
                    f"Risque élevé détecté : {risk_score} - {justification}"
                )
                
                # Créer une alerte pour l'interface web
                self.add_alert({
                    'event_id': event.event_id,
                    'source': 'Cassandra',
                    'risk_level': risk_level,
                    'justification': justification,
                    'user': event.user_context.username if event.user_context else 'Unknown',
                    'risk_score': risk_score,
                    'action_taken': 'handle_high_risk_event'
                })
                
                await self.aegis.handle_high_risk_event(event, {'justification': justification})
        except Exception as e:
            self.logger.error(f"Erreur module Cassandra : {e}")
    
    async def _health_monitor(self) -> None:
        """Surveille la santé des modules."""
        self.logger.info("Démarrage du moniteur de santé")
        
        while self.is_running:
            try:
                # Vérification de l'état des modules
                hydra_status = await self.hydra.get_health_status()
                cassandra_status = await self.cassandra.get_health_status()
                aegis_status = await self.aegis.get_health_status()
                
                self.module_statuses.update({
                    'hydra': hydra_status,
                    'cassandra': cassandra_status,
                    'aegis': aegis_status
                })
                
                # Logging des problèmes de santé
                for module_name, status in self.module_statuses.items():
                    if status.status != 'running':
                        self.logger.warning(
                            f"Module {module_name} en état : {status.status}"
                        )
                
                await asyncio.sleep(30)  # Vérification toutes les 30 secondes
                
            except Exception as e:
                self.logger.error(f"Erreur moniteur de santé : {e}")
                await asyncio.sleep(60)  # Attente plus longue en cas d'erreur
    
    async def _metrics_collector(self) -> None:
        """Collecte les métriques de performance."""
        self.logger.info("Démarrage du collecteur de métriques")
        
        while self.is_running:
            try:
                # Collecte des métriques de chaque module
                metrics = {
                    'hydra': await self.hydra.get_metrics(),
                    'cassandra': await self.cassandra.get_metrics(),
                    'aegis': await self.aegis.get_metrics(),
                    'orchestrator': {
                        'events_processed': self.event_queue.qsize(),
                        'uptime': (datetime.now() - self._start_time).total_seconds()
                    }
                }
                
                # Envoi des métriques au système de monitoring
                await self._send_metrics(metrics)
                
                await asyncio.sleep(60)  # Collecte toutes les minutes
                
            except Exception as e:
                self.logger.error(f"Erreur collecteur de métriques : {e}")
                await asyncio.sleep(120)
    
    async def _send_metrics(self, metrics: Dict) -> None:
        """Envoie les métriques au système de monitoring."""
        # TODO: Implémenter l'envoi vers InfluxDB ou Prometheus
        self.logger.debug(f"Métriques collectées : {metrics}")
    
    def get_status(self) -> Dict:
        """Retourne le statut actuel de l'orchestrateur."""
        return {
            'running': self.is_running,
            'modules': self.module_statuses,
            'event_queue_size': self.event_queue.qsize(),
            'uptime': (datetime.now() - getattr(self, '_start_time', datetime.now())).total_seconds()
        }
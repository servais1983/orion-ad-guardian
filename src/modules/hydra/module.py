"""
Module Hydra - Déception Dynamique (Version factice pour les tests)
"""

import logging
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass

from ...core.events import SecurityEvent


@dataclass
class HealthStatus:
    """Statut de santé du module."""
    name: str
    status: str
    last_heartbeat: datetime
    metrics: Dict[str, float]


class HydraModule:
    """Module de déception dynamique (version factice)."""
    
    def __init__(self, config: Any):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.is_running = False
    
    async def start(self) -> None:
        """Démarre le module Hydra."""
        self.logger.info("Module Hydra démarré (mode factice)")
        self.is_running = True
    
    async def stop(self) -> None:
        """Arrête le module Hydra."""
        self.logger.info("Module Hydra arrêté")
        self.is_running = False
    
    async def is_decoy_interaction(self, event: SecurityEvent) -> bool:
        """Vérifie si l'événement implique un leurre (MVP)."""
        # Détection simple : username contenant '_decoy_' ou se terminant par '_decoy_admin'
        if event.event_type.value == 'ad_logon' and event.user_context:
            username = event.user_context.username.lower()
            if '_decoy_' in username or username.endswith('_decoy_admin'):
                return True
        return False
    
    async def get_health_status(self) -> HealthStatus:
        """Retourne le statut de santé du module."""
        return HealthStatus(
            name="hydra",
            status="running" if self.is_running else "stopped",
            last_heartbeat=datetime.now(),
            metrics={"decoys_active": 0, "interactions_detected": 0}
        )
    
    async def get_metrics(self) -> Dict[str, float]:
        """Retourne les métriques du module."""
        return {
            "decoys_active": 0.0,
            "interactions_detected": 0.0,
            "poison_injections": 0.0
        } 
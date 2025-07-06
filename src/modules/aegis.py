"""
Module Aegis - Remédiation Automatique (Version factice pour les tests)
"""

import logging
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass

from ..core.events import SecurityEvent


@dataclass
class HealthStatus:
    """Statut de santé du module."""
    name: str
    status: str
    last_heartbeat: datetime
    metrics: Dict[str, float]


class AegisModule:
    """Module de remédiation automatique (version factice)."""
    
    def __init__(self, config: Any):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.is_running = False
    
    async def start(self) -> None:
        """Démarre le module Aegis."""
        self.logger.info("Module Aegis démarré (mode factice)")
        self.is_running = True
    
    async def stop(self) -> None:
        """Arrête le module Aegis."""
        self.logger.info("Module Aegis arrêté")
        self.is_running = False
    
    async def handle_decoy_interaction(self, event: SecurityEvent) -> None:
        """Gère une interaction avec un leurre."""
        self.logger.warning(f"Interaction avec leurre détectée : {event.event_id}")
        # En mode factice, on ne fait que logger
    
    async def handle_high_risk(self, event: SecurityEvent, risk_assessment: Any) -> None:
        """Gère un événement à haut risque."""
        self.logger.warning(f"Événement à haut risque détecté : {event.event_id}")
        # En mode factice, on ne fait que logger
    
    async def get_health_status(self) -> HealthStatus:
        """Retourne le statut de santé du module."""
        return HealthStatus(
            name="aegis",
            status="running" if self.is_running else "stopped",
            last_heartbeat=datetime.now(),
            metrics={"actions_taken": 0, "quarantines_active": 0}
        )
    
    async def get_metrics(self) -> Dict[str, float]:
        """Retourne les métriques du module."""
        return {
            "actions_taken": 0.0,
            "quarantines_active": 0.0,
            "avg_response_time": 0.0
        } 
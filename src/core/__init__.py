"""
Orion Core Engine

Moteur principal d'Orion coordonnant tous les modules de sécurité.
"""

__version__ = "0.1.0-alpha"
__author__ = "Orion Security Team"
__email__ = "team@orion-project.com"

from .orchestrator import Orchestrator
from .events import SecurityEvent, EventType, RiskLevel
from .config import OrionConfig

__all__ = [
    "Orchestrator",
    "SecurityEvent",
    "EventType",
    "RiskLevel",
    "OrionConfig",
]
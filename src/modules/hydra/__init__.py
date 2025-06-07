"""
Module Hydra - Déception Dynamique

Le module Hydra crée et maintient un écosystème de leurres au sein
de l'Active Directory pour détecter les activités malveillantes.
"""

from .module import HydraModule
from .decoy_manager import DecoyManager
from .interaction_detector import InteractionDetector
from .poison_injector import PoisonInjector

__all__ = [
    "HydraModule",
    "DecoyManager",
    "InteractionDetector",
    "PoisonInjector",
]
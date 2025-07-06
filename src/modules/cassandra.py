"""
Module Cassandra - Analyse Comportementale par IA Locale (Version avec Phi-3)
"""

import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass

from ..core.events import SecurityEvent, RiskLevel, EventType


@dataclass
class RiskAssessment:
    """Évaluation des risques d'un événement."""
    risk_score: float
    risk_level: RiskLevel
    confidence: float
    factors: Dict[str, float]


@dataclass
class HealthStatus:
    """Statut de santé du module."""
    name: str
    status: str
    last_heartbeat: datetime
    metrics: Dict[str, float]


class CassandraModule:
    """Module d'analyse comportementale par IA locale (version avec Phi-3)."""
    
    def __init__(self, config: Any):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.tokenizer = None
        self.pipe = None
        self.is_running = False
        
        # Le chargement du modèle est lourd, on le fait au démarrage
        self.load_model()
    
    def load_model(self):
        """Charge le modèle Phi-3 et le tokenizer."""
        self.logger.info("Tentative de chargement du modèle Phi-3...")
        model_id = "microsoft/Phi-3-mini-4k-instruct"
        
        try:
            # Pour l'instant, on désactive le chargement automatique
            # et on utilise un mode de fallback
            self.logger.info("Mode de développement : utilisation de l'analyse basique")
            self.pipe = None
            
            # TODO: Implémenter le chargement asynchrone du modèle
            # self.model = AutoModelForCausalLM.from_pretrained(...)
            
        except Exception as e:
            self.logger.warning(f"Impossible de charger le modèle Phi-3 : {e}")
            self.logger.info("Passage en mode analyse basique (sans IA)")
            self.pipe = None
    
    def create_prompt(self, event: SecurityEvent) -> str:
        """Crée un prompt détaillé pour que l'IA puisse l'analyser."""
        prompt = f"""<|system|>
Vous êtes un analyste expert en cybersécurité pour le système "Orion AD Guardian". Votre rôle est d'analyser les événements Active Directory pour détecter des menaces subtiles. Restez concis et factuel.

Analysez l'événement suivant et fournissez une réponse structurée :
- Risque: (1-Très Faible, 2-Faible, 3-Moyen, 4-Élevé, 5-Critique)
- Justification: (Une phrase expliquant votre raisonnement)
<|end|>
<|user|>
Événement à analyser :
- Type: {event.event_type.name}
- Utilisateur: {event.user_context.username}@{event.user_context.domain}
- Machine: {event.device_context.hostname} ({event.device_context.ip_address})
- Heure: {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- Données brutes: {event.raw_data}
<|end|>
<|assistant|>
"""
        return prompt
    
    async def start(self) -> None:
        """Démarre le module Cassandra."""
        self.logger.info("Module Cassandra démarré (mode IA locale)")
        self.is_running = True
    
    async def stop(self) -> None:
        """Arrête le module Cassandra."""
        self.logger.info("Module Cassandra arrêté")
        self.is_running = False
    
    async def analyze_event(self, event: SecurityEvent) -> RiskAssessment:
        """
        Analyse un événement en utilisant le modèle Phi-3 local ou une logique basique.
        """
        if not self.pipe:
            # Mode de fallback : analyse basique intelligente
            return self._analyze_event_basic(event)

        prompt = self.create_prompt(event)
        
        try:
            # Génération de la réponse par l'IA
            outputs = self.pipe(
                prompt,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.3,
                eos_token_id=self.tokenizer.eos_token_id,
            )
            
            ia_response = outputs[0]['generated_text'].split("<|assistant|>")[-1].strip()
            self.logger.info(f"Réponse de l'IA : {ia_response}")
            
            # On parse la réponse pour la rendre utilisable (simplifié)
            # Idéalement, on utiliserait des regex plus robustes ici.
            risk_score = 1
            justification = "Analyse IA non concluante."
            for line in ia_response.split('\n'):
                if "Risque:" in line:
                    try:
                        risk_score = int(line.split(':')[-1].strip().split('-')[0])
                    except (ValueError, IndexError):
                        risk_score = 1
                if "Justification:" in line:
                    justification = line.split(':')[-1].strip()
            
            # Conversion du score en RiskLevel
            if risk_score <= 1:
                risk_level = RiskLevel.VERY_LOW
            elif risk_score == 2:
                risk_level = RiskLevel.LOW
            elif risk_score == 3:
                risk_level = RiskLevel.MEDIUM
            elif risk_score == 4:
                risk_level = RiskLevel.HIGH
            else:
                risk_level = RiskLevel.CRITICAL
            
            if risk_score >= 3:
                self.logger.warning(
                    f"ALERTE CASSANDRA (IA): {justification} (Risque: {risk_score})"
                )
                
            return RiskAssessment(
                risk_score=risk_score / 5.0,  # Normalisation entre 0 et 1
                risk_level=risk_level,
                confidence=0.8,
                factors={"ai_analysis": risk_score / 5.0, "justification": justification}
            )
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse IA : {e}")
            return self._analyze_event_basic(event)
    
    def _analyze_event_basic(self, event: SecurityEvent) -> RiskAssessment:
        """Analyse basique intelligente en mode de fallback."""
        risk_score = 1.0  # Très faible par défaut
        risk_level = RiskLevel.VERY_LOW
        factors = {}
        justification = "Événement normal"
        
        # Analyse de l'utilisateur
        if event.user_context:
            username = event.user_context.username.lower()
            
            # Comptes sensibles
            if any(sensitive in username for sensitive in ['admin', 'root', 'service', 'system']):
                risk_score += 1.0
                factors['sensitive_account'] = 1.0
                justification = "Compte sensible utilisé"
            
            # Privilèges élevés
            if event.user_context.privileges:
                risk_score += 0.5
                factors['high_privileges'] = 0.5
                justification = "Privilèges élevés détectés"
        
        # Analyse de l'appareil
        if event.device_context:
            # Appareil non joint au domaine
            if not event.device_context.domain_joined:
                risk_score += 1.0
                factors['non_domain_joined'] = 1.0
                justification = "Appareil non joint au domaine"
            
            # IP externe
            ip = event.device_context.ip_address
            if ip.startswith(('10.', '192.168.', '172.')) == False:
                risk_score += 2.0
                factors['external_ip'] = 2.0
                justification = "Connexion depuis IP externe"
            
            # Appareil inconnu
            if 'unknown' in event.device_context.hostname.lower():
                risk_score += 0.5
                factors['unknown_device'] = 0.5
                justification = "Appareil inconnu"
        
        # Analyse temporelle
        hour = event.timestamp.hour
        if hour < 6 or hour > 22:  # Heures non ouvrables
            risk_score += 0.5
            factors['off_hours'] = 0.5
            justification = "Connexion en dehors des heures ouvrables"
        
        # Analyse spécifique des types d'événements
        if event.event_type == EventType.AD_GROUP_MODIFIED:
            # Modification de groupe - très sensible
            risk_score += 2.0
            factors['group_modification'] = 2.0
            justification = "Modification de groupe détectée"
            
            # Vérifier si c'est un groupe critique
            raw_data = event.raw_data or {}
            group_name = raw_data.get('Group', '').lower()
            if any(critical in group_name for critical in ['domain admins', 'enterprise admins', 'schema admins']):
                risk_score += 3.0
                factors['critical_group'] = 3.0
                justification = "Modification du groupe Domain Admins - CRITIQUE"
        
        elif event.event_type == EventType.AD_ACCOUNT_MODIFIED:
            # Modification de compte
            risk_score += 1.0
            factors['account_modification'] = 1.0
            justification = "Modification de compte détectée"
            
            # Vérifier si c'est une réactivation de compte
            raw_data = event.raw_data or {}
            event_type = raw_data.get('EventType', '').lower()
            if 'enabled' in event_type:
                risk_score += 1.0
                factors['account_enabled'] = 1.0
                justification = "Réactivation de compte détectée"
        
        elif event.event_type == EventType.AD_ACCOUNT_CREATED:
            # Création de compte
            risk_score += 0.5
            factors['account_creation'] = 0.5
            justification = "Création de compte détectée"
        
        # Normalisation et conversion
        risk_score = min(risk_score, 5.0)  # Max 5
        normalized_score = risk_score / 5.0
        
        if risk_score <= 1.5:
            risk_level = RiskLevel.VERY_LOW
        elif risk_score <= 2.5:
            risk_level = RiskLevel.LOW
        elif risk_score <= 3.5:
            risk_level = RiskLevel.MEDIUM
        elif risk_score <= 4.5:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
        
        if risk_score >= 3.0:
            self.logger.warning(
                f"ALERTE CASSANDRA (Basique): {justification} (Risque: {risk_score:.1f})"
            )
        
        return RiskAssessment(
            risk_score=normalized_score,
            risk_level=risk_level,
            confidence=0.7,
            factors=factors
        )
    
    async def get_health_status(self) -> HealthStatus:
        """Retourne le statut de santé du module."""
        return HealthStatus(
            name="cassandra",
            status="running" if self.is_running else "stopped",
            last_heartbeat=datetime.now(),
            metrics={
                "events_analyzed": 0,
                "anomalies_detected": 0,
                "model_loaded": 1.0 if self.pipe else 0.0
            }
        )
    
    async def get_metrics(self) -> Dict[str, float]:
        """Retourne les métriques du module."""
        return {
            "events_analyzed": 0.0,
            "anomalies_detected": 0.0,
            "avg_processing_time": 0.0,
            "model_loaded": 1.0 if self.pipe else 0.0
        } 
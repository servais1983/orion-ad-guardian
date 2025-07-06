import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
import json
import uuid
import csv
import io
from collections import defaultdict, Counter
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Gestion du cycle de vie de l'application ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage de l'application
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Initialiser les alertes et les alertes lues
    app.state.alerts = []
    app.state.read_alerts = set()  # Set des IDs d'alertes marquées comme lues
    
    yield  # L'API est maintenant prête à recevoir des requêtes

# --- Initialisation de l'API ---
app = FastAPI(
    title="Orion AD Guardian API",
    description="API de surveillance et sécurité Active Directory",
    version="2.0.0",
    lifespan=lifespan
)

# Configuration CORS pour la production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3180").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sécurité
security = HTTPBearer()
API_KEY = os.getenv("API_KEY", "orion-secret-key-2024")

# Modèles de données
class ADEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: float
    source_ip: str
    user: str
    details: Dict

class Alert(BaseModel):
    alert_id: str
    event_id: str
    severity: str
    title: str
    description: str
    timestamp: float
    source_ip: str
    user: str
    status: str = "new"
    read: bool = False
    remediated: bool = False
    remediation_actions: List[str] = []

class AlertAction(BaseModel):
    action: str
    timestamp: float
    user: str
    details: Dict

class Statistics(BaseModel):
    total_alerts: int
    alerts_by_severity: Dict[str, int]
    alerts_by_type: Dict[str, int]
    recent_activity: List[Dict]
    top_users: List[Dict]
    top_ips: List[Dict]

# Stockage en mémoire (remplacé par base de données en production)
events_db = []
alerts_db = []
actions_db = []

# Configuration de production
PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "false").lower() == "true"
MAX_ALERTS = int(os.getenv("MAX_ALERTS", "1000"))
ALERT_RETENTION_DAYS = int(os.getenv("ALERT_RETENTION_DAYS", "30"))

# Fonction d'authentification
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide"
        )
    return credentials.credentials

# Fonction de nettoyage automatique
def cleanup_old_data():
    """Nettoie les anciennes données selon la politique de rétention"""
    cutoff_time = time.time() - (ALERT_RETENTION_DAYS * 24 * 3600)
    
    # Nettoyer les alertes anciennes
    global alerts_db
    alerts_db = [alert for alert in alerts_db if alert["timestamp"] > cutoff_time]
    
    # Nettoyer les événements anciens
    global events_db
    events_db = [event for event in events_db if event["timestamp"] > cutoff_time]
    
    logger.info(f"Nettoyage effectué: {len(alerts_db)} alertes, {len(events_db)} événements conservés")

# Fonction de génération d'alertes améliorée
def generate_alert(event: ADEvent) -> Optional[Alert]:
    """Génère des alertes basées sur des règles de sécurité avancées"""
    
    # Règles de sécurité
    security_rules = {
        "AD_ACCOUNT_CREATED": {
            "severity": "medium",
            "title": "Création de compte détectée",
            "description": f"Nouveau compte créé pour l'utilisateur {event.user}"
        },
        "AD_GROUP_MODIFIED": {
            "severity": "high",
            "title": "Modification de groupe détectée",
            "description": f"Modification du groupe pour l'utilisateur {event.user}"
        },
        "AD_LOGON": {
            "severity": "low",
            "title": "Connexion utilisateur",
            "description": f"Connexion de l'utilisateur {event.user} depuis {event.source_ip}"
        }
    }
    
    # Vérifier les règles spéciales
    if event.event_type == "AD_LOGON":
        # Détecter les connexions suspectes
        if event.source_ip.startswith("192.168.1.") and event.user == "admin":
            return Alert(
                alert_id=f"alert_{len(alerts_db)}_{event.timestamp}",
                event_id=event.event_id,
                severity="critical",
                title="Connexion administrateur suspecte",
                description=f"Connexion admin depuis IP suspecte: {event.source_ip}",
                timestamp=event.timestamp,
                source_ip=event.source_ip,
                user=event.user,
                remediation_actions=["Désactivation du compte", "Notification immédiate", "Audit de sécurité"]
            )
    
    # Règle standard
    if event.event_type in security_rules:
        rule = security_rules[event.event_type]
        return Alert(
            alert_id=f"alert_{len(alerts_db)}_{event.timestamp}",
            event_id=event.event_id,
            severity=rule["severity"],
            title=rule["title"],
            description=rule["description"],
            timestamp=event.timestamp,
            source_ip=event.source_ip,
            user=event.user,
            remediation_actions=["Analyse de sécurité", "Vérification des permissions"]
        )
    
    return None

# Endpoints API
@app.get("/health")
async def health_check():
    """Vérification de l'état du service"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "production_mode": PRODUCTION_MODE,
        "alerts_count": len(alerts_db),
        "events_count": len(events_db)
    }

@app.post("/api/v1/events", status_code=202)
async def receive_event(event: ADEvent, token: str = Depends(verify_token)):
    """Réception d'un événement AD"""
    try:
        # Nettoyage automatique
        if len(alerts_db) > MAX_ALERTS:
            cleanup_old_data()
        
        # Stocker l'événement
        event_dict = event.dict()
        events_db.append(event_dict)
        
        # Générer une alerte
        alert = generate_alert(event)
        if alert:
            alert_dict = alert.dict()
            alerts_db.append(alert_dict)
            logger.info(f"Alerte générée: {alert.alert_id} - {alert.severity}")
        
        logger.info(f"Événement traité : {event.event_id} - {event.event_type}")
        
        return {"status": "accepted", "event_id": event.event_id}
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'événement: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/api/v1/alerts")
async def get_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    token: str = Depends(verify_token)
):
    """Récupération des alertes avec filtres"""
    try:
        filtered_alerts = alerts_db.copy()
        
        # Filtres
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a["severity"] == severity]
        if status:
            filtered_alerts = [a for a in filtered_alerts if a["status"] == status]
        
        # Tri par timestamp décroissant
        filtered_alerts.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Limitation
        filtered_alerts = filtered_alerts[:limit]
        
        return {"alerts": filtered_alerts, "total": len(filtered_alerts)}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des alertes: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.post("/api/v1/alerts/{alert_id}/mark-read")
async def mark_alert_read(alert_id: str, token: str = Depends(verify_token)):
    """Marquer une alerte comme lue"""
    try:
        for alert in alerts_db:
            if alert["alert_id"] == alert_id:
                alert["read"] = True
                alert["status"] = "read"
                
                # Enregistrer l'action
                action = AlertAction(
                    action="mark_read",
                    timestamp=time.time(),
                    user="system",
                    details={"alert_id": alert_id}
                )
                actions_db.append(action.dict())
                
                logger.info(f"Alerte {alert_id} marquée comme lue")
                return {"status": "success", "message": "Alerte marquée comme lue"}
        
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du marquage de l'alerte: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.post("/api/v1/alerts/{alert_id}/remediate")
async def remediate_alert(alert_id: str, token: str = Depends(verify_token)):
    """Déclencher la remédiation pour une alerte"""
    try:
        for alert in alerts_db:
            if alert["alert_id"] == alert_id:
                alert["remediated"] = True
                alert["status"] = "remediated"
                
                # Actions de remédiation simulées
                remediation_actions = [
                    "Désactivation du compte utilisateur",
                    "Déconnexion forcée des sessions",
                    "Notification à l'administrateur",
                    "Audit de sécurité déclenché",
                    "Mise en quarantaine du compte"
                ]
                
                # Enregistrer l'action
                action = AlertAction(
                    action="remediate",
                    timestamp=time.time(),
                    user="system",
                    details={
                        "alert_id": alert_id,
                        "actions": remediation_actions
                    }
                )
                actions_db.append(action.dict())
                
                logger.info(f"Remédiation déclenchée pour l'alerte {alert_id}: {remediation_actions}")
                return {
                    "status": "success",
                    "message": "Remédiation déclenchée",
                    "actions": remediation_actions
                }
        
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la remédiation: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/api/v1/statistics")
async def get_statistics(token: str = Depends(verify_token)):
    """Récupération des statistiques"""
    try:
        # Statistiques de base
        total_alerts = len(alerts_db)
        
        # Alertes par sévérité
        severity_counts = Counter(alert["severity"] for alert in alerts_db)
        
        # Alertes par type d'événement
        event_types = Counter()
        for alert in alerts_db:
            for event in events_db:
                if event["event_id"] == alert["event_id"]:
                    event_types[event["event_type"]] += 1
                    break
        
        # Activité récente (dernières 24h)
        cutoff_time = time.time() - 86400
        recent_alerts = [a for a in alerts_db if a["timestamp"] > cutoff_time]
        
        # Top utilisateurs
        user_counts = Counter(alert["user"] for alert in alerts_db)
        top_users = [{"user": user, "count": count} for user, count in user_counts.most_common(10)]
        
        # Top IPs
        ip_counts = Counter(alert["source_ip"] for alert in alerts_db)
        top_ips = [{"ip": ip, "count": count} for ip, count in ip_counts.most_common(10)]
        
        stats = Statistics(
            total_alerts=total_alerts,
            alerts_by_severity=dict(severity_counts),
            alerts_by_type=dict(event_types),
            recent_activity=recent_alerts,
            top_users=top_users,
            top_ips=top_ips
        )
        
        return stats.dict()
        
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/api/v1/export/alerts")
async def export_alerts(
    format: str = "json",
    severity: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Export des alertes"""
    try:
        filtered_alerts = alerts_db.copy()
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a["severity"] == severity]
        
        if format.lower() == "csv":
            # Export CSV
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=[
                "alert_id", "severity", "title", "description", "timestamp", 
                "source_ip", "user", "status", "read", "remediated"
            ])
            
            writer.writeheader()
            for alert in filtered_alerts:
                writer.writerow(alert)
            
            return {
                "content": output.getvalue(),
                "content_type": "text/csv",
                "filename": f"alerts_export_{int(time.time())}.csv"
            }
        
        else:
            # Export JSON
            return {
                "alerts": filtered_alerts,
                "export_timestamp": time.time(),
                "total_count": len(filtered_alerts)
            }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'export: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/api/v1/config")
async def get_config(token: str = Depends(verify_token)):
    """Récupération de la configuration"""
    return {
        "production_mode": PRODUCTION_MODE,
        "max_alerts": MAX_ALERTS,
        "alert_retention_days": ALERT_RETENTION_DAYS,
        "allowed_origins": os.getenv("ALLOWED_ORIGINS", "http://localhost:3180").split(","),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Configuration de production
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8006"))
    workers = int(os.getenv("WORKERS", "1"))
    
    logger.info(f"🚀 Démarrage d'Orion AD Guardian v2.0.0")
    logger.info(f"📡 Mode production: {PRODUCTION_MODE}")
    logger.info(f"🌐 Serveur: {host}:{port}")
    
    uvicorn.run(
        "main_simple:app",
        host=host,
        port=port,
        workers=workers if PRODUCTION_MODE else 1,
        log_level="info" if PRODUCTION_MODE else "debug"
    ) 
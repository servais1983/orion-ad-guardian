import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from src.core.config import OrionConfig
from src.core.orchestrator import Orchestrator
from src.core.events import SecurityEvent
from src.modules.hydra.module import HydraModule
from src.modules.cassandra import CassandraModule
from src.modules.aegis import AegisModule

# --- Gestion du cycle de vie de l'application ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage de l'application
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Charger la config et initialiser les composants
    config = OrionConfig.load_from_file('config/local.yaml')
    orchestrator = Orchestrator(config)
    
    # Injection des dépendances (modules)
    orchestrator.hydra = HydraModule(config.hydra)
    orchestrator.cassandra = CassandraModule(config.cassandra)
    orchestrator.aegis = AegisModule(config.aegis)
    
    app.state.orchestrator = orchestrator  # Rendre l'orchestrateur accessible
    
    # Démarrer l'orchestrateur en tâche de fond
    await orchestrator.start()
    
    yield  # L'API est maintenant prête à recevoir des requêtes
    
    # Arrêt de l'application
    await app.state.orchestrator.stop()

# --- Initialisation de l'API ---
app = FastAPI(
    title="Orion AD Guardian - API",
    version="0.1.0-alpha",
    lifespan=lifespan
)

# --- Définition de l'Endpoint ---
@app.post("/api/v1/events", status_code=status.HTTP_202_ACCEPTED)
async def submit_event(event_data: dict, request: Request):
    """
    Point d'entrée pour que les agents soumettent des événements de sécurité.
    """
    try:
        # Pydantic va valider et convertir le dict en notre modèle SecurityEvent
        security_event = SecurityEvent.from_dict(event_data)
        
        # On récupère l'orchestrateur depuis l'état de l'application
        orchestrator: Orchestrator = request.app.state.orchestrator
        
        # On place l'événement dans la file d'attente pour traitement asynchrone
        await orchestrator.process_event(security_event)
        
        return {"status": "event accepted", "event_id": security_event.event_id}
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de l'API et de l'orchestrateur."""
    return {"status": "ok"}

@app.get("/api/v1/alerts")
async def get_alerts(request: Request):
    """Récupère la liste des dernières alertes de sécurité."""
    try:
        orchestrator: Orchestrator = request.app.state.orchestrator
        # On retourne les 50 dernières alertes, les plus récentes en premier
        alerts = sorted(orchestrator.alerts, key=lambda x: x.get('timestamp', ''), reverse=True)[:50]
        return {"alerts": alerts, "count": len(alerts)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
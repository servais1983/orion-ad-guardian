import asyncio
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.config import OrionConfig
from src.core.orchestrator import Orchestrator
from src.core.events import SecurityEvent
import uvicorn

app = FastAPI(title="Orion AD Guardian API", version="0.1.0")

# Initialisation globale
config = OrionConfig.load_from_file('config/local.yaml')
orchestrator = Orchestrator(config)

# Démarrage de l'orchestrateur en tâche de fond
@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.create_task(orchestrator.start())

@app.on_event("shutdown")
async def shutdown_event():
    await orchestrator.stop()

@app.post("/api/v1/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(request: Request):
    """Endpoint d'ingestion d'événements de sécurité."""
    try:
        data = await request.json()
        event = SecurityEvent.from_dict(data)
        await orchestrator.process_event(event)
        return {"status": "accepted", "event_id": event.event_id}
    except Exception as e:
        logging.exception("Erreur lors de l'ingestion de l'événement :")
        return JSONResponse(status_code=400, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True) 
import asyncio
import logging
import httpx
import random
from datetime import datetime
from typing import Dict, Any

class SimpleADAgent:
    def __init__(self):
        self.orchestrator_url = "http://localhost:8006/api/v1/events"
        self.logger = logging.getLogger(__name__)
        self.is_running = False

    async def start(self):
        """Démarre la surveillance de l'agent."""
        self.logger.info("🚀 Démarrage de l'agent AD simplifié...")
        self.is_running = True
        
        # Simulation de la surveillance continue
        while self.is_running:
            await self.simulate_event_detection()
            await asyncio.sleep(10)  # Simule une détection toutes les 10 secondes

    async def stop(self):
        """Arrête l'agent."""
        self.logger.info("🛑 Arrêt de l'agent AD...")
        self.is_running = False

    async def simulate_event_detection(self):
        """Simule la détection d'un événement depuis le journal Windows."""
        self.logger.info("🔍 Simulation de la lecture d'un nouvel événement AD...")
        
        # Simulation d'événements variés
        event_types = [
            {
                "event_type": "AD_LOGON",
                "severity": "INFO",
                "risk_level": "LOW",
                "user_context": {"username": "john.doe", "domain": "CORP.LOCAL"},
                "device_context": {"hostname": "workstation-01", "ip_address": "192.168.1.100", "domain_joined": True},
                "raw_data": {"EventID": 4624, "AccountName": "john.doe", "ClientAddress": "192.168.1.100"},
                "source": "ad_agent",
                "tags": ["ad_logon", "successful"]
            },
            {
                "event_type": "AD_LOGON",
                "severity": "WARNING",
                "risk_level": "MEDIUM",
                "user_context": {"username": "attacker", "domain": "CORP.LOCAL"},
                "device_context": {"hostname": "unknown", "ip_address": "10.0.0.50", "domain_joined": False},
                "raw_data": {"EventID": 4625, "AccountName": "attacker", "ClientAddress": "10.0.0.50"},
                "source": "ad_agent",
                "tags": ["ad_logon", "failed", "suspicious"]
            },
            {
                "event_type": "AD_ACCOUNT_CREATED",
                "severity": "INFO",
                "risk_level": "MEDIUM",
                "user_context": {"username": "admin", "domain": "CORP.LOCAL"},
                "device_context": {"hostname": "DC-01", "ip_address": "10.0.0.1", "domain_joined": True},
                "raw_data": {"EventID": 4720, "AccountName": "admin", "TargetAccount": "newuser"},
                "source": "ad_agent",
                "tags": ["ad_account", "created"]
            },
            {
                "event_type": "AD_GROUP_MODIFIED",
                "severity": "CRITICAL",
                "risk_level": "HIGH",
                "user_context": {"username": "admin", "domain": "CORP.LOCAL"},
                "device_context": {"hostname": "DC-01", "ip_address": "10.0.0.1", "domain_joined": True},
                "raw_data": {"EventID": 4728, "AccountName": "admin", "TargetAccount": "user", "Group": "Domain Admins"},
                "source": "ad_agent",
                "tags": ["ad_group", "modified", "privilege_escalation"]
            }
        ]
        
        # Sélection aléatoire d'un événement
        event_data = random.choice(event_types)
        
        # Ajout d'un ID unique et timestamp
        event_data["event_id"] = f"evt_{datetime.now().timestamp()}_{random.randint(1000, 9999)}"
        event_data["timestamp"] = datetime.now().isoformat()
        
        # Envoi à l'orchestrateur
        await self.send_event_to_orchestrator(event_data)

    async def send_event_to_orchestrator(self, event_data: Dict[str, Any]):
        """Envoie l'événement formaté à l'API de l'orchestrateur."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.orchestrator_url, 
                    json=event_data,
                    timeout=10.0
                )
                
                if response.status_code == 202:  # 202 Accepted
                    self.logger.info(f"✅ Événement {event_data['event_id']} envoyé avec succès à l'orchestrateur.")
                else:
                    self.logger.error(f"❌ Erreur lors de l'envoi de l'événement: {response.status_code} {response.text}")
                    
        except httpx.ConnectError as e:
            self.logger.error(f"❌ Impossible de se connecter à l'orchestrateur : {e}")
        except httpx.TimeoutException as e:
            self.logger.error(f"⏰ Timeout lors de l'envoi à l'orchestrateur : {e}")
        except Exception as e:
            self.logger.error(f"❌ Erreur inattendue lors de l'envoi : {e}")


async def main():
    """Fonction principale pour tester l'agent."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Créer et démarrer l'agent
        agent = SimpleADAgent()
        
        print("🚀 Démarrage de l'agent AD simplifié...")
        print("📡 Envoi d'événements simulés vers l'orchestrateur...")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter")
        
        await agent.start()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'agent...")
        await agent.stop()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        logging.exception("Détails de l'erreur :")


if __name__ == "__main__":
    asyncio.run(main()) 
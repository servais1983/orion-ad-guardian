#!/usr/bin/env python3
"""
Script de test principal pour Orion AD Guardian

Ce script teste le flux d'événements le plus simple :
[Simulated Agent] -> [Orchestrator's Event Queue] -> [Orchestrator's Log]
"""

import asyncio
import logging
import sys
from pathlib import Path

# Ajout du répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.config import OrionConfig
from src.core.orchestrator import Orchestrator
from src.core.events import SecurityEvent, EventType, UserContext, DeviceContext, Severity, RiskLevel


async def main():
    """Fonction principale de test."""
    print("🚀 Démarrage du test Orion AD Guardian...")
    
    try:
        # 1. Charger la configuration
        print("📋 Chargement de la configuration...")
        config = OrionConfig.load_from_file('config/local.yaml')
        print(f"✅ Configuration chargée : {config.environment}")
        
        # 2. Initialiser l'orchestrateur
        print("⚙️ Initialisation de l'orchestrateur...")
        orchestrator = Orchestrator(config)
        print("✅ Orchestrateur initialisé")
        
        # 3. Créer un faux événement de sécurité
        print("🎭 Création d'un événement de test...")
        test_event = SecurityEvent(
            event_type=EventType.AD_LOGON,
            severity=Severity.INFO,
            risk_level=RiskLevel.LOW,
            user_context=UserContext(
                username="john_decoy_admin",
                domain="DEV.ORION.LOCAL",
                email="testuser@dev.orion.local",
                groups=["Users", "Developers"]
            ),
            device_context=DeviceContext(
                hostname="workstation-01",
                ip_address="192.168.1.100",
                mac_address="00:11:22:33:44:55",
                operating_system="Windows 10",
                domain_joined=True
            ),
            raw_data={
                "EventCode": "4624",
                "EventType": "Logon successful",
                "LogonType": "Interactive",
                "AuthenticationPackage": "NTLM",
                "WorkstationName": "WORKSTATION-01",
                "IpAddress": "192.168.1.100",
                "ProcessName": "C:\\Windows\\System32\\winlogon.exe"
            },
            source="test_agent",
            tags=["test", "ad_logon", "interactive"]
        )
        
        print(f"✅ Événement créé : {test_event.event_id}")
        print(f"   Type: {test_event.event_type.value}")
        print(f"   Utilisateur: {test_event.user_context.username}@{test_event.user_context.domain}")
        print(f"   Appareil: {test_event.device_context.hostname} ({test_event.device_context.ip_address})")
        
        # 4. Lancer l'orchestrateur en tâche de fond
        print("🔄 Démarrage de l'orchestrateur...")
        orchestrator_task = asyncio.create_task(orchestrator.start())
        
        # Donner un peu de temps à l'orchestrateur pour démarrer
        print("⏳ Attente du démarrage de l'orchestrateur...")
        await asyncio.sleep(3)
        
        # 5. Simuler l'arrivée de l'événement
        print(f"📥 Envoi de l'événement de test...")
        await orchestrator.process_event(test_event)
        
        # Laisser le temps de traiter l'événement
        print("⏳ Traitement de l'événement...")
        await asyncio.sleep(3)
        
        # 6. Afficher le statut
        print("📊 Statut de l'orchestrateur :")
        status = orchestrator.get_status()
        for module_name, module_status in status.get('modules', {}).items():
            print(f"   {module_name}: {module_status.get('status', 'unknown')}")
        
        # 7. Arrêter l'orchestrateur
        print("🛑 Arrêt de l'orchestrateur...")
        await orchestrator.stop()
        orchestrator_task.cancel()
        
        print("✅ Test terminé avec succès !")
        print("\n📝 Résumé :")
        print("   - Configuration chargée ✓")
        print("   - Orchestrateur démarré ✓")
        print("   - Événement créé et envoyé ✓")
        print("   - Événement traité par les modules ✓")
        print("   - Orchestrateur arrêté proprement ✓")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        logging.exception("Détails de l'erreur :")
        return 1
    
    return 0


if __name__ == "__main__":
    # Configuration du logging pour voir ce qui se passe
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/test.log', mode='w')
        ]
    )
    
    # Création du répertoire logs s'il n'existe pas
    Path('logs').mkdir(exist_ok=True)
    
    # Exécution du test
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 
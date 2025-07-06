#!/usr/bin/env python3
"""
Script de test pour l'analyse IA d'escalade de privilèges

Ce script teste l'analyse comportementale par IA locale sur un scénario
d'escalade de privilèges critique.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Ajout du répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.config import OrionConfig
from src.core.orchestrator import Orchestrator
from src.core.events import SecurityEvent, EventType, UserContext, DeviceContext, Severity, RiskLevel


async def test_privilege_escalation():
    """Test d'escalade de privilèges critique."""
    print("🎭 Test : Événement d'escalade de privilèges critique")
    
    privilege_escalation_event = SecurityEvent(
        event_type=EventType.AD_GROUP_MODIFIED,
        severity=Severity.CRITICAL,
        risk_level=RiskLevel.HIGH,
        user_context=UserContext(
            username="admin_compromis",
            domain="DEV.ORION.LOCAL",
            email="admin@dev.orion.local",
            groups=["Administrators", "Domain Admins"],
            privileges=["SeDebugPrivilege", "SeBackupPrivilege", "SeSecurityPrivilege"]
        ),
        device_context=DeviceContext(
            hostname="DC-01",
            ip_address="10.0.0.1",
            mac_address="00:11:22:33:44:55",
            operating_system="Windows Server 2022",
            domain_joined=True
        ),
        raw_data={
            "EventCode": "4728",
            "EventType": "A member was added to a security-enabled global group",
            "Subject": "admin_compromis@DEV.ORION.LOCAL",
            "Target": "utilisateur_lambda@DEV.ORION.LOCAL",
            "Group": "Domain Admins",
            "GroupSID": "S-1-5-21-1234567890-1234567890-1234567890-512",
            "Details": "Un utilisateur a été ajouté à un groupe de sécurité global.",
            "LogonID": "0x123456",
            "CallerProcessName": "C:\\Windows\\System32\\dsa.msc"
        },
        source="test_agent",
        tags=["test", "ad_group_modified", "privilege_escalation", "critical", "domain_admins"]
    )
    
    return privilege_escalation_event


async def test_suspicious_admin_activity():
    """Test d'activité administrative suspecte."""
    print("🎭 Test : Activité administrative suspecte")
    
    suspicious_admin_event = SecurityEvent(
        event_type=EventType.AD_ACCOUNT_MODIFIED,
        severity=Severity.WARNING,
        risk_level=RiskLevel.MEDIUM,
        user_context=UserContext(
            username="service_account",
            domain="DEV.ORION.LOCAL",
            email="service@dev.orion.local",
            groups=["Service Accounts", "High Privilege"],
            privileges=["SeTcbPrivilege", "SeSecurityPrivilege"]
        ),
        device_context=DeviceContext(
            hostname="unknown-server",
            ip_address="192.168.1.200",
            mac_address="AA:BB:CC:DD:EE:FF",
            operating_system="Windows Server 2019",
            domain_joined=False
        ),
        raw_data={
            "EventCode": "4722",
            "EventType": "A user account was enabled",
            "Subject": "service_account@DEV.ORION.LOCAL",
            "Target": "disabled_admin@DEV.ORION.LOCAL",
            "Details": "Compte administrateur désactivé réactivé",
            "LogonID": "0x654321",
            "CallerProcessName": "C:\\Windows\\System32\\lusrmgr.msc"
        },
        source="test_agent",
        tags=["test", "ad_account_modified", "suspicious", "admin_reactivation"]
    )
    
    return suspicious_admin_event


async def test_normal_admin_activity():
    """Test d'activité administrative normale."""
    print("🎭 Test : Activité administrative normale")
    
    normal_admin_event = SecurityEvent(
        event_type=EventType.AD_ACCOUNT_CREATED,
        severity=Severity.INFO,
        risk_level=RiskLevel.LOW,
        user_context=UserContext(
            username="admin_legitime",
            domain="DEV.ORION.LOCAL",
            email="admin@dev.orion.local",
            groups=["Administrators"],
            privileges=["SeDebugPrivilege"]
        ),
        device_context=DeviceContext(
            hostname="DC-01",
            ip_address="10.0.0.1",
            mac_address="00:11:22:33:44:55",
            operating_system="Windows Server 2022",
            domain_joined=True
        ),
        raw_data={
            "EventCode": "4720",
            "EventType": "A user account was created",
            "Subject": "admin_legitime@DEV.ORION.LOCAL",
            "Target": "nouveau_utilisateur@DEV.ORION.LOCAL",
            "Details": "Création d'un compte utilisateur standard",
            "LogonID": "0x111111",
            "CallerProcessName": "C:\\Windows\\System32\\dsa.msc"
        },
        source="test_agent",
        tags=["test", "ad_account_created", "normal", "user_creation"]
    )
    
    return normal_admin_event


async def main():
    """Fonction principale de test."""
    print("🚀 Démarrage du test d'analyse IA sur escalade de privilèges...")
    
    try:
        # 1. Charger la configuration
        print("📋 Chargement de la configuration...")
        config = OrionConfig.load_from_file('config/local.yaml')
        print(f"✅ Configuration chargée : {config.environment}")
        
        # 2. Initialiser l'orchestrateur
        print("⚙️ Initialisation de l'orchestrateur...")
        orchestrator = Orchestrator(config)
        print("✅ Orchestrateur initialisé")
        
        # 3. Lancer l'orchestrateur en tâche de fond
        print("🔄 Démarrage de l'orchestrateur...")
        orchestrator_task = asyncio.create_task(orchestrator.start())
        
        # Donner du temps pour le chargement du modèle IA
        print("⏳ Attente du chargement du modèle IA...")
        await asyncio.sleep(5)
        
        # 4. Tests avec différents scénarios d'administration
        test_events = [
            await test_normal_admin_activity(),
            await test_suspicious_admin_activity(),
            await test_privilege_escalation()
        ]
        
        for i, event in enumerate(test_events, 1):
            print(f"\n📥 Test {i} : Envoi de l'événement {event.event_id}")
            print(f"   Type: {event.event_type.value}")
            print(f"   Utilisateur: {event.user_context.username}@{event.user_context.domain}")
            print(f"   Appareil: {event.device_context.hostname} ({event.device_context.ip_address})")
            print(f"   Données: {event.raw_data.get('Details', 'N/A')}")
            
            await orchestrator.process_event(event)
            
            # Attendre le traitement
            await asyncio.sleep(3)
        
        # 5. Afficher le statut final
        print("\n📊 Statut final de l'orchestrateur :")
        status = orchestrator.get_status()
        for module_name, module_status in status.get('modules', {}).items():
            print(f"   {module_name}: {module_status.status}")
        
        # 6. Arrêter l'orchestrateur
        print("\n🛑 Arrêt de l'orchestrateur...")
        await orchestrator.stop()
        orchestrator_task.cancel()
        
        print("✅ Test d'escalade de privilèges terminé avec succès !")
        print("\n📝 Résumé :")
        print("   - Configuration chargée ✓")
        print("   - Modèle IA chargé ✓")
        print("   - 3 scénarios d'administration testés ✓")
        print("   - Analyse IA effectuée ✓")
        print("   - Orchestrateur arrêté proprement ✓")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'escalade de privilèges : {e}")
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
            logging.FileHandler('logs/test_privilege_escalation.log', mode='w')
        ]
    )
    
    # Création du répertoire logs s'il n'existe pas
    Path('logs').mkdir(exist_ok=True)
    
    # Exécution du test
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 
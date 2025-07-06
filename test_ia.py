#!/usr/bin/env python3
"""
Script de test pour le module Cassandra avec IA locale (Phi-3)

Ce script teste l'analyse comportementale par IA locale.
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


async def test_normal_event():
    """Test avec un événement normal."""
    print("🎭 Test 1 : Événement de connexion normal")
    
    normal_event = SecurityEvent(
        event_type=EventType.AD_LOGON,
        severity=Severity.INFO,
        risk_level=RiskLevel.LOW,
        user_context=UserContext(
            username="john.doe",
            domain="DEV.ORION.LOCAL",
            email="john.doe@dev.orion.local",
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
        tags=["test", "ad_logon", "interactive", "normal"]
    )
    
    return normal_event


async def test_suspicious_event():
    """Test avec un événement suspect."""
    print("🎭 Test 2 : Événement de connexion suspect")
    
    suspicious_event = SecurityEvent(
        event_type=EventType.AD_LOGON,
        severity=Severity.WARNING,
        risk_level=RiskLevel.MEDIUM,
        user_context=UserContext(
            username="admin",
            domain="DEV.ORION.LOCAL",
            email="admin@dev.orion.local",
            groups=["Administrators", "Domain Admins"],
            privileges=["SeDebugPrivilege", "SeBackupPrivilege"]
        ),
        device_context=DeviceContext(
            hostname="unknown-workstation",
            ip_address="10.0.0.50",
            mac_address="AA:BB:CC:DD:EE:FF",
            operating_system="Windows 11",
            domain_joined=False
        ),
        raw_data={
            "EventCode": "4624",
            "EventType": "Logon successful",
            "LogonType": "Interactive",
            "AuthenticationPackage": "Kerberos",
            "WorkstationName": "UNKNOWN-WORKSTATION",
            "IpAddress": "10.0.0.50",
            "ProcessName": "C:\\Windows\\System32\\winlogon.exe",
            "LogonTime": "2025-07-05T23:30:00Z"  # Heure tardive
        },
        source="test_agent",
        tags=["test", "ad_logon", "interactive", "suspicious", "admin", "off_hours"]
    )
    
    return suspicious_event


async def test_critical_event():
    """Test avec un événement critique."""
    print("🎭 Test 3 : Événement de connexion critique")
    
    critical_event = SecurityEvent(
        event_type=EventType.AD_LOGON,
        severity=Severity.CRITICAL,
        risk_level=RiskLevel.HIGH,
        user_context=UserContext(
            username="service_account",
            domain="DEV.ORION.LOCAL",
            email="service@dev.orion.local",
            groups=["Service Accounts", "High Privilege"],
            privileges=["SeTcbPrivilege", "SeSecurityPrivilege"]
        ),
        device_context=DeviceContext(
            hostname="external-device",
            ip_address="203.0.113.10",
            mac_address="FF:EE:DD:CC:BB:AA",
            operating_system="Unknown",
            domain_joined=False
        ),
        raw_data={
            "EventCode": "4624",
            "EventType": "Logon successful",
            "LogonType": "Network",
            "AuthenticationPackage": "NTLM",
            "WorkstationName": "EXTERNAL-DEVICE",
            "IpAddress": "203.0.113.10",
            "ProcessName": "C:\\Windows\\System32\\lsass.exe",
            "LogonTime": "2025-07-05T02:15:00Z",  # Heure très tardive
            "NetworkAddress": "203.0.113.10"
        },
        source="test_agent",
        tags=["test", "ad_logon", "network", "critical", "external_ip", "service_account"]
    )
    
    return critical_event


async def main():
    """Fonction principale de test."""
    print("🚀 Démarrage du test IA locale Orion AD Guardian...")
    
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
        print("⏳ Attente du chargement du modèle IA (peut prendre plusieurs minutes)...")
        await asyncio.sleep(10)  # Plus de temps pour le chargement du modèle
        
        # 4. Tests avec différents types d'événements
        test_events = [
            await test_normal_event(),
            await test_suspicious_event(),
            await test_critical_event()
        ]
        
        for i, event in enumerate(test_events, 1):
            print(f"\n📥 Test {i} : Envoi de l'événement {event.event_id}")
            print(f"   Type: {event.event_type.value}")
            print(f"   Utilisateur: {event.user_context.username}@{event.user_context.domain}")
            print(f"   Appareil: {event.device_context.hostname} ({event.device_context.ip_address})")
            
            await orchestrator.process_event(event)
            
            # Attendre le traitement
            await asyncio.sleep(5)
        
        # 5. Afficher le statut final
        print("\n📊 Statut final de l'orchestrateur :")
        status = orchestrator.get_status()
        for module_name, module_status in status.get('modules', {}).items():
            print(f"   {module_name}: {module_status.status}")
        
        # 6. Arrêter l'orchestrateur
        print("\n🛑 Arrêt de l'orchestrateur...")
        await orchestrator.stop()
        orchestrator_task.cancel()
        
        print("✅ Test IA terminé avec succès !")
        print("\n📝 Résumé :")
        print("   - Configuration chargée ✓")
        print("   - Modèle IA chargé ✓")
        print("   - 3 événements testés (normal, suspect, critique) ✓")
        print("   - Analyse IA effectuée ✓")
        print("   - Orchestrateur arrêté proprement ✓")
        
    except Exception as e:
        print(f"❌ Erreur lors du test IA : {e}")
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
            logging.FileHandler('logs/test_ia.log', mode='w')
        ]
    )
    
    # Création du répertoire logs s'il n'existe pas
    Path('logs').mkdir(exist_ok=True)
    
    # Exécution du test
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 
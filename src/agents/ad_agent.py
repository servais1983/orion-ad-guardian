import asyncio
import logging
import httpx
import win32evtlog
import win32evtlogutil
import win32con
import win32security
import win32api
import win32process
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from src.core.config import OrionConfig
from src.core.events import SecurityEvent, EventType, UserContext, DeviceContext, Severity, RiskLevel

class ActiveDirectoryAgent:
    def __init__(self, config: OrionConfig):
        self.config = config
        self.orchestrator_url = "http://localhost:8000/api/v1/events"
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.last_event_time = None
        self.event_handles = {}
        
        # Vérifier les privilèges administrateur
        self._check_admin_privileges()
        
        # Initialiser les handles pour les différents logs
        self._initialize_event_logs()

    def _check_admin_privileges(self):
        """Vérifie si l'agent a les privilèges administrateur nécessaires."""
        try:
            # Vérifier si nous avons les privilèges SeSecurityPrivilege
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32con.TOKEN_QUERY
            )
            
            privileges = win32security.GetTokenInformation(
                token,
                win32security.TokenPrivileges
            )
            
            has_security_privilege = any(
                priv[0] == win32security.LookupPrivilegeValue(
                    None, 
                    win32security.SE_SECURITY_NAME
                ) for priv in privileges
            )
            
            if not has_security_privilege:
                self.logger.warning("⚠️  Privilèges administrateur limités. Certains événements peuvent ne pas être accessibles.")
            else:
                self.logger.info("✅ Privilèges administrateur confirmés.")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la vérification des privilèges : {e}")
            raise

    def _initialize_event_logs(self):
        """Initialise les handles pour les différents journaux d'événements."""
        try:
            # Journal de sécurité (événements AD)
            self.event_handles['security'] = win32evtlog.OpenEventLog(
                None, 
                "Security"
            )
            
            # Journal système (pour les événements système)
            self.event_handles['system'] = win32evtlog.OpenEventLog(
                None, 
                "System"
            )
            
            # Journal application (pour les événements d'application)
            self.event_handles['application'] = win32evtlog.OpenEventLog(
                None, 
                "Application"
            )
            
            self.logger.info("✅ Handles des journaux d'événements initialisés.")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'initialisation des journaux : {e}")
            raise

    async def start(self):
        """Démarre la surveillance de l'agent."""
        self.logger.info("🚀 Démarrage de l'agent Active Directory...")
        self.is_running = True
        
        # Surveillance continue des événements
        while self.is_running:
            await self.monitor_events()
            await asyncio.sleep(5)  # Vérification toutes les 5 secondes

    async def stop(self):
        """Arrête l'agent."""
        self.logger.info("🛑 Arrêt de l'agent Active Directory...")
        self.is_running = False
        
        # Fermer les handles
        for handle in self.event_handles.values():
            try:
                win32evtlog.CloseEventLog(handle)
            except:
                pass

    async def monitor_events(self):
        """Surveille les nouveaux événements dans les journaux Windows."""
        try:
            # Surveiller principalement le journal de sécurité
            new_events = self._read_new_security_events()
            
            for raw_event in new_events:
                # Transformer l'événement brut en SecurityEvent Orion
                orion_event = self._parse_windows_event(raw_event)
                
                if orion_event:
                    self.logger.info(f"🔍 Nouvel événement détecté : {orion_event.event_type} - {orion_event.severity}")
                    await self.send_event_to_orchestrator(orion_event)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la surveillance des événements : {e}")

    def _read_new_security_events(self) -> List[Dict[str, Any]]:
        """Lit les nouveaux événements du journal de sécurité."""
        events = []
        
        try:
            handle = self.event_handles['security']
            
            # Lire les événements depuis le dernier événement lu
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            # Si c'est la première lecture, commencer par les événements récents
            if self.last_event_time is None:
                flags |= win32evtlog.EVENTLOG_FORWARDS_READ
                self.last_event_time = datetime.now() - timedelta(minutes=5)  # Dernières 5 minutes
            
            # Lire les événements
            while True:
                try:
                    events_raw = win32evtlog.ReadEventLog(handle, flags, 0)
                    
                    if not events_raw:
                        break
                    
                    for event in events_raw:
                        event_data = self._extract_event_data(event)
                        
                        if event_data and self._is_relevant_event(event_data):
                            events.append(event_data)
                            
                except Exception as e:
                    if "No more data" in str(e):
                        break
                    else:
                        self.logger.error(f"Erreur lors de la lecture d'événement : {e}")
                        break
                        
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la lecture du journal de sécurité : {e}")
            
        return events

    def _extract_event_data(self, event) -> Optional[Dict[str, Any]]:
        """Extrait les données d'un événement Windows brut."""
        try:
            # Extraire les informations de base
            event_data = {
                'EventID': event.EventID,
                'TimeGenerated': event.TimeGenerated,
                'SourceName': event.SourceName,
                'ComputerName': event.ComputerName,
                'EventType': event.EventType,
                'EventCategory': event.EventCategory,
                'StringInserts': event.StringInserts,
                'Sid': event.Sid
            }
            
            # Extraire les données spécifiques selon l'EventID
            if event.EventID in [4624, 4625, 4626, 4627, 4634, 4647, 4648, 4657, 4672, 4673, 4674, 4675, 4688, 4697, 4698, 4699, 4700, 4701, 4702, 4719, 4720, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4737, 4738, 4739, 4740, 4754, 4755, 4756, 4757, 4758, 4759, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4792, 4793, 4794, 4795, 4796, 4797, 4798, 4799, 4800, 4801, 4802, 4803, 4804, 4805, 4806, 4807, 4808, 4809, 4810, 4811, 4812, 4813, 4814, 4815, 4816, 4817, 4818, 4819, 4820, 4821, 4822, 4823, 4824, 4825, 4826, 4827, 4828, 4829, 4830, 4831, 4832, 4833, 4834, 4835, 4836, 4837, 4838, 4839, 4840, 4841, 4842, 4843, 4844, 4845, 4846, 4847, 4848, 4849, 4850, 4851, 4852, 4853, 4854, 4855, 4856, 4857, 4858, 4859, 4860, 4861, 4862, 4863, 4864, 4865, 4866, 4867, 4868, 4869, 4870, 4871, 4872, 4873, 4874, 4875, 4876, 4877, 4878, 4879, 4880, 4881, 4882, 4883, 4884, 4885, 4886, 4887, 4888, 4889, 4890, 4891, 4892, 4893, 4894, 4895, 4896, 4897, 4898, 4899, 4900, 4901, 4902, 4903, 4904, 4905, 4906, 4907, 4908, 4909, 4910, 4911, 4912, 4913, 4914, 4915, 4916, 4917, 4918, 4919, 4920, 4921, 4922, 4923, 4924, 4925, 4926, 4927, 4928, 4929, 4930, 4931, 4932, 4933, 4934, 4935, 4936, 4937, 4938, 4939, 4940, 4941, 4942, 4943, 4944, 4945, 4946, 4947, 4948, 4949, 4950, 4951, 4952, 4953, 4954, 4955, 4956, 4957, 4958, 4959, 4960, 4961, 4962, 4963, 4964, 4965, 4966, 4967, 4968, 4969, 4970, 4971, 4972, 4973, 4974, 4975, 4976, 4977, 4978, 4979, 4980, 4981, 4982, 4983, 4984, 4985, 4986, 4987, 4988, 4989, 4990, 4991, 4992, 4993, 4994, 4995, 4996, 4997, 4998, 4999, 5000]:
                # Événements de sécurité critiques
                event_data.update(self._parse_security_event(event))
            
            return event_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction des données d'événement : {e}")
            return None

    def _parse_security_event(self, event) -> Dict[str, Any]:
        """Parse un événement de sécurité spécifique."""
        parsed_data = {}
        
        try:
            # Extraire les informations selon l'EventID
            if event.EventID == 4624:  # Logon successful
                if len(event.StringInserts) >= 5:
                    parsed_data.update({
                        'AccountName': event.StringInserts[5] if len(event.StringInserts) > 5 else 'Unknown',
                        'ClientAddress': event.StringInserts[18] if len(event.StringInserts) > 18 else 'Unknown',
                        'LogonType': event.StringInserts[8] if len(event.StringInserts) > 8 else 'Unknown',
                        'ProcessName': event.StringInserts[17] if len(event.StringInserts) > 17 else 'Unknown'
                    })
                    
            elif event.EventID == 4625:  # Logon failed
                if len(event.StringInserts) >= 5:
                    parsed_data.update({
                        'AccountName': event.StringInserts[5] if len(event.StringInserts) > 5 else 'Unknown',
                        'ClientAddress': event.StringInserts[18] if len(event.StringInserts) > 18 else 'Unknown',
                        'FailureReason': event.StringInserts[8] if len(event.StringInserts) > 8 else 'Unknown'
                    })
                    
            elif event.EventID == 4720:  # Account created
                if len(event.StringInserts) >= 2:
                    parsed_data.update({
                        'AccountName': event.StringInserts[0] if len(event.StringInserts) > 0 else 'Unknown',
                        'TargetAccount': event.StringInserts[2] if len(event.StringInserts) > 2 else 'Unknown'
                    })
                    
            elif event.EventID == 4728:  # Member added to group
                if len(event.StringInserts) >= 3:
                    parsed_data.update({
                        'AccountName': event.StringInserts[0] if len(event.StringInserts) > 0 else 'Unknown',
                        'TargetAccount': event.StringInserts[2] if len(event.StringInserts) > 2 else 'Unknown',
                        'Group': event.StringInserts[3] if len(event.StringInserts) > 3 else 'Unknown'
                    })
                    
        except Exception as e:
            self.logger.error(f"Erreur lors du parsing de l'événement {event.EventID} : {e}")
            
        return parsed_data

    def _is_relevant_event(self, event_data: Dict[str, Any]) -> bool:
        """Détermine si un événement est pertinent pour la sécurité."""
        relevant_event_ids = [
            4624, 4625, 4626, 4627, 4634, 4647, 4648, 4657, 4672, 4673, 4674, 4675, 4688, 4697, 4698, 4699, 4700, 4701, 4702, 4719, 4720, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4737, 4738, 4739, 4740, 4754, 4755, 4756, 4757, 4758, 4759, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4792, 4793, 4794, 4795, 4796, 4797, 4798, 4799, 4800, 4801, 4802, 4803, 4804, 4805, 4806, 4807, 4808, 4809, 4810, 4811, 4812, 4813, 4814, 4815, 4816, 4817, 4818, 4819, 4820, 4821, 4822, 4823, 4824, 4825, 4826, 4827, 4828, 4829, 4830, 4831, 4832, 4833, 4834, 4835, 4836, 4837, 4838, 4839, 4840, 4841, 4842, 4843, 4844, 4845, 4846, 4847, 4848, 4849, 4850, 4851, 4852, 4853, 4854, 4855, 4856, 4857, 4858, 4859, 4860, 4861, 4862, 4863, 4864, 4865, 4866, 4867, 4868, 4869, 4870, 4871, 4872, 4873, 4874, 4875, 4876, 4877, 4878, 4879, 4880, 4881, 4882, 4883, 4884, 4885, 4886, 4887, 4888, 4889, 4890, 4891, 4892, 4893, 4894, 4895, 4896, 4897, 4898, 4899, 4900, 4901, 4902, 4903, 4904, 4905, 4906, 4907, 4908, 4909, 4910, 4911, 4912, 4913, 4914, 4915, 4916, 4917, 4918, 4919, 4920, 4921, 4922, 4923, 4924, 4925, 4926, 4927, 4928, 4929, 4930, 4931, 4932, 4933, 4934, 4935, 4936, 4937, 4938, 4939, 4940, 4941, 4942, 4943, 4944, 4945, 4946, 4947, 4948, 4949, 4950, 4951, 4952, 4953, 4954, 4955, 4956, 4957, 4958, 4959, 4960, 4961, 4962, 4963, 4964, 4965, 4966, 4967, 4968, 4969, 4970, 4971, 4972, 4973, 4974, 4975, 4976, 4977, 4978, 4979, 4980, 4981, 4982, 4983, 4984, 4985, 4986, 4987, 4988, 4989, 4990, 4991, 4992, 4993, 4994, 4995, 4996, 4997, 4998, 4999, 5000
        ]
        
        return event_data.get('EventID') in relevant_event_ids

    def _parse_windows_event(self, raw_event: Dict[str, Any]) -> Optional[SecurityEvent]:
        """Traduit un événement brut Windows en un SecurityEvent Orion."""
        event_id = raw_event.get('EventID')
        
        if event_id == 4624:  # Logon successful
            return SecurityEvent(
                event_type=EventType.AD_LOGON,
                severity=Severity.INFO,
                risk_level=RiskLevel.LOW,
                user_context=UserContext(
                    username=raw_event.get('AccountName', 'Unknown'),
                    domain=self.config.ad_domain
                ),
                device_context=DeviceContext(
                    hostname=raw_event.get('ComputerName', 'Unknown'),
                    ip_address=raw_event.get('ClientAddress', 'Unknown'),
                    domain_joined=True
                ),
                raw_data=raw_event,
                source="ad_agent",
                tags=["ad_logon", "successful"]
            )
            
        elif event_id == 4625:  # Logon failed
            return SecurityEvent(
                event_type=EventType.AD_LOGON,
                severity=Severity.WARNING,
                risk_level=RiskLevel.MEDIUM,
                user_context=UserContext(
                    username=raw_event.get('AccountName', 'Unknown'),
                    domain=self.config.ad_domain
                ),
                device_context=DeviceContext(
                    hostname=raw_event.get('ComputerName', 'Unknown'),
                    ip_address=raw_event.get('ClientAddress', 'Unknown'),
                    domain_joined=False
                ),
                raw_data=raw_event,
                source="ad_agent",
                tags=["ad_logon", "failed", "suspicious"]
            )
            
        elif event_id == 4720:  # Account created
            return SecurityEvent(
                event_type=EventType.AD_ACCOUNT_CREATED,
                severity=Severity.INFO,
                risk_level=RiskLevel.MEDIUM,
                user_context=UserContext(
                    username=raw_event.get('AccountName', 'Unknown'),
                    domain=self.config.ad_domain
                ),
                device_context=DeviceContext(
                    hostname=raw_event.get('ComputerName', 'Unknown'),
                    ip_address="10.0.0.1",  # DC typique
                    domain_joined=True
                ),
                raw_data=raw_event,
                source="ad_agent",
                tags=["ad_account", "created"]
            )
            
        elif event_id == 4728:  # Member added to group
            return SecurityEvent(
                event_type=EventType.AD_GROUP_MODIFIED,
                severity=Severity.CRITICAL,
                risk_level=RiskLevel.HIGH,
                user_context=UserContext(
                    username=raw_event.get('AccountName', 'Unknown'),
                    domain=self.config.ad_domain
                ),
                device_context=DeviceContext(
                    hostname=raw_event.get('ComputerName', 'Unknown'),
                    ip_address="10.0.0.1",  # DC typique
                    domain_joined=True
                ),
                raw_data=raw_event,
                source="ad_agent",
                tags=["ad_group", "modified", "privilege_escalation"]
            )
        
        return None

    async def send_event_to_orchestrator(self, event: SecurityEvent):
        """Envoie l'événement formaté à l'API de l'orchestrateur."""
        if event is None:
            return
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.orchestrator_url, 
                    json=event.to_dict(),
                    timeout=10.0
                )
                
                if response.status_code == 202:  # 202 Accepted
                    self.logger.info(f"✅ Événement {event.event_id} envoyé avec succès à l'orchestrateur.")
                else:
                    self.logger.error(f"❌ Erreur lors de l'envoi de l'événement: {response.status_code} {response.text}")
                    
        except httpx.ConnectError as e:
            self.logger.error(f"❌ Impossible de se connecter à l'orchestrateur : {e}")
        except httpx.TimeoutException as e:
            self.logger.error(f"⏰ Timeout lors de l'envoi à l'orchestrateur : {e}")
        except Exception as e:
            self.logger.error(f"❌ Erreur inattendue lors de l'envoi : {e}")

    def format_event(self, win_event) -> SecurityEvent:
        """Traduit un objet EventLogRecord en un SecurityEvent Orion enrichi."""
        event_id = win_event.EventID
        string_inserts = win_event.StringInserts or []

        # --- CAS 1: Logon Réussi (4624) ---
        if event_id == 4624 and len(string_inserts) > 18:
            account_name = string_inserts[5]
            domain_name = string_inserts[6]
            ip_address = string_inserts[18]
            return SecurityEvent(
                event_type=EventType.AD_LOGON,
                user_context=UserContext(username=account_name, domain=domain_name),
                device_context=DeviceContext(hostname="unknown", ip_address=ip_address),
                raw_data={"EventID": event_id, "Inserts": string_inserts}
            )

        # --- CAS 2: Création de Compte (4720) ---
        elif event_id == 4720 and len(string_inserts) > 4:
            new_account_name = string_inserts[0]
            new_account_domain = string_inserts[1]
            admin_user = string_inserts[4]  # L'utilisateur qui a créé le compte
            self.logger.info(f"Détection de la création du compte '{new_account_name}' par '{admin_user}'.")
            return SecurityEvent(
                event_type=EventType.AD_ACCOUNT_CREATED,
                user_context=UserContext(username=admin_user.split('\\')[-1], domain=self.config.ad_domain),
                device_context=DeviceContext(hostname="DomainController", ip_address="N/A"),
                raw_data={"EventID": event_id, "Inserts": string_inserts},
                enriched_data={
                    "target_account": new_account_name,
                    "target_domain": new_account_domain
                }
            )

        # On ajoutera d'autres 'elif' ici pour les autres événements...
        return None


async def main():
    """Fonction principale pour tester l'agent."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Charger la configuration
        config = OrionConfig.load_from_file('config/local.yaml')
        
        # Créer et démarrer l'agent
        agent = ActiveDirectoryAgent(config)
        
        print("🚀 Démarrage de l'agent Active Directory...")
        print("📡 Surveillance des journaux d'événements Windows en temps réel...")
        print("🔍 Détection d'événements de sécurité critiques...")
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
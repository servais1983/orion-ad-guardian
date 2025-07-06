# Orion AD Guardian

<div align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-green?style=flat-square" alt="Project Status">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Platform-Cross%20Platform-blue?style=flat-square" alt="Platform">
</div>

<p align="center">
  <strong>Le Gardien Proactif de votre Active Directory</strong>
</p>

<p align="center">
  Orion AD Guardian est une solution de cybersécurité modulaire conçue pour protéger votre Active Directory en temps réel. Elle combine détection d'événements, analyse comportementale par IA, et remédiation automatisée pour une protection proactive contre les menaces.
</p>

---

## ✨ Fonctionnalités Principales

### 🛡️ Détection en Temps Réel
- **Surveillance continue** des événements Active Directory
- **Génération automatique d'alertes** basée sur des règles configurables
- **Analyse comportementale** avec scoring de risque dynamique
- **Détection de patterns d'attaque** (mouvement latéral, escalade de privilèges)

### 🧠 Intelligence Artificielle
- **Module Cassandra** : Analyse prédictive et scoring de risque
- **Corrélation multi-sources** des événements
- **Apprentissage automatique** des comportements normaux
- **Détection d'anomalies** en temps réel

### ⚔️ Remédiation Automatisée
- **Module Aegis** : Actions de remédiation chirurgicales
- **Quarantaine intelligente** des comptes compromis
- **Annulation automatique** des modifications non autorisées
- **Actions personnalisables** selon le niveau de menace

### 🌐 Interface Web Moderne
- **Dashboard React/TypeScript** en temps réel
- **Visualisation interactive** des alertes et statistiques
- **Actions utilisateur** (marquer comme lu, déclencher remédiation)
- **Filtres et recherche** avancés
- **Export de données** (JSON, CSV)

### 🔧 Architecture Modulaire
- **Backend FastAPI** haute performance
- **Agents légers** pour la collecte d'événements
- **Base de données PostgreSQL** pour la persistance
- **API REST sécurisée** avec authentification par token
- **Déploiement Docker** prêt pour la production

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Web React                     │
│                    (Dashboard Temps Réel)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                  Backend FastAPI                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │   Hydra     │ │  Cassandra  │ │       Aegis         │    │
│  │ (Deception) │ │ (AI/ML)     │ │   (Remediation)     │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                Agents de Collecte                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │  AD Agent   │ │ Network     │ │  Endpoint Agent     │    │
│  │ (Simulé)    │ │ Monitoring  │ │                     │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Statut Actuel du Projet

**✅ PRODUCTION READY** - Le système est entièrement fonctionnel et prêt pour le déploiement en production.

### ✅ Fonctionnalités Implémentées
- [x] **Backend FastAPI** avec API REST complète
- [x] **Interface web React/TypeScript** avec dashboard temps réel
- [x] **Module Hydra** (déception) intégré
- [x] **Module Cassandra** (IA/ML) intégré
- [x] **Module Aegis** (remédiation) intégré
- [x] **Agent AD simulé** pour les tests
- [x] **Authentification par token**
- [x] **Statistiques et export** des données
- [x] **Configuration dynamique**
- [x] **Déploiement Docker** complet
- [x] **Monitoring** (Prometheus + Grafana)
- [x] **Base de données PostgreSQL**
- [x] **Reverse proxy Nginx**

### 🔄 En Développement
- [ ] **Agents réels** pour collecte d'événements AD
- [ ] **Module de notification** (mail, SMS, webhook)
- [ ] **Tests de charge** et optimisation
- [ ] **Documentation utilisateur** complète

## 🗺️ Roadmap 2025-2026

### Q1 2025 - Production & Optimisation
- [x] **Déploiement en production** ✅
- [x] **Tests de sécurité** ✅
- [ ] **Optimisation des performances**
- [ ] **Documentation complète**

### Q2 2025 - Extension & Intégration
- [ ] **Agents AD réels** (remplacement de la simulation)
- [ ] **Intégration SIEM** (Splunk, QRadar, etc.)
- [ ] **API webhook** pour notifications
- [ ] **Module de notification** personnalisable

### Q3 2025 - Fonctionnalités Avancées
- [ ] **Machine Learning** avancé
- [ ] **Threat Intelligence** feeds
- [ ] **Forensics** automatisé
- [ ] **Compliance reporting** (SOX, GDPR, etc.)

### Q4 2025 - Écosystème
- [ ] **Marketplace** de modules
- [ ] **API publique** pour développeurs
- [ ] **Intégrations tierces** (CrowdStrike, SentinelOne, etc.)
- [ ] **Version Enterprise** avec clustering

## 🛠️ Stack Technologique

### Backend
- **Framework** : FastAPI (Python 3.12+)
- **Base de données** : PostgreSQL
- **Cache** : Redis (optionnel)
- **IA/ML** : PyTorch, scikit-learn
- **Authentification** : JWT tokens

### Frontend
- **Framework** : React 18+ avec TypeScript
- **Styling** : Tailwind CSS
- **État** : React Hooks + Context
- **HTTP Client** : Axios
- **Build** : Vite

### Infrastructure
- **Conteneurisation** : Docker + Docker Compose
- **Reverse Proxy** : Nginx
- **Monitoring** : Prometheus + Grafana
- **Logs** : Structured logging (JSON)

### Agents
- **Langage** : Python (simulation actuelle)
- **Communication** : HTTP REST API
- **Authentification** : API tokens

## 📁 Structure du Projet

```
orion-ad-guardian/
├── 📁 src/
│   ├── 📁 core/                 # Moteur principal
│   │   ├── config.py           # Configuration
│   │   ├── orchestrator.py     # Orchestrateur principal
│   │   └── main_simple.py      # Point d'entrée
│   ├── 📁 modules/
│   │   ├── 📁 hydra/           # Module de déception
│   │   ├── 📁 cassandra/       # Module d'analyse IA
│   │   └── 📁 aegis/           # Module de remédiation
│   ├── 📁 agents/              # Agents de collecte
│   │   └── ad_agent_simple.py  # Agent AD simulé
│   └── 📁 web/                 # Interface web React
│       ├── src/
│       │   ├── components/     # Composants React
│       │   ├── api/           # Client API
│       │   └── types/         # Types TypeScript
│       └── package.json
├── 📁 deployments/             # Configuration Docker
│   └── 📁 docker/
│       ├── Dockerfile.backend
│       └── Dockerfile.frontend
├── 📁 config/                  # Fichiers de configuration
│   └── production.env
├── 📁 scripts/                 # Scripts utilitaires
│   └── deploy-production.sh
├── docker-compose.prod.yml     # Stack production
└── README.md
```

## 🚀 Démarrage Rapide

### Prérequis
- Docker et Docker Compose
- Python 3.12+ (pour développement)
- Node.js 18+ (pour développement frontend)

### Déploiement Production
```bash
# Cloner le projet
git clone https://github.com/servais1983/orion-ad-guardian.git
cd orion-ad-guardian

# Déployer avec Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Accéder à l'interface web
# http://localhost:80
```

### Développement Local
```bash
# Backend
cd src/core
python main_simple.py

# Frontend
cd src/web
npm install
npm start

# Agent (optionnel)
cd src/agents
python ad_agent_simple.py
```

## 🔐 Sécurité

### Authentification
- **API tokens** pour l'authentification des agents
- **JWT tokens** pour l'interface web
- **Chiffrement** des communications HTTPS

### Données
- **Stockage sécurisé** en base PostgreSQL
- **Chiffrement** des données sensibles
- **Audit trail** complet des actions

### Réseau
- **Reverse proxy** Nginx pour la sécurité
- **CORS** configuré
- **Rate limiting** sur les API

## 📊 Monitoring

### Métriques
- **Prometheus** pour la collecte de métriques
- **Grafana** pour la visualisation
- **Alertes** configurables

### Logs
- **Structured logging** en JSON
- **Niveaux de log** configurables
- **Rotation** automatique des logs

## 🔌 Notifications Administrateur

**Le système est conçu pour être branché facilement sur un système de notification externe** (mail, SMS, webhook, etc.).

### Intégration Possible
- **Module Python** `notifier.py` (à créer dans `src/modules/`)
- **Support SMTP**, API SMS, Slack, webhook, etc.
- **Configuration** dans `config/production.env`

### Exemple d'Usage
```python
# Dans src/modules/notifier.py
class NotificationModule:
    def send_alert(self, alert: Alert):
        # Envoi mail, SMS, webhook, etc.
        pass
```

## 🤝 Contribution

### Comment Contribuer
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de Code
- **Python** : PEP 8, type hints
- **TypeScript** : ESLint, Prettier
- **Tests** : pytest pour Python, Jest pour TypeScript
- **Documentation** : docstrings, README à jour

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/servais1983/orion-ad-guardian/issues)
- **Documentation** : Voir le dossier `docs/`
- **Sécurité** : Voir `SECURITY.md`

---

<p align="center">
  <strong>Orion AD Guardian - Protection proactive de votre Active Directory</strong>
</p>
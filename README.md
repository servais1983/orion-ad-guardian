# Orion

<div align="center">
  <img src="https://img.shields.io/badge/Status-Phase%201-blue?style=flat-square" alt="Project Status">
  <img src="https://img.shields.io/badge/Version-0.1.0--alpha-orange?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/License-Proprietary-red?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20Server-blue?style=flat-square" alt="Platform">
</div>

<p align="center">
  <strong>Le Gardien Proactif de votre Active Directory</strong>
</p>

<p align="center">
  Orion est une solution de cybersécurité de nouvelle génération conçue pour protéger la zone la plus critique et la plus attaquée de votre infrastructure : l'Active Directory. Plutôt que de simplement réagir aux menaces, Orion les anticipe, les piège et les neutralise grâce à une approche innovante combinant la déception, l'analyse comportementale par IA et la remédiation automatisée.
</p>

---

## 💡 Notre Philosophie : Anticiper, Piéger, Neutraliser

Les outils de sécurité traditionnels attendent qu'une action malveillante se produise pour la bloquer. Cette approche réactive laisse une fenêtre d'opportunité aux attaquants.

**La philosophie d'Orion est de renverser ce paradigme.** Nous créons un environnement hostile pour l'attaquant, où chaque pas peut être un piège. Nous ne nous contentons pas de chercher une aiguille dans une botte de foin ; nous y ajoutons des centaines d'aiguilles magnétisées qui nous montrent exactement où chercher.

## ✨ Fonctionnalités Clés

Orion s'articule autour de trois modules principaux qui fonctionnent en parfaite synergie :

### 🛡️ Module Hydra : Déception Dynamique

Le module Hydra tisse une toile d'entités leurres (comptes, groupes, GPO, machines) parfaitement intégrées et indiscernables au sein de votre Active Directory.

- **Détection sans faux positifs** : Toute interaction avec un leurre est, par définition, une activité suspecte.
- **Empoisonnement des données** : Fournit des informations piégées aux outils de reconnaissance (type BloodHound) pour ralentir l'attaquant et l'envoyer sur de fausses pistes.
- **Leurres évolutifs** : Les entités leurres vivent et évoluent pour maintenir un réalisme constant.

### 🧠 Module Cassandra : Analyse Prédictive

Le cœur intelligent d'Orion. Cassandra modélise le comportement normal de chaque entité et utilise le Machine Learning pour prédire et identifier les menaces avant leur exécution.

- **Score de risque dynamique** : Chaque utilisateur et service se voit attribuer un score de risque qui évolue en temps réel en fonction de ses actions.
- **Identification de schémas d'attaque** : Détecte les séquences d'actions qui correspondent à des tactiques connues (mouvement latéral, escalade de privilèges), même si chaque action prise individuellement semble légitime.
- **Corrélation multi-sources** : Analyse les logs d'événements, le trafic réseau (Kerberos, LDAP) et l'activité des terminaux pour une vision à 360°.

### ⚔️ Module Aegis : Remédiation Chirurgicale

Lorsque Cassandra ou Hydra détectent une menace confirmée, Aegis applique une réponse automatisée, immédiate et proportionnée.

- **Quarantaine intelligente** : Isole une session ou un compte compromis sans le bloquer, permettant une analyse de l'attaquant dans un bac à sable.
- **Micro-segmentation à la volée** : Bloque les chemins d'attaque en appliquant des politiques de sécurité ciblées en temps réel.
- **Annulation des modifications** : Annule instantanément les changements critiques non autorisés (ex: ajout à un groupe à privilèges) et sécurise la faille exploitée.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Orion Control Center                   │
│                    (Management Console)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                  Orion Core Engine                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │   Hydra     │ │  Cassandra  │ │       Aegis         │    │
│  │ (Deception) │ │ (AI/ML)     │ │   (Remediation)     │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                Data Collection Layer                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │  AD Agent   │ │ Network     │ │  Endpoint Agent     │    │
│  │             │ │ Monitoring  │ │                     │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Statut Actuel du Projet

**Statut** : Phase 1 - Structuration et Planification

Nous sommes actuellement en phase de conception et de spécification détaillée de l'architecture et des fonctionnalités clés. L'objectif est de finaliser le cahier des charges pour lancer le développement du Produit Minimum Viable (MVP).

## 🗺️ Feuille de Route (Roadmap)

- [x] **Q2 2025** : Conceptualisation et Idéation
- [ ] **Q3 2025** : Planification Technique et Structuration du projet
- [ ] **Q4 2025** : Développement de l'MVP (focus sur les modules Hydra & Cassandra)
- [ ] **Q1 2026** : Phase de Tests (Red Team) & Validation
- [ ] **Q2 2026** : Programme Bêta avec des partenaires sélectionnés
- [ ] **Q3 2026** : Lancement Commercial

## 🛠️ Architecture Technique

### Stack Technologique

- **Agents** : C# / Go sur les Contrôleurs de Domaine
- **Backend & IA** : Python (FastAPI, TensorFlow/PyTorch)
- **Base de données** : Elasticsearch / InfluxDB pour les données temporelles
- **Frontend** : React avec TypeScript
- **Déploiement** : Conteneurisation (Docker, Kubernetes)
- **Communication** : gRPC pour les agents, REST API pour l'interface

### Prérequis Système

- **Windows Server 2016+** (Contrôleurs de domaine)
- **Active Directory Functional Level 2016+**
- **RAM** : 8GB minimum, 16GB recommandé
- **CPU** : 4 cores minimum, 8 cores recommandé
- **Stockage** : 500GB SSD minimum pour les logs et l'analytique
- **Réseau** : Accès LDAP/LDAPS aux contrôleurs de domaine

## 📁 Structure du Projet

```
orion-ad-guardian/
├── 📁 src/
│   ├── 📁 core/                 # Moteur principal Orion
│   ├── 📁 modules/
│   │   ├── 📁 hydra/           # Module de déception
│   │   ├── 📁 cassandra/       # Module d'analyse IA
│   │   └── 📁 aegis/           # Module de remédiation
│   ├── 📁 agents/              # Agents de collecte
│   ├── 📁 api/                 # API REST
│   └── 📁 web/                 # Interface web
├── 📁 docs/                    # Documentation technique
├── 📁 deployments/             # Scripts et configs de déploiement
├── 📁 tests/                   # Tests unitaires et d'intégration
└── 📁 scripts/                 # Outils et utilitaires
```

## 🔐 Sécurité

Orion manipule des données extrêmement sensibles. La sécurité est intégrée by-design :

- **Chiffrement de bout en bout** pour toutes les communications
- **Authentification mutuelle** entre tous les composants
- **Principe du moindre privilège** pour tous les agents
- **Audit trail complet** de toutes les actions
- **Stockage chiffré** des données sensibles

## 🤝 Contribution

Ce projet est actuellement en développement privé. Les contributions externes seront ouvertes après la phase bêta.

Pour les questions techniques ou commerciales, contactez l'équipe de développement.

## 📄 Licence

Ce projet est propriétaire. Tous droits réservés.

---

<p align="center">
  <strong>Orion - Parce que la meilleure défense est une attaque préventive</strong>
</p>
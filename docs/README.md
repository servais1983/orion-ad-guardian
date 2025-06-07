# Documentation Orion AD Guardian

Bienvenue dans la documentation technique d'Orion AD Guardian.

## Structure de la Documentation

### 📚 Guides Principaux

- **[Guide de Démarrage Rapide](quick-start.md)** - Installation et premier lancement
- **[Architecture](../ARCHITECTURE.md)** - Architecture technique détaillée
- **[Configuration](configuration.md)** - Guide de configuration complet
- **[Déploiement](deployment.md)** - Guides de déploiement

### 🔧 Développement

- **[Guide de Développement](development.md)** - Configuration de l'environnement de dev
- **[Standards de Code](coding-standards.md)** - Conventions et bonnes pratiques
- **[Tests](testing.md)** - Guide des tests et validation
- **[API Reference](api/README.md)** - Documentation de l'API

### 🛡️ Modules

- **[Module Hydra](modules/hydra.md)** - Déception dynamique
- **[Module Cassandra](modules/cassandra.md)** - Analyse comportementale IA
- **[Module Aegis](modules/aegis.md)** - Remédiation automatique

### 🚀 Déploiement et Opérations

- **[Installation](installation.md)** - Installation en production
- **[Monitoring](monitoring.md)** - Surveillance et métriques
- **[Troubleshooting](troubleshooting.md)** - Résolution des problèmes
- **[Sécurité](security.md)** - Bonnes pratiques de sécurité

### 📋 Références

- **[FAQ](faq.md)** - Questions fréquemment posées
- **[Glossaire](glossary.md)** - Terminologie et définitions
- **[Changelog](../CHANGELOG.md)** - Historique des versions
- **[Contribution](../CONTRIBUTING.md)** - Guide de contribution

## Démarrage Rapide

Pour commencer rapidement avec Orion :

```bash
# 1. Cloner le repository
git clone https://github.com/servais1983/orion-ad-guardian.git
cd orion-ad-guardian

# 2. Configuration de l'environnement de développement
./scripts/setup-dev.sh

# 3. Configuration
cp config/example.yaml config/local.yaml
# Éditez config/local.yaml selon votre environnement

# 4. Démarrage
source venv/bin/activate
python -m src.core.main
```

## Support

Pour obtenir de l'aide :

- 📖 Consultez la [FAQ](faq.md)
- 🐛 Signalez les bugs via [GitHub Issues](https://github.com/servais1983/orion-ad-guardian/issues)
- 💬 Discussions sur [GitHub Discussions](https://github.com/servais1983/orion-ad-guardian/discussions)
- 📧 Contact équipe : team@orion-project.com

## Contribution

Orion est un projet en développement actif. Consultez le [guide de contribution](../CONTRIBUTING.md) pour participer.

---

*Documentation mise à jour le 7 juin 2025*
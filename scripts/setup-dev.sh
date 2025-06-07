#!/bin/bash

# Script de configuration de l'environnement de développement Orion
# Usage: ./scripts/setup-dev.sh

set -e

echo "🚀 Configuration de l'environnement de développement Orion..."

# Vérification des prérequis
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ requis"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker requis"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose requis"; exit 1; }

# Vérification de la version Python
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if (( $(echo "$PYTHON_VERSION < 3.11" | bc -l) )); then
    echo "❌ Python 3.11+ requis (version actuelle: $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Prérequis validés"

# Création de l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existant"
fi

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances
echo "📚 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dépendances installées"

# Création des répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p {logs,models,data,certs}
echo "✅ Répertoires créés"

# Copie de la configuration d'exemple
echo "⚙️ Configuration..."
if [ ! -f "config/local.yaml" ]; then
    cp config/example.yaml config/local.yaml
    echo "✅ Configuration locale créée (config/local.yaml)"
    echo "💡 Modifiez config/local.yaml selon votre environnement"
else
    echo "✅ Configuration locale existante"
fi

# Démarrage des services Docker
echo "🐳 Démarrage des services Docker..."
docker-compose up -d elasticsearch influxdb redis
echo "✅ Services Docker démarrés"

# Attente de la disponibilité des services
echo "⏳ Attente de la disponibilité des services..."
sleep 30

# Vérification de la santé des services
echo "🔍 Vérification des services..."

# Elasticsearch
if curl -f http://localhost:9200/_cluster/health >/dev/null 2>&1; then
    echo "✅ Elasticsearch opérationnel"
else
    echo "❌ Elasticsearch non disponible"
fi

# InfluxDB
if curl -f http://localhost:8086/health >/dev/null 2>&1; then
    echo "✅ InfluxDB opérationnel"
else
    echo "❌ InfluxDB non disponible"
fi

# Redis
if docker exec orion-redis redis-cli ping >/dev/null 2>&1; then
    echo "✅ Redis opérationnel"
else
    echo "❌ Redis non disponible"
fi

# Installation des pre-commit hooks (optionnel)
if command -v pre-commit >/dev/null 2>&1; then
    echo "🪝 Installation des pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installés"
fi

# Instructions finales
echo ""
echo "🎉 Environnement de développement configuré avec succès !"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. Activez l'environnement virtuel : source venv/bin/activate"
echo "   2. Modifiez config/local.yaml selon votre AD"
echo "   3. Lancez les tests : python -m pytest"
echo "   4. Démarrez Orion : python -m src.core.main"
echo ""
echo "🔗 Services disponibles :"
echo "   - Elasticsearch : http://localhost:9200"
echo "   - InfluxDB : http://localhost:8086"
echo "   - Redis : localhost:6379"
echo ""
echo "📚 Documentation : voir docs/README.md"
echo ""
echo "🐛 Pour les visualisations (optionnel) :"
echo "   docker-compose --profile visualization up -d"
echo "   - Kibana : http://localhost:5601"
echo "   - Grafana : http://localhost:3000 (admin/orion-dev-password)"
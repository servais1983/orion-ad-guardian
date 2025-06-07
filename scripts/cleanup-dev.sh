#!/bin/bash

# Script de nettoyage de l'environnement de développement Orion
# Usage: ./scripts/cleanup-dev.sh [--force]

set -e

FORCE=false
if [ "$1" = "--force" ]; then
    FORCE=true
fi

echo "🧹 Nettoyage de l'environnement de développement Orion..."

if [ "$FORCE" = false ]; then
    echo "⚠️ Cette action va supprimer :"
    echo "   - Tous les conteneurs Docker Orion"
    echo "   - Tous les volumes Docker (données perdues !)"
    echo "   - L'environnement virtuel Python"
    echo "   - Les logs et données locales"
    echo ""
    read -p "Êtes-vous sûr ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Nettoyage annulé"
        exit 0
    fi
fi

# Arrêt et suppression des conteneurs
echo "🛑 Arrêt des conteneurs Docker..."
docker-compose down --volumes --remove-orphans

# Suppression des images Orion
echo "🗑️ Suppression des images Docker Orion..."
docker images | grep orion | awk '{print $3}' | xargs -r docker rmi -f

# Nettoyage des volumes orphelins
echo "🧽 Nettoyage des volumes Docker..."
docker volume prune -f

# Suppression de l'environnement virtuel
if [ -d "venv" ]; then
    echo "🗂️ Suppression de l'environnement virtuel..."
    rm -rf venv
    echo "✅ Environnement virtuel supprimé"
fi

# Suppression des fichiers temporaires
echo "🗃️ Suppression des fichiers temporaires..."
rm -rf logs/* 2>/dev/null || true
rm -rf data/* 2>/dev/null || true
rm -rf models/* 2>/dev/null || true
rm -rf __pycache__ 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Suppression de la configuration locale (optionnel)
if [ -f "config/local.yaml" ]; then
    if [ "$FORCE" = true ]; then
        rm -f config/local.yaml
        echo "✅ Configuration locale supprimée"
    else
        read -p "Supprimer config/local.yaml ? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f config/local.yaml
            echo "✅ Configuration locale supprimée"
        else
            echo "✅ Configuration locale conservée"
        fi
    fi
fi

echo ""
echo "🎉 Nettoyage terminé !"
echo ""
echo "💡 Pour reconfigurer l'environnement :"
echo "   ./scripts/setup-dev.sh"
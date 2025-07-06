#!/bin/bash

# Script pour démarrer l'interface web Orion
echo "🚀 Démarrage de l'interface web Orion..."

# Aller dans le dossier web
cd src/web

# Installer les dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances React..."
    npm install
fi

# Démarrer le serveur de développement
echo "🌐 Lancement du serveur de développement React..."
echo "📱 Interface disponible sur: http://localhost:3000"
echo "🔗 API backend: http://localhost:8000"
echo "⏹️  Appuyez sur Ctrl+C pour arrêter"

npm start 
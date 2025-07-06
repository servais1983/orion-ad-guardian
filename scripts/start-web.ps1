# Script PowerShell pour démarrer l'interface web Orion
Write-Host "🚀 Démarrage de l'interface web Orion..." -ForegroundColor Green

# Aller dans le dossier web
Set-Location "src/web"

# Installer les dépendances si nécessaire
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installation des dépendances React..." -ForegroundColor Yellow
    npm install
}

# Démarrer le serveur de développement
Write-Host "🌐 Lancement du serveur de développement React..." -ForegroundColor Green
Write-Host "📱 Interface disponible sur: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 API backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "⏹️  Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow

npm start 
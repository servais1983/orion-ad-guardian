# Script de lancement d'Orion AD Guardian
# Lance tous les composants en parallèle dans des fenêtres séparées

Write-Host "🛡️  Lancement d'Orion AD Guardian..." -ForegroundColor Green
Write-Host ""

# Vérifier que nous sommes dans le bon répertoire
if (-not (Test-Path "src")) {
    Write-Host "❌ Erreur: Ce script doit être exécuté depuis la racine du projet Orion AD Guardian" -ForegroundColor Red
    exit 1
}

# Fonction pour lancer un processus dans une nouvelle fenêtre
function Start-ProcessInNewWindow {
    param(
        [string]$Title,
        [string]$Command,
        [string]$WorkingDirectory = $PWD
    )
    
    Write-Host "🚀 Lancement: $Title" -ForegroundColor Yellow
    
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = "powershell.exe"
    $processInfo.Arguments = "-NoExit", "-Command", "cd '$WorkingDirectory'; Write-Host '=== $Title ===' -ForegroundColor Cyan; $Command"
    $processInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo
    $process.Start() | Out-Null
    
    Start-Sleep -Seconds 2
    return $process
}

try {
    # 1. Lancer le backend FastAPI
    Write-Host "📡 Démarrage du backend FastAPI..." -ForegroundColor Blue
    $backendProcess = Start-ProcessInNewWindow -Title "Orion Backend (Port 8006)" -Command "python src/core/main_simple.py"
    
    # 2. Lancer l'agent AD simulé
    Write-Host "🤖 Démarrage de l'agent AD simulé..." -ForegroundColor Blue
    $agentProcess = Start-ProcessInNewWindow -Title "Orion Agent AD" -Command "python src/agents/ad_agent_simple.py"
    
    # 3. Lancer l'interface web React
    Write-Host "🌐 Démarrage de l'interface web React..." -ForegroundColor Blue
    $webProcess = Start-ProcessInNewWindow -Title "Orion Web Interface (Port 3180)" -Command "cd src/web; npm start"
    
    Write-Host ""
    Write-Host "✅ Orion AD Guardian est en cours de démarrage..." -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Services lancés:" -ForegroundColor Cyan
    Write-Host "   • Backend API: http://localhost:8006" -ForegroundColor White
    Write-Host "   • Interface Web: http://localhost:3180" -ForegroundColor White
    Write-Host "   • Agent AD: Simulation d'événements" -ForegroundColor White
    Write-Host ""
    Write-Host "🔗 Ouvrez http://localhost:3180 dans votre navigateur" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⏹️  Pour arrêter tous les services, fermez les fenêtres ou appuyez sur Ctrl+C" -ForegroundColor Gray
    Write-Host ""
    
    # Attendre que l'utilisateur appuie sur une touche pour arrêter
    Write-Host "Appuyez sur une touche pour arrêter tous les services..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Arrêter tous les processus
    Write-Host ""
    Write-Host "🛑 Arrêt des services..." -ForegroundColor Yellow
    
    if ($backendProcess -and -not $backendProcess.HasExited) {
        $backendProcess.Kill()
        Write-Host "   • Backend arrêté" -ForegroundColor Gray
    }
    
    if ($agentProcess -and -not $agentProcess.HasExited) {
        $agentProcess.Kill()
        Write-Host "   • Agent arrêté" -ForegroundColor Gray
    }
    
    if ($webProcess -and -not $webProcess.HasExited) {
        $webProcess.Kill()
        Write-Host "   • Interface web arrêtée" -ForegroundColor Gray
    }
    
    Write-Host "✅ Tous les services ont été arrêtés" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Erreur lors du lancement: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 
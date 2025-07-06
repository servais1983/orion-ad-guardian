#!/bin/bash

# Script de déploiement en production pour Orion AD Guardian
# Usage: ./scripts/deploy-production.sh [start|stop|restart|update]

set -e

# Configuration
PROJECT_NAME="orion-ad-guardian"
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE="config/production.env"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    # Vérifier le fichier d'environnement
    if [ ! -f "$ENV_FILE" ]; then
        log_warning "Fichier d'environnement $ENV_FILE non trouvé"
        log_info "Création du fichier d'environnement par défaut..."
        cp config/production.env.example "$ENV_FILE" 2>/dev/null || {
            log_error "Impossible de créer le fichier d'environnement"
            exit 1
        }
    fi
    
    log_success "Prérequis vérifiés"
}

# Fonction pour charger les variables d'environnement
load_env() {
    log_info "Chargement des variables d'environnement..."
    if [ -f "$ENV_FILE" ]; then
        export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
    fi
}

# Fonction pour démarrer les services
start_services() {
    log_info "Démarrage des services Orion AD Guardian..."
    
    # Construire les images si nécessaire
    log_info "Construction des images Docker..."
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    
    # Démarrer les services
    log_info "Démarrage des conteneurs..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # Attendre que les services soient prêts
    log_info "Attente du démarrage des services..."
    sleep 30
    
    # Vérifier l'état des services
    check_services_health
    
    log_success "Services démarrés avec succès"
}

# Fonction pour arrêter les services
stop_services() {
    log_info "Arrêt des services Orion AD Guardian..."
    docker-compose -f "$COMPOSE_FILE" down
    log_success "Services arrêtés"
}

# Fonction pour redémarrer les services
restart_services() {
    log_info "Redémarrage des services Orion AD Guardian..."
    docker-compose -f "$COMPOSE_FILE" restart
    log_success "Services redémarrés"
}

# Fonction pour mettre à jour les services
update_services() {
    log_info "Mise à jour des services Orion AD Guardian..."
    
    # Arrêter les services
    stop_services
    
    # Récupérer les dernières modifications
    log_info "Récupération des dernières modifications..."
    git pull origin main
    
    # Reconstruire et redémarrer
    start_services
    
    log_success "Services mis à jour"
}

# Fonction pour vérifier la santé des services
check_services_health() {
    log_info "Vérification de la santé des services..."
    
    # Vérifier le backend
    if curl -f http://localhost:8006/health > /dev/null 2>&1; then
        log_success "Backend API opérationnel"
    else
        log_error "Backend API non accessible"
        return 1
    fi
    
    # Vérifier le frontend
    if curl -f http://localhost:3180 > /dev/null 2>&1; then
        log_success "Interface web opérationnelle"
    else
        log_error "Interface web non accessible"
        return 1
    fi
    
    # Vérifier la base de données
    if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U orion_user > /dev/null 2>&1; then
        log_success "Base de données opérationnelle"
    else
        log_error "Base de données non accessible"
        return 1
    fi
}

# Fonction pour afficher les logs
show_logs() {
    log_info "Affichage des logs..."
    docker-compose -f "$COMPOSE_FILE" logs -f
}

# Fonction pour afficher l'état des services
show_status() {
    log_info "État des services Orion AD Guardian:"
    docker-compose -f "$COMPOSE_FILE" ps
    
    echo ""
    log_info "URLs d'accès:"
    echo "  Interface web: http://localhost:3180"
    echo "  API Backend: http://localhost:8006"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana: http://localhost:3000"
}

# Fonction pour sauvegarder les données
backup_data() {
    log_info "Sauvegarde des données..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Sauvegarder la base de données
    docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_dump -U orion_user orion_ad_guardian > "$BACKUP_DIR/database.sql"
    
    # Sauvegarder les logs
    if [ -d "logs" ]; then
        cp -r logs "$BACKUP_DIR/"
    fi
    
    log_success "Sauvegarde créée dans $BACKUP_DIR"
}

# Fonction pour afficher l'aide
show_help() {
    echo "Script de déploiement Orion AD Guardian"
    echo ""
    echo "Usage: $0 [COMMANDE]"
    echo ""
    echo "Commandes:"
    echo "  start     - Démarrer les services"
    echo "  stop      - Arrêter les services"
    echo "  restart   - Redémarrer les services"
    echo "  update    - Mettre à jour et redémarrer les services"
    echo "  status    - Afficher l'état des services"
    echo "  logs      - Afficher les logs"
    echo "  backup    - Sauvegarder les données"
    echo "  health    - Vérifier la santé des services"
    echo "  help      - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 start"
    echo "  $0 update"
    echo "  $0 status"
}

# Fonction principale
main() {
    case "${1:-help}" in
        start)
            check_prerequisites
            load_env
            start_services
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        update)
            check_prerequisites
            load_env
            update_services
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        backup)
            backup_data
            ;;
        health)
            check_services_health
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Commande inconnue: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter la fonction principale
main "$@" 
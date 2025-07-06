# 🛡️ Orion AD Guardian - Fonctionnalités Interactives

## Vue d'ensemble

Orion AD Guardian dispose maintenant d'une interface web interactive complète permettant aux administrateurs de sécurité de visualiser, filtrer et agir sur les alertes en temps réel.

## 🚀 Lancement Rapide

### Option 1: Script PowerShell (Recommandé)
```powershell
.\scripts\launch-orion.ps1
```

### Option 2: Lancement Manuel
```powershell
# Terminal 1 - Backend
python src/core/main_simple.py

# Terminal 2 - Agent
python src/agents/ad_agent_simple.py

# Terminal 3 - Interface Web
cd src/web
npm start
```

## 🌐 Interface Web

### URL d'accès
- **Interface principale**: http://localhost:3180
- **API Backend**: http://localhost:8006

### Fonctionnalités Principales

#### 1. 📊 Tableau de Bord en Temps Réel
- **Statistiques en direct** : Total d'alertes, alertes critiques, élevées
- **Rafraîchissement automatique** : Mise à jour toutes les 5 secondes
- **Indicateurs visuels** : Codes couleur par niveau de risque

#### 2. 🔍 Filtrage et Recherche
- **Filtre par niveau de risque** : Critique, Élevé, Moyen, Faible
- **Recherche textuelle** : Par utilisateur, justification, source
- **Compteur d'alertes affichées** : Mise à jour en temps réel

#### 3. ⚡ Actions Interactives

##### Bouton "👁️" - Voir Détails
- **Modal détaillé** avec toutes les informations de l'alerte
- **Données brutes** de l'événement AD
- **Contexte utilisateur et appareil**
- **Marquage automatique** comme lue

##### Bouton "✓" - Marquer comme Lu
- **Action immédiate** via API backend
- **Notification de confirmation**
- **Mise à jour de l'état** en temps réel

##### Bouton "🛡️" - Remédiation (Alertes HIGH/CRITICAL uniquement)
- **Actions automatiques** selon le niveau de risque
- **Simulation de remédiation** avec délai réaliste
- **Notification des actions** prises

#### 4. 🔔 Système de Notifications
- **Toasts animés** : Succès (vert), Erreur (rouge), Info (bleu)
- **Auto-disparition** après 3 secondes
- **Fermeture manuelle** possible

## 🎨 Interface Utilisateur

### Design Moderne
- **Gradients colorés** pour les statistiques
- **Animations fluides** pour les interactions
- **Responsive design** pour mobile et desktop
- **Codes couleur intuitifs** par niveau de risque

### Expérience Utilisateur
- **Hover effects** sur les éléments interactifs
- **Feedback visuel** immédiat sur les actions
- **Navigation intuitive** avec icônes explicites
- **Chargement progressif** des données

## 🔧 API Backend

### Nouveaux Endpoints

#### GET `/api/v1/alerts/{alert_id}`
Récupère les détails complets d'une alerte spécifique.

#### POST `/api/v1/alerts/{alert_id}/mark-read`
Marque une alerte comme lue.

#### POST `/api/v1/alerts/{alert_id}/remediate`
Déclenche des actions de remédiation automatiques.

#### GET `/api/v1/stats`
Récupère les statistiques détaillées des alertes.

### Actions de Remédiation Simulées

#### Pour les Alertes HIGH/CRITICAL
**Source Cassandra :**
- Désactivation du compte utilisateur
- Déconnexion forcée des sessions
- Notification à l'administrateur

**Source Hydra :**
- Mise en quarantaine de l'entité
- Analyse approfondie déclenchée

#### Pour les Alertes MEDIUM/LOW
- Surveillance renforcée
- Log des actions utilisateur

## 📱 Responsive Design

### Desktop (1200px+)
- **Layout en grille** pour les statistiques
- **Tableau complet** avec toutes les colonnes
- **Actions horizontales** dans les cellules

### Tablette (768px - 1199px)
- **Grille adaptée** 2x2 pour les stats
- **Filtres empilés** verticalement
- **Boutons d'action** redimensionnés

### Mobile (< 768px)
- **Grille 2x2** pour les statistiques
- **Filtres en colonne**
- **Actions verticales** dans les cellules
- **Modal adapté** à l'écran

## 🛠️ Développement

### Structure des Composants
```
AlertsDashboard.tsx
├── AlertModal (Modal de détails)
├── Toast (Notifications)
├── Filtres et recherche
├── Tableau des alertes
└── Statistiques
```

### Technologies Utilisées
- **React 18** avec TypeScript
- **CSS Modules** pour le styling
- **Fetch API** pour les requêtes HTTP
- **Hooks React** pour l'état et les effets

### État de l'Application
- **Alertes** : Liste principale des alertes
- **Alertes filtrées** : Résultat des filtres appliqués
- **Alerte sélectionnée** : Pour le modal de détails
- **Notifications** : Système de toast
- **Filtres** : État des filtres actifs

## 🔒 Sécurité

### CORS Configuration
- **Origines autorisées** : localhost:3180, 127.0.0.1:3180
- **Méthodes HTTP** : GET, POST, PUT, DELETE
- **Headers** : Content-Type, Authorization

### Validation des Données
- **Types TypeScript** stricts pour les interfaces
- **Validation backend** des paramètres
- **Gestion d'erreurs** complète

## 🚀 Prochaines Étapes

### Fonctionnalités Planifiées
1. **Authentification** utilisateur
2. **Rôles et permissions** 
3. **Historique des actions** de remédiation
4. **Export des alertes** (CSV, PDF)
5. **Intégration** avec des SIEM externes
6. **Alertes par email/SMS**
7. **Dashboard analytique** avancé

### Améliorations Techniques
1. **WebSocket** pour les mises à jour en temps réel
2. **Cache Redis** pour les performances
3. **Base de données** persistante
4. **Tests automatisés** complets
5. **CI/CD** pipeline

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs dans les terminaux
2. Consultez la documentation API
3. Testez les endpoints avec un client HTTP
4. Vérifiez la configuration CORS

---

**Orion AD Guardian** - Protection Active Directory Intelligente 🛡️ 
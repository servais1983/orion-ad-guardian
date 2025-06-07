# Contributing to Orion

🎉 Merci pour votre intérêt à contribuer au projet Orion !

## Statut Actuel

**Important**: Le projet Orion est actuellement en phase de développement initial (Phase 1). Les contributions externes ne sont pas encore ouvertes, mais nous préparons l'infrastructure pour accueillir des contributeurs dans les phases suivantes.

## Phases de Contribution

### Phase 1 - Développement Initial (Actuel)
- ❌ Contributions externes fermées
- ✅ Équipe core uniquement
- 🎯 Focus: Architecture et MVP

### Phase 2 - Développement MVP (Q4 2025)
- ⚠️ Contributions limitées aux partenaires techniques
- 🎯 Focus: Tests et validation

### Phase 3 - Programme Bêta (Q2 2026)
- ✅ Contributions ouvertes avec approbation
- 🎯 Focus: Amélioration et stabilisation

### Phase 4 - Open Source (TBD)
- ✅ Contributions ouvertes à la communauté
- 🎯 Focus: Évolution et nouvelles fonctionnalités

## Comment Contribuer (Prochaines Phases)

### 🐛 Signalement de Bugs

Lorsque les contributions seront ouvertes, vous pourrez signaler des bugs en créant une issue avec :

1. **Description claire** du problème
2. **Étapes de reproduction** détaillées
3. **Comportement attendu** vs comportement observé
4. **Environnement** (OS, version AD, etc.)
5. **Logs pertinents** (anonymisés)

### 💡 Propositions d'Améliorations

Pour proposer de nouvelles fonctionnalités :

1. **Vérifiez** qu'elle n'existe pas déjà dans la roadmap
2. **Décrivez** le besoin métier
3. **Proposez** une solution technique
4. **Évaluez** l'impact sur les performances
5. **Considérez** les implications de sécurité

### 🔧 Contributions de Code

#### Prérequis
- Connaissance approfondie d'Active Directory
- Expérience en cybersécurité
- Maîtrise de Python, C#, ou JavaScript/TypeScript
- Compréhension des principes de Machine Learning (pour Cassandra)

#### Standards de Code

**Python**
```python
# Suivre PEP 8
# Type hints obligatoires
# Docstrings complètes
# Tests unitaires minimum 80% de couverture

from typing import List, Optional

def analyze_user_behavior(
    user_id: str, 
    events: List[SecurityEvent],
    threshold: Optional[float] = 0.7
) -> RiskScore:
    """Analyse le comportement d'un utilisateur pour détecter des anomalies.
    
    Args:
        user_id: Identifiant unique de l'utilisateur
        events: Liste des événements de sécurité
        threshold: Seuil de détection d'anomalie (défaut: 0.7)
        
    Returns:
        Score de risque calculé
        
    Raises:
        ValueError: Si user_id est invalide
    """
    pass
```

**C#**
```csharp
// Suivre les conventions Microsoft
// XML Documentation obligatoire
// Async/await pour toutes les opérations I/O
// Unit tests avec xUnit

/// <summary>
/// Collecte les événements de sécurité depuis Active Directory
/// </summary>
/// <param name="domainController">Contrôleur de domaine cible</param>
/// <param name="filters">Filtres à appliquer</param>
/// <returns>Liste des événements collectés</returns>
public async Task<IEnumerable<SecurityEvent>> CollectSecurityEventsAsync(
    string domainController,
    EventFilters filters)
{
    // Implementation
}
```

#### Processus de Review

1. **Fork** du repository
2. **Branche** dédiée par fonctionnalité
3. **Commits** atomiques avec messages clairs
4. **Tests** complets
5. **Pull Request** avec description détaillée
6. **Review** par minimum 2 membres de l'équipe core
7. **Merge** après approbation

#### Messages de Commit

```
type(scope): description courte en français

Description plus détaillée si nécessaire.
Expliquer le pourquoi, pas le comment.

Fixes #123
```

Types :
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `docs`: documentation
- `style`: formatage
- `refactor`: refactoring
- `test`: tests
- `chore`: maintenance

Scopes :
- `hydra`: module de déception
- `cassandra`: module d'analyse IA
- `aegis`: module de remédiation
- `core`: moteur principal
- `api`: interface API
- `web`: interface web
- `agent`: agents de collecte

### 📚 Documentation

La documentation est cruciale pour un projet de sécurité :

- **README** : Vue d'ensemble et quick start
- **Architecture** : Documentation technique détaillée
- **API** : Documentation auto-générée avec OpenAPI
- **Deployment** : Guides de déploiement
- **Security** : Pratiques de sécurité

## Standards de Sécurité

### Code Review Sécurisé

Tout code doit être reviewé sous l'angle sécurité :

- ✅ Validation des entrées
- ✅ Gestion des erreurs
- ✅ Logging sécurisé (pas de données sensibles)
- ✅ Authentification et autorisation
- ✅ Chiffrement des données sensibles
- ✅ Protection contre l'injection
- ✅ Gestion sécurisée des sessions

### Tests de Sécurité

- **SAST** : Analyse statique automatique
- **DAST** : Tests dynamiques
- **Dependency Check** : Vulnérabilités des dépendances
- **Penetration Testing** : Tests d'intrusion réguliers

## Communication

### Canaux de Communication (Future)

- **GitHub Issues** : Bugs et fonctionnalités
- **GitHub Discussions** : Questions générales
- **Discord** : Chat en temps réel (communauté)
- **Email** : Questions sensibles ou privées

### Langues

- **Français** : Langue principale du projet
- **Anglais** : Accepté pour la contribution internationale
- **Code** : Commentaires en français, variables/fonctions en anglais

## Code de Conduite

### Nos Valeurs

- **Respect** : Traiter tous les contributeurs avec respect
- **Inclusivité** : Accueillir toutes les perspectives
- **Collaboration** : Travailler ensemble vers un objectif commun
- **Excellence** : Viser la qualité et l'innovation
- **Sécurité** : Prioriser la sécurité dans toutes les décisions

### Comportements Attendus

- Communication constructive et professionnelle
- Feedback bienveillant et actionnable
- Reconnaissance du travail des autres
- Partage des connaissances
- Respect des deadlines et engagements

### Comportements Inacceptables

- Langage offensant ou discriminatoire
- Harcèlement sous toute forme
- Publication d'informations privées
- Disruption des discussions
- Comportement non professionnel

## Reconnaissance

Tous les contributeurs seront reconnus :

- **CONTRIBUTORS.md** : Liste des contributeurs
- **Release Notes** : Mention des contributions importantes
- **Crédits** : Dans la documentation et l'interface

## Questions ?

Pour toute question sur la contribution :

- 📧 **Email** : contribute@orion-project.com
- 🐛 **Issue** : Pour les questions publiques
- 📖 **Wiki** : Documentation détaillée (à venir)

---

*Ce guide de contribution sera mis à jour régulièrement selon l'évolution du projet.*
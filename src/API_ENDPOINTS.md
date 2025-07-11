# Documentation des Endpoints API - Système d'Affiliation

## 🔐 Authentification JWT

Tous les endpoints (sauf ceux marqués comme publics) nécessitent une authentification JWT.
Ajoutez le header : `Authorization: Bearer <votre_access_token>`

### Configuration JWT
- **Access Token** : 24 heures
- **Refresh Token** : 7 jours
- **Algorithme** : HS256
- **Type** : Bearer

### Types d'Utilisateurs
- **Superuser Django** : Administrateur principal créé avec `python manage.py createsuperuser`
- **Influenceur** : Utilisateur du système d'affiliation avec permissions limitées

## Endpoints d'Authentification

### POST /api/v1/auth/login/
**Public** - Connexion des superusers et influenceurs
```json
{
  "email": "admin@example.com",
  "password": "adminpass123"
}
```
**Réponse pour Superuser :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_type": "superuser",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_superuser": true
  },
  "permissions": {
    "is_admin": true,
    "is_moderateur": false,
    "peut_creer_influenceurs": true,
    "peut_valider_prospects": true,
    "peut_payer_remises": true,
    "peut_voir_statistiques": true,
    "peut_gerer_systeme": true
  },
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**Réponse pour Influenceur :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_type": "influenceur",
  "influenceur": {
    "id": 1,
    "nom": "Influenceur Test",
    "email": "influenceur@example.com",
    "role": "influenceur",
    "code_affiliation": "abc12345"
  },
  "permissions": {
    "is_admin": false,
    "is_moderateur": false,
    "peut_creer_influenceurs": false,
    "peut_valider_prospects": false,
    "peut_payer_remises": false,
    "peut_voir_statistiques": true
  },
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### POST /api/v1/auth/refresh/
**Public** - Rafraîchir un token JWT
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
**Réponse :**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### POST /api/v1/auth/logout/
**Authentifié** - Déconnexion
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Déconnexion réussie"
}
```

### GET /api/v1/auth/profile/
**Authentifié** - Récupérer le profil de l'utilisateur connecté
**Headers :** `Authorization: Bearer <access_token>`

**Réponse pour Superuser :**
```json
{
  "user_type": "superuser",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_superuser": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z"
  },
  "permissions": {
    "is_admin": true,
    "is_moderateur": false,
    "peut_creer_influenceurs": true,
    "peut_valider_prospects": true,
    "peut_payer_remises": true,
    "peut_voir_statistiques": true,
    "peut_gerer_systeme": true
  }
}
```

**Réponse pour Influenceur :**
```json
{
  "user_type": "influenceur",
  "influenceur": {
    "id": 1,
    "nom": "Influenceur Test",
    "email": "influenceur@example.com",
    "role": "influenceur",
    "code_affiliation": "abc12345",
    "date_creation": "2024-01-01T00:00:00Z",
    "is_active": true
  },
  "permissions": {
    "is_admin": false,
    "is_moderateur": false,
    "peut_creer_influenceurs": false,
    "peut_valider_prospects": false,
    "peut_payer_remises": false,
    "peut_voir_statistiques": true
  },
  "last_login": "2024-01-01T12:00:00Z",
  "account_status": {
    "is_active": true,
    "is_locked": false,
    "login_attempts": 0
  }
}
```

### POST /api/v1/auth/register/
**Public** - Inscription des nouveaux influenceurs
```json
{
  "nom": "Nouvel Influenceur",
  "email": "nouveau@example.com",
  "password": "motdepasse123"
}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Inscription réussie",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "influenceur": {...},
  "permissions": {...},
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### POST /api/v1/auth/change-password/
**Authentifié** - Changer le mot de passe
```json
{
  "current_password": "ancien_mot_de_passe",
  "new_password": "nouveau_mot_de_passe"
}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Mot de passe modifié avec succès"
}
```

## Endpoints d'Administration

### POST /api/v1/admin/create-influenceur/
**Superuser uniquement** - Créer un nouvel influenceur
**Headers :** `Authorization: Bearer <superuser_access_token>`
```json
{
  "nom": "Nouvel Influenceur",
  "email": "influenceur@example.com",
  "password": "motdepasse123",
  "role": "influenceur"
}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Influenceur créé avec succès",
  "influenceur": {
    "id": 2,
    "nom": "Nouvel Influenceur",
    "email": "influenceur@example.com",
    "role": "influenceur",
    "code_affiliation": "def67890"
  }
}
```

## Endpoints des Influenceurs

### GET /api/v1/influenceurs/
**Superuser uniquement** - Lister tous les influenceurs
**Headers :** `Authorization: Bearer <superuser_access_token>`

### POST /api/v1/influenceurs/
**Superuser uniquement** - Créer un nouvel influenceur
```json
{
  "nom": "Nom de l'influenceur",
  "email": "influenceur@example.com",
  "password": "motdepasse",
  "role": "influenceur"
}
```

### GET /api/v1/influenceurs/{id}/
**Authentifié** - Détails d'un influenceur (propre profil ou superuser)

### PUT/PATCH /api/v1/influenceurs/{id}/update/
**Authentifié** - Modifier un influenceur (propre profil ou superuser)

### DELETE /api/v1/influenceurs/{id}/
**Superuser uniquement** - Supprimer un influenceur

### GET /api/v1/influenceurs/{id}/dashboard/
**Authentifié** - Dashboard d'un influenceur (propre dashboard ou superuser)
**Réponse :**
```json
{
  "influenceur": "Nom de l'influenceur",
  "code_affiliation": "abc12345",
  "nb_prospects": 10,
  "nb_prospects_confirmes": 5,
  "montant_total_remises_payees": 150.00,
  "prospects": [...],
  "remises": [...]
}
```

### GET /api/v1/influenceurs/{id}/prospects/
**Authentifié** - Prospects d'un influenceur (propres prospects ou superuser)

### GET /api/v1/influenceurs/{id}/remises/
**Authentifié** - Remises d'un influenceur (propres remises ou superuser)

## Endpoints des Prospects

### GET /api/v1/prospects/
**Authentifié** - Lister les prospects (propres prospects ou tous pour superuser)

### POST /api/v1/prospects/
**Authentifié** - Créer un prospect
```json
{
  "nom": "Nom du prospect",
  "email": "prospect@example.com",
  "influenceur": 1
}
```

### POST /api/v1/prospects/{id}/valider/
**Permission de validation** - Valider un prospect
```json
{
  "statut": "confirme"
}
```

### GET /api/v1/prospects/sans-remise/
**Authentifié** - Prospects sans remise (propres prospects ou tous pour superuser)

## Endpoints des Remises

### GET /api/v1/remises/
**Authentifié** - Lister les remises (propres remises ou toutes pour superuser)

### POST /api/v1/remises/
**Authentifié** - Créer une remise
```json
{
  "montant": 25.00,
  "description": "Commission pour prospect confirmé",
  "influenceur": 1
}
```

### POST /api/v1/remises/{id}/payer/
**Permission de paiement** - Marquer une remise comme payée
```json
{
  "justificatif": "fichier_upload"
}
```

### POST /api/v1/remises/calculer-automatiques/
**Superuser uniquement** - Calculer automatiquement les remises
```json
{
  "montant_par_prospect": 10.00
}
```

### POST /api/v1/remises/calculer-influenceur/{influenceur_id}/
**Superuser uniquement** - Calculer remise pour un influenceur spécifique

### GET /api/v1/remises/statistiques/
**Superuser uniquement** - Statistiques globales des remises

## Endpoint Public

### GET /affiliation/{code_affiliation}/
**Public** - Formulaire d'affiliation publique
- Affiche un formulaire HTML pour l'inscription via un lien d'affiliation
- Accepte les soumissions POST avec nom et email

### POST /affiliation/{code_affiliation}/
**Public** - Soumission du formulaire d'affiliation
```json
{
  "nom": "Nom du prospect",
  "email": "prospect@example.com"
}
```

## Codes de Statut HTTP

- `200` - Succès
- `201` - Créé avec succès
- `400` - Données invalides
- `401` - Non authentifié (token invalide ou expiré)
- `403` - Accès interdit (permissions insuffisantes)
- `404` - Ressource non trouvée
- `429` - Trop de tentatives de connexion (compte bloqué)
- `500` - Erreur serveur

## Permissions par Type d'Utilisateur

### Superuser Django
- **Accès complet** à toutes les fonctionnalités
- **Peut créer/supprimer** des influenceurs
- **Peut voir toutes** les statistiques
- **Peut valider tous** les prospects
- **Peut payer toutes** les remises
- **Peut gérer le système** complet
- **Permissions automatiques** : Toutes les permissions sont activées

### Influenceur
- **Peut voir/modifier** son propre profil
- **Peut voir ses propres** prospects et remises
- **Peut voir son propre** dashboard
- **Permissions spécifiques** selon configuration
- **Accès limité** aux fonctionnalités d'administration

## Sécurité

### Protection contre les attaques
- **Blocage automatique** après 5 tentatives de connexion échouées
- **Durée de blocage** : 30 minutes
- **Hachage des mots de passe** avec bcrypt
- **Tokens JWT** avec expiration automatique
- **Refresh tokens** pour renouvellement sécurisé

### Validation des données
- **Validation côté serveur** pour tous les champs
- **Sanitisation** des entrées utilisateur
- **Protection CSRF** pour les formulaires
- **Validation des emails** et formats

## Exemples d'Utilisation

### Connexion du Superuser
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "adminpass123"}'
```

### Connexion d'un Influenceur
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "influenceur@example.com", "password": "influenceurpass123"}'
```

### Utilisation du token pour accéder aux données
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer votre_access_token_ici"
```

### Création d'influenceur par Superuser
```bash
curl -X POST http://localhost:8000/api/v1/admin/create-influenceur/ \
  -H "Authorization: Bearer superuser_access_token" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Nouvel Influenceur", "email": "nouveau@example.com", "password": "motdepasse123"}'
```

### Rafraîchissement du token
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "votre_refresh_token_ici"}'
```

### Création d'un prospect via le formulaire d'affiliation
```bash
curl -X POST http://localhost:8000/affiliation/abc12345/ \
  -H "Content-Type: application/json" \
  -d '{"nom": "Nouveau Prospect", "email": "prospect@example.com"}'
```

## Configuration Initiale

### 1. Créer un Superuser Django
```bash
python manage.py createsuperuser
# Suivez les instructions pour créer l'administrateur principal
```

### 2. Tester l'Authentification
```bash
python test_superuser_auth.py
```

### 3. Informations de Connexion
- **Superuser** : Utilisez les identifiants créés avec `createsuperuser`
- **Influenceur** : Créé automatiquement lors des tests ou par le superuser 
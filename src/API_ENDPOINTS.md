# Documentation des Endpoints API - Système d'Affiliation

## Authentification

Tous les endpoints (sauf ceux marqués comme publics) nécessitent une authentification par token.
Ajoutez le header : `Authorization: Token <votre_token>`

## Endpoints d'Authentification

### POST /api/v1/auth/login/
**Public** - Connexion des influenceurs
```json
{
  "email": "influenceur@example.com",
  "password": "motdepasse"
}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "token": "votre_token_ici",
  "influenceur": {...},
  "permissions": {
    "is_admin": false,
    "is_moderateur": false,
    "peut_creer_influenceurs": false,
    "peut_valider_prospects": false,
    "peut_payer_remises": false,
    "peut_voir_statistiques": true
  }
}
```

### POST /api/v1/auth/register/
**Public** - Inscription des nouveaux influenceurs
```json
{
  "nom": "Nom de l'influenceur",
  "email": "influenceur@example.com",
  "password": "motdepasse"
}
```

### GET /api/v1/auth/profile/
**Authentifié** - Récupérer le profil de l'utilisateur connecté

### POST /api/v1/auth/logout/
**Authentifié** - Déconnexion

### POST /api/v1/auth/change-password/
**Authentifié** - Changer le mot de passe
```json
{
  "current_password": "ancien_mot_de_passe",
  "new_password": "nouveau_mot_de_passe"
}
```

## Endpoints des Influenceurs

### GET /api/v1/influenceurs/
**Admin uniquement** - Lister tous les influenceurs

### POST /api/v1/influenceurs/
**Admin uniquement** - Créer un nouvel influenceur
```json
{
  "nom": "Nom de l'influenceur",
  "email": "influenceur@example.com",
  "password": "motdepasse",
  "role": "influenceur"
}
```

### GET /api/v1/influenceurs/{id}/
**Authentifié** - Détails d'un influenceur (propre profil ou admin)

### PUT/PATCH /api/v1/influenceurs/{id}/update/
**Authentifié** - Modifier un influenceur (propre profil ou admin)

### DELETE /api/v1/influenceurs/{id}/
**Admin uniquement** - Supprimer un influenceur

### GET /api/v1/influenceurs/{id}/dashboard/
**Authentifié** - Dashboard d'un influenceur (propre dashboard ou admin)
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
**Authentifié** - Prospects d'un influenceur (propres prospects ou admin)

### GET /api/v1/influenceurs/{id}/remises/
**Authentifié** - Remises d'un influenceur (propres remises ou admin)

## Endpoints des Prospects

### GET /api/v1/prospects/
**Authentifié** - Lister les prospects (propres prospects ou tous pour admin)

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
**Authentifié** - Prospects sans remise (propres prospects ou tous pour admin)

## Endpoints des Remises

### GET /api/v1/remises/
**Authentifié** - Lister les remises (propres remises ou toutes pour admin)

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
**Admin uniquement** - Calculer automatiquement les remises
```json
{
  "montant_par_prospect": 10.00
}
```

### POST /api/v1/remises/calculer-influenceur/{influenceur_id}/
**Admin uniquement** - Calculer remise pour un influenceur spécifique

### GET /api/v1/remises/statistiques/
**Admin uniquement** - Statistiques globales des remises

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
- `401` - Non authentifié
- `403` - Accès interdit (permissions insuffisantes)
- `404` - Ressource non trouvée
- `500` - Erreur serveur

## Permissions par Rôle

### Admin
- Accès complet à toutes les fonctionnalités
- Peut créer/supprimer des influenceurs
- Peut voir toutes les statistiques
- Peut valider tous les prospects
- Peut payer toutes les remises

### Influenceur
- Peut voir/modifier son propre profil
- Peut voir ses propres prospects et remises
- Peut voir son propre dashboard
- Permissions spécifiques selon les champs du modèle

### Modérateur
- Permissions intermédiaires selon configuration

## Exemples d'Utilisation

### Connexion et récupération du token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "influenceur@example.com", "password": "motdepasse"}'
```

### Utilisation du token pour accéder aux données
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Token votre_token_ici"
```

### Création d'un prospect via le formulaire d'affiliation
```bash
curl -X POST http://localhost:8000/affiliation/abc12345/ \
  -H "Content-Type: application/json" \
  -d '{"nom": "Nouveau Prospect", "email": "prospect@example.com"}'
``` 
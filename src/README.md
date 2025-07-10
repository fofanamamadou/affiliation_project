# Système d'Affiliation - API Backend

Un système d'affiliation complet avec authentification, permissions et API REST sécurisée.

## 🚀 Fonctionnalités

### Authentification et Sécurité
- ✅ Authentification par token JWT
- ✅ Système de permissions basé sur les rôles
- ✅ Protection CORS pour le frontend
- ✅ Validation des données et sécurité

### Gestion des Influenceurs
- ✅ CRUD complet des influenceurs
- ✅ Génération automatique de codes d'affiliation
- ✅ Système de rôles (admin, influenceur, modérateur)
- ✅ Permissions granulaires

### Gestion des Prospects
- ✅ Suivi des prospects par influenceur
- ✅ Validation des prospects
- ✅ Notifications automatiques par email
- ✅ Formulaire d'affiliation publique

### Gestion des Remises
- ✅ Calcul automatique des commissions
- ✅ Système de paiement avec justificatifs
- ✅ Statistiques et rapports
- ✅ Notifications de paiement

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip
- Git

### Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd affiliation/src
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

## 🔐 Authentification

### Connexion
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "influenceur@example.com", "password": "motdepasse"}'
```

### Utilisation du token
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Token votre_token_ici"
```

## 📋 Rôles et Permissions

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
- Permissions spécifiques selon configuration

### Modérateur
- Permissions intermédiaires selon configuration

## 🔗 Endpoints Principaux

### Authentification
- `POST /api/v1/auth/login/` - Connexion
- `POST /api/v1/auth/register/` - Inscription
- `GET /api/v1/auth/profile/` - Profil utilisateur
- `POST /api/v1/auth/logout/` - Déconnexion
- `POST /api/v1/auth/change-password/` - Changer mot de passe

### Influenceurs
- `GET /api/v1/influenceurs/` - Lister (admin)
- `POST /api/v1/influenceurs/` - Créer (admin)
- `GET /api/v1/influenceurs/{id}/` - Détails
- `PUT/PATCH /api/v1/influenceurs/{id}/update/` - Modifier
- `DELETE /api/v1/influenceurs/{id}/` - Supprimer (admin)
- `GET /api/v1/influenceurs/{id}/dashboard/` - Dashboard
- `GET /api/v1/influenceurs/{id}/prospects/` - Prospects
- `GET /api/v1/influenceurs/{id}/remises/` - Remises

### Prospects
- `GET /api/v1/prospects/` - Lister
- `POST /api/v1/prospects/` - Créer
- `POST /api/v1/prospects/{id}/valider/` - Valider
- `GET /api/v1/prospects/sans-remise/` - Sans remise

### Remises
- `GET /api/v1/remises/` - Lister
- `POST /api/v1/remises/` - Créer
- `POST /api/v1/remises/{id}/payer/` - Payer
- `POST /api/v1/remises/calculer-automatiques/` - Calculer (admin)
- `GET /api/v1/remises/statistiques/` - Statistiques (admin)

### Public
- `GET /affiliation/{code}/` - Formulaire d'affiliation
- `POST /affiliation/{code}/` - Soumission d'affiliation

## 🧪 Tests

### Tester l'API
```bash
python test_api.py
```

### Tests manuels avec curl
```bash
# Connexion
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Récupérer le profil
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Token votre_token"
```

## 📊 Documentation API

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Documentation complète**: `API_ENDPOINTS.md`

## 🔧 Configuration

### Variables d'environnement (optionnel)
Créer un fichier `.env` :
```env
DATABASE_NAME=affiliation_db
DATABASE_USER_NAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Configuration CORS
Les origines autorisées sont configurées dans `settings.py` :
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
]
```

## 🚀 Déploiement

### Production
1. Modifier `DEBUG = False` dans `settings.py`
2. Configurer une base de données PostgreSQL
3. Configurer les variables d'environnement
4. Collecter les fichiers statiques : `python manage.py collectstatic`
5. Utiliser Gunicorn ou uWSGI

### Docker (optionnel)
```bash
docker build -t affiliation-api .
docker run -p 8000:8000 affiliation-api
```

## 📝 Structure du Projet

```
src/
├── influenceur/          # App des influenceurs
│   ├── models.py        # Modèle Influenceur
│   ├── views.py         # Vues API
│   ├── auth.py          # Authentification
│   ├── auth_views.py    # Vues d'auth
│   ├── permissions.py   # Permissions
│   └── serializers.py   # Sérialiseurs
├── prospect/            # App des prospects
│   ├── models.py        # Modèle Prospect
│   ├── views.py         # Vues API
│   └── serializers.py   # Sérialiseurs
├── remise/              # App des remises
│   ├── models.py        # Modèle Remise
│   ├── views.py         # Vues API
│   └── serializers.py   # Sérialiseurs
├── src/                 # Configuration Django
│   ├── settings.py      # Paramètres
│   └── urls.py          # URLs principales
├── API_ENDPOINTS.md     # Documentation API
├── test_api.py          # Script de test
└── requirements.txt     # Dépendances
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Consulter la documentation API
2. Vérifier les logs du serveur
3. Tester avec le script `test_api.py`
4. Ouvrir une issue sur GitHub

---

**🎉 L'API est maintenant prête pour le développement du frontend !** 
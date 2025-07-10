# Système d'Affiliation - Django

Un système complet d'affiliation permettant aux influenceurs de générer des liens de parrainage, suivre leurs prospects et recevoir des primes.

## 🎯 Fonctionnalités

### ✅ Implémentées
- **Génération de liens d'affiliation uniques** : Chaque influenceur reçoit un code unique
- **Formulaire d'inscription** : Interface web pour les prospects
- **Notifications automatiques** : Emails envoyés aux influenceurs lors des inscriptions
- **Dashboard influenceur** : Statistiques et suivi des prospects
- **Calcul automatique des primes** : Système de commission basé sur les prospects confirmés
- **API REST complète** : Endpoints pour toutes les fonctionnalités
- **Interface admin** : Gestion des influenceurs, prospects et remises

### 🔄 Workflow
1. **Admin crée un influenceur** → Code d'affiliation généré automatiquement
2. **Influenceur partage son lien** : `/affiliation/<code>/`
3. **Prospect clique et s'inscrit** → Formulaire web avec validation
4. **Notification automatique** → Email envoyé à l'influenceur
5. **Admin valide les prospects** → Changement de statut
6. **Calcul automatique des primes** → Commission générée
7. **Admin marque comme payée** → Statut mis à jour

## 🚀 Installation

### Prérequis
- Python 3.8+
- PostgreSQL (ou SQLite pour le développement)
- pip

### Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd affiliation
```

2. **Créer un environnement virtuel**
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# ou
env\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
cd src
pip install -r ../requirements.txt
```

4. **Configuration de l'environnement**
```bash
# Copier le fichier d'exemple
cp env_example.txt .env
# Éditer .env avec vos paramètres
```

5. **Base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

## 📋 Configuration

### Variables d'environnement (.env)

```env
# Base de données
DATABASE_NAME=affiliation_db
DATABASE_USER_NAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Site
AFFILIATION_BASE_URL=https://tondomaine.com
DEFAULT_FROM_EMAIL=noreply@tondomaine.com
```

## 🔧 Utilisation

### API Endpoints

#### Influenceurs
- `GET /api/influenceurs/influenceurs/` - Lister tous les influenceurs
- `POST /api/influenceurs/influenceurs/` - Créer un influenceur
- `GET /api/influenceurs/influenceurs/<id>/` - Détails d'un influenceur
- `GET /api/influenceurs/influenceurs/<id>/dashboard/` - Dashboard influenceur
- `POST /api/influenceurs/influenceurs/login/` - Connexion influenceur

#### Prospects
- `GET /api/prospects/prospects/` - Lister tous les prospects
- `POST /api/prospects/prospects/<id>/valider/` - Valider un prospect
- `GET /affiliation/<code>/` - Formulaire d'inscription

#### Remises
- `GET /api/remises/remises/` - Lister toutes les remises
- `POST /api/remises/remises/<id>/payer/` - Marquer comme payée
- `POST /api/remises/remises/calculer-automatiques/` - Calculer toutes les remises
- `GET /api/remises/remises/statistiques/` - Statistiques des remises

### Commandes Django

```bash
# Calculer automatiquement les remises
python manage.py calculer_remises

# Avec un montant personnalisé
python manage.py calculer_remises --montant-par-prospect 15.0

# Mode test (sans effectuer les changements)
python manage.py calculer_remises --dry-run
```

## 📊 Workflow d'utilisation

### 1. Créer un influenceur (Admin)
```bash
# Via l'interface admin ou l'API
POST /api/influenceurs/influenceurs/
{
    "nom": "John Doe",
    "email": "john@example.com",
    "password": "motdepasse123"
}
```

### 2. L'influenceur reçoit son lien
L'email automatique contient le lien : `https://tondomaine.com/affiliation/abc12345/`

### 3. Prospect s'inscrit
Le prospect visite le lien et remplit le formulaire

### 4. Notification automatique
L'influenceur reçoit un email avec les détails du prospect

### 5. Admin valide les prospects
```bash
POST /api/prospects/prospects/1/valider/
```

### 6. Calcul automatique des primes
```bash
python manage.py calculer_remises
```

### 7. Marquer comme payée
```bash
POST /api/remises/remises/1/payer/
```

## 🎨 Interface utilisateur

### Formulaire d'affiliation
- Interface moderne et responsive
- Validation côté client et serveur
- Messages de succès/erreur
- Design adaptatif

### Dashboard influenceur
- Statistiques en temps réel
- Liste des prospects
- Historique des remises
- Liens d'affiliation

## 🔒 Sécurité

- Validation des données côté serveur
- Protection CSRF
- Hachage des mots de passe
- Validation des emails
- Gestion des erreurs

## 📈 Statistiques disponibles

- Nombre de prospects par influenceur
- Taux de conversion
- Montant total des remises
- Remises payées vs en attente
- Historique des paiements

## 🚀 Déploiement

### Production
1. Configurer une base de données PostgreSQL
2. Configurer un serveur SMTP
3. Définir `DEBUG=False`
4. Configurer un serveur web (Nginx + Gunicorn)
5. Configurer les variables d'environnement

### Variables de production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## 🆘 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation API : `/swagger/`
- Vérifier les logs Django

---

**Développé avec ❤️ en Django** 
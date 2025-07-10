from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Influenceur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('influenceur', 'Influenceur'),
        ('moderateur', 'Modérateur'),
    ]
    
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    code_affiliation = models.CharField(max_length=32, unique=True, editable=False)
    date_creation = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=128)  # à hasher avec set_password si login prévu
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influenceur')
    is_active = models.BooleanField(default=True)
    date_derniere_connexion = models.DateTimeField(null=True, blank=True)
    
    # Permissions spécifiques
    peut_creer_influenceurs = models.BooleanField(default=False)
    peut_valider_prospects = models.BooleanField(default=False)
    peut_payer_remises = models.BooleanField(default=False)
    peut_voir_statistiques = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code_affiliation:
            import uuid
            self.code_affiliation = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_affiliation_link(self):
        # Utilise le domaine du site (à configurer dans settings.py)
        base_url = getattr(settings, 'AFFILIATION_BASE_URL', 'http://localhost:8000')
        return f"{base_url}/affiliation/{self.code_affiliation}/"
    
    def has_permission(self, permission):
        """Vérifie si l'influenceur a une permission spécifique"""
        if self.role == 'admin':
            return True
        return getattr(self, f'peut_{permission}', False)
    
    def is_admin(self):
        """Vérifie si l'influenceur est admin"""
        return self.role == 'admin'
    
    def is_moderateur(self):
        """Vérifie si l'influenceur est modérateur"""
        return self.role == 'moderateur'
    
    def update_last_login(self):
        """Met à jour la date de dernière connexion"""
        from django.utils import timezone
        self.date_derniere_connexion = timezone.now()
        self.save(update_fields=['date_derniere_connexion'])
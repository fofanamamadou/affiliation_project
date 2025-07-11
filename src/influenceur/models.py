from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import uuid

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
    password = models.CharField(max_length=128)  # Mot de passe hashé
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influenceur')
    is_active = models.BooleanField(default=True)
    date_derniere_connexion = models.DateTimeField(null=True, blank=True)
    
    # Permissions spécifiques
    peut_creer_influenceurs = models.BooleanField(default=False)
    peut_valider_prospects = models.BooleanField(default=False)
    peut_payer_remises = models.BooleanField(default=False)
    peut_voir_statistiques = models.BooleanField(default=True)
    
    # Champs de sécurité
    date_derniere_modification_password = models.DateTimeField(null=True, blank=True)
    nombre_tentatives_connexion = models.IntegerField(default=0)
    date_derniere_tentative = models.DateTimeField(null=True, blank=True)
    bloque_jusqu_a = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code_affiliation:
            self.code_affiliation = uuid.uuid4().hex[:8]
        
        # Hash le mot de passe si il a changé
        if self.pk:  # Si c'est une mise à jour
            old_instance = Influenceur.objects.get(pk=self.pk)
            if old_instance.password != self.password:
                self.password = make_password(self.password)
                self.date_derniere_modification_password = timezone.now()
        else:  # Si c'est une création
            self.password = make_password(self.password)
            self.date_derniere_modification_password = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_affiliation_link(self):
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
        self.date_derniere_connexion = timezone.now()
        self.nombre_tentatives_connexion = 0  # Reset les tentatives
        self.save(update_fields=['date_derniere_connexion', 'nombre_tentatives_connexion'])
    
    def check_password(self, raw_password):
        """Vérifie le mot de passe"""
        return check_password(raw_password, self.password)
    
    def set_password(self, raw_password):
        """Définit un nouveau mot de passe hashé"""
        self.password = make_password(raw_password)
        self.date_derniere_modification_password = timezone.now()
        self.save(update_fields=['password', 'date_derniere_modification_password'])
    
    def is_locked(self):
        """Vérifie si le compte est bloqué"""
        if self.bloque_jusqu_a and timezone.now() < self.bloque_jusqu_a:
            return True
        return False
    
    def increment_login_attempts(self):
        """Incrémente le nombre de tentatives de connexion"""
        self.nombre_tentatives_connexion += 1
        self.date_derniere_tentative = timezone.now()
        
        # Bloquer après 5 tentatives échouées
        if self.nombre_tentatives_connexion >= 5:
            from datetime import timedelta
            self.bloque_jusqu_a = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['nombre_tentatives_connexion', 'date_derniere_tentative', 'bloque_jusqu_a'])
    
    def get_all_permissions(self):
        """Retourne toutes les permissions de l'influenceur"""
        return {
            'is_admin': self.is_admin(),
            'is_moderateur': self.is_moderateur(),
            'peut_creer_influenceurs': self.has_permission('creer_influenceurs'),
            'peut_valider_prospects': self.has_permission('valider_prospects'),
            'peut_payer_remises': self.has_permission('payer_remises'),
            'peut_voir_statistiques': self.has_permission('voir_statistiques'),
        }
    
    def can_login(self):
        """Vérifie si l'influenceur peut se connecter"""
        if not self.is_active:
            return False, "Compte désactivé"
        
        if self.is_locked():
            return False, f"Compte bloqué jusqu'à {self.bloque_jusqu_a.strftime('%H:%M')}"
        
        return True, "OK"
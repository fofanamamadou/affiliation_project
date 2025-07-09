from django.db import models
from django.utils import timezone
from influenceur.models import Influenceur
from remise.models import Remise

# Create your models here.
class Prospect(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
    ]
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    date_inscription = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    influenceur = models.ForeignKey(Influenceur, on_delete=models.CASCADE, related_name='prospects')
    remise = models.ForeignKey(Remise, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospects')

    def __str__(self):
        return self.nom
from django.db import models
from influenceur.models import Influenceur

# Create your models here.
class Remise(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée')
    ]
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    influenceur = models.ForeignKey(Influenceur, on_delete=models.CASCADE, related_name='remises')
    justificatif = models.ImageField(upload_to='justificatifs/', null=True, blank=True)  # Pour la capture du dépôt

    def __str__(self):
        return f"{self.influenceur.nom} - {self.montant} - {self.statut}"


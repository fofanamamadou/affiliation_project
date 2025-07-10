from django.db import models
from influenceur.models import Influenceur
from django.db.models import Sum
from decimal import Decimal

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
    date_creation = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, help_text="Description de la remise (ex: commission pour 5 prospects)")

    def __str__(self):
        return f"{self.influenceur.nom} - {self.montant}€ - {self.statut}"

    def marquer_comme_payee(self):
        """Marque la remise comme payée et enregistre la date de paiement"""
        from django.utils import timezone
        self.statut = 'payee'
        self.date_paiement = timezone.now()
        self.save()

    @classmethod
    def calculer_remise_automatique(cls, influenceur, montant_par_prospect=Decimal('10.00')):
        """
        Calcule et crée automatiquement une remise pour un influenceur
        basée sur ses prospects confirmés sans remise
        """
        from prospect.models import Prospect
        
        # Compter les prospects confirmés sans remise
        prospects_confirmes = Prospect.objects.filter(
            influenceur=influenceur,
            statut='confirme',
            remise__isnull=True
        )
        
        nb_prospects = prospects_confirmes.count()
        
        if nb_prospects > 0:
            montant_total = nb_prospects * montant_par_prospect
            
            # Créer la remise
            remise = cls.objects.create(
                influenceur=influenceur,
                montant=montant_total,
                description=f"Commission pour {nb_prospects} prospect(s) confirmé(s) à {montant_par_prospect}€ chacun"
            )
            
            # Associer la remise aux prospects
            prospects_confirmes.update(remise=remise)
            
            return remise
        
        return None

    @classmethod
    def generer_remises_pour_tous(cls, montant_par_prospect=Decimal('10.00')):
        """
        Génère automatiquement des remises pour tous les influenceurs
        ayant des prospects confirmés sans remise
        """
        influenceurs_avec_prospects = Influenceur.objects.filter(
            prospects__statut='confirme',
            prospects__remise__isnull=True
        ).distinct()
        
        remises_creees = []
        for influenceur in influenceurs_avec_prospects:
            remise = cls.calculer_remise_automatique(influenceur, montant_par_prospect)
            if remise:
                remises_creees.append(remise)
        
        return remises_creees


from django.contrib import admin
from .models import Remise

@admin.register(Remise)
class RemiseAdmin(admin.ModelAdmin):
    list_display = ('influenceur', 'montant', 'statut', 'date_creation', 'date_paiement')
    list_filter = ('statut', 'date_creation', 'date_paiement', 'influenceur')
    search_fields = ('influenceur__nom', 'description')
    readonly_fields = ('date_creation', 'date_paiement')
    
    def get_queryset(self, request):
        return super().get_queryset(request)

from django.contrib import admin
from .models import Prospect

@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'influenceur', 'statut', 'date_inscription')
    list_filter = ('statut', 'date_inscription', 'influenceur')
    search_fields = ('nom', 'email', 'influenceur__nom')
    readonly_fields = ('date_inscription',)
    
    def get_queryset(self, request):
        return super().get_queryset(request)

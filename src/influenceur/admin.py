from django.contrib import admin
from .models import Influenceur

@admin.register(Influenceur)
class InfluenceurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'code_affiliation', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('nom', 'email', 'code_affiliation')
    readonly_fields = ('code_affiliation', 'date_creation')
    
    def get_queryset(self, request):
        return super().get_queryset(request)

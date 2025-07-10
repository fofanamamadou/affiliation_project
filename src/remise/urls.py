from django.urls import path
from .views import (remise_view, remise_payer_view, calculer_remises_automatiques_view,
                    calculer_remise_influenceur_view, statistiques_remises_view)

urlpatterns = [
    path('remises/', remise_view, name='remise_view'),
    path('remises/<int:pk>/payer/', remise_payer_view, name='remise_payer'),
    path('remises/calculer-automatiques/', calculer_remises_automatiques_view, name='calculer_remises_automatiques'),
    path('remises/calculer-influenceur/<int:influenceur_id>/', calculer_remise_influenceur_view, name='calculer_remise_influenceur'),
    path('remises/statistiques/', statistiques_remises_view, name='statistiques_remises'),
]
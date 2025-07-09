from django.urls import path
from .views import (influenceur_view, influenceur_detail_view, influenceur_update_view,
                    influenceur_delete_view, influenceur_login_view, influenceur_dashboard_view,
                    influenceur_prospects_view, influenceur_remises_view)


urlpatterns = [
    path('influenceurs/', influenceur_view, name='influenceur_view'),
    path('influenceurs/<int:pk>/', influenceur_detail_view, name='influenceur_detail'),
    path('influenceurs/<int:pk>/update/', influenceur_update_view, name='influenceur_update'),
    path('influenceurs/<int:pk>/delete/', influenceur_delete_view, name='influenceur_delete'),
    path('influenceurs/login/', influenceur_login_view, name='influenceur_login'),
    path('influenceurs/<int:pk>/dashboard/', influenceur_dashboard_view, name='influenceur_dashboard'),
    path('influenceurs/<int:pk>/prospects/', influenceur_prospects_view, name='influenceur_prospects'),
    path('influenceurs/<int:pk>/remises/', influenceur_remises_view, name='influenceur_remises'),
]


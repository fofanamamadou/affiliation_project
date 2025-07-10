from django.urls import path
from .auth_views import (login_view, logout_view, profile_view, register_view, change_password_view)
from .views import (influenceur_view, influenceur_detail_view, influenceur_update_view,
                    influenceur_delete_view, influenceur_dashboard_view, influenceur_prospects_view, 
                    influenceur_remises_view)

urlpatterns = [
    # URLs d'authentification
    path('auth/login/', login_view, name='auth_login'),
    path('auth/logout/', logout_view, name='auth_logout'),
    path('auth/profile/', profile_view, name='auth_profile'),
    path('auth/register/', register_view, name='auth_register'),
    path('auth/change-password/', change_password_view, name='auth_change_password'),
    
    # URLs des influenceurs (CRUD)
    path('influenceurs/', influenceur_view, name='influenceur_view'),
    path('influenceurs/<int:pk>/', influenceur_detail_view, name='influenceur_detail'),
    path('influenceurs/<int:pk>/update/', influenceur_update_view, name='influenceur_update'),
    path('influenceurs/<int:pk>/delete/', influenceur_delete_view, name='influenceur_delete'),
    path('influenceurs/<int:pk>/dashboard/', influenceur_dashboard_view, name='influenceur_dashboard'),
    path('influenceurs/<int:pk>/prospects/', influenceur_prospects_view, name='influenceur_prospects'),
    path('influenceurs/<int:pk>/remises/', influenceur_remises_view, name='influenceur_remises'),
]


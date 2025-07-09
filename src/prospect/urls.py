from django.urls import path
from .views import prospect_view, prospect_valider_view, prospects_sans_remise_view

urlpatterns = [
    path('prospects/', prospect_view, name='prospect_view'),
    path('prospects/<int:pk>/valider/', prospect_valider_view, name='prospect_valider'),
    path('prospects/sans-remise/', prospects_sans_remise_view, name='prospects_sans_remise'),
]
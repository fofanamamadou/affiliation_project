from django.urls import path
from .views import remise_view, remise_payer_view

urlpatterns = [
    path('remises/', remise_view, name='remise_view'),
    path('remises/<int:pk>/payer/', remise_payer_view, name='remise_payer'),
]
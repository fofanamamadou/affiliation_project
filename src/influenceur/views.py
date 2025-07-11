from django.contrib.auth.hashers import check_password
from .serializers import InfluenceurSerializer
from prospect.models import Prospect
from prospect.serializers import ProspectSerializers
from remise.models import Remise
from remise.serializers import RemiseSerializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Influenceur
from .permissions import (
    IsAdminUser, IsInfluenceurOrAdmin, CanCreateInfluenceurs,
    CanValidateProspects, CanPayRemises, CanViewStatistics, IsOwnerOrAdmin
)
from .auth import get_influenceur_from_user
from .email_service import EmailService
from django.db import models

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def influenceur_view(request):
    """
    Vue API pour lister tous les influenceurs (GET) ou en créer un (POST).
    Seuls les admins peuvent accéder à cette vue.
    """
    if request.method == 'GET':
        influenceurs = Influenceur.objects.all()
        serializer = InfluenceurSerializer(influenceurs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = InfluenceurSerializer(data=request.data)
        if serializer.is_valid():
            # On sauvegarde et on récupère l'instance créée
            influenceur = serializer.save()

            # Envoi des emails avec le nouveau service
            try:
                # Email d'affiliation avec le lien
                EmailService.send_affiliation_link(influenceur)
                
                # Email de bienvenue
                EmailService.send_welcome_email(influenceur)
                
            except Exception as e:
                print(f"Erreur lors de l'envoi des emails : {e}")
                # On continue même si l'email échoue
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def influenceur_detail_view(request, pk):
    """
    Vue API pour obtenir les détails d'un influenceur.
    L'influenceur peut voir ses propres détails, les admins peuvent voir tous.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    
    # Vérifier les permissions
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and current_influenceur.id != influenceur.id:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = InfluenceurSerializer(influenceur)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsInfluenceurOrAdmin])
def influenceur_update_view(request, pk):
    """
    Vue API pour mettre à jour un influenceur existant.
    L'influenceur peut modifier ses propres infos, les admins peuvent modifier tous.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    
    # Vérifier les permissions
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and current_influenceur.id != influenceur.id:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = InfluenceurSerializer(influenceur, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def influenceur_delete_view(request, pk):
    """
    Vue API pour supprimer un influenceur existant.
    Seuls les admins peuvent supprimer des influenceurs.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    influenceur.delete()
    return Response({'detail': 'Influenceur supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def influenceur_dashboard_view(request, pk):
    """
    Vue API pour afficher le tableau de bord d'un influenceur.
    L'influenceur peut voir son propre dashboard, les admins peuvent voir tous.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    
    # Vérifier les permissions
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and current_influenceur.id != influenceur.id:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    prospects = Prospect.objects.filter(influenceur=influenceur)
    prospects_confirmes = prospects.filter(statut='confirme')
    remises = Remise.objects.filter(influenceur=influenceur)
    montant_total_remises = remises.filter(statut='payee').aggregate(models.Sum('montant'))['montant__sum'] or 0

    prospects_serializer = ProspectSerializers(prospects, many=True)
    remises_serializer = RemiseSerializers(remises, many=True)

    dashboard_data = {
        'influenceur': influenceur.nom,
        'code_affiliation': influenceur.code_affiliation,
        'nb_prospects': prospects.count(),
        'nb_prospects_confirmes': prospects_confirmes.count(),
        'montant_total_remises_payees': montant_total_remises,
        'prospects': prospects_serializer.data,
        'remises': remises_serializer.data,
    }
    return Response(dashboard_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def influenceur_prospects_view(request, pk):
    """
    Vue API pour lister tous les prospects d'un influenceur donné.
    L'influenceur peut voir ses propres prospects, les admins peuvent voir tous.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    
    # Vérifier les permissions
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and current_influenceur.id != influenceur.id:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    prospects = Prospect.objects.filter(influenceur=influenceur)
    serializer = ProspectSerializers(prospects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def influenceur_remises_view(request, pk):
    """
    Vue API pour lister toutes les remises d'un influenceur donné.
    L'influenceur peut voir ses propres remises, les admins peuvent voir tous.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    
    # Vérifier les permissions
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and current_influenceur.id != influenceur.id:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    remises = Remise.objects.filter(influenceur=influenceur)
    serializer = RemiseSerializers(remises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
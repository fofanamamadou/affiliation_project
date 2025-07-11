from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Remise
from .serializers import RemiseSerializers
from influenceur.permissions import CanPayRemises, IsInfluenceurOrAdmin, IsAdminUser
from influenceur.auth import get_influenceur_from_user
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from decimal import Decimal

@api_view(['GET'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsInfluenceurOrAdmin])
def remise_view(request):
    """
    Vue API pour lister toutes les remises (GET) .
    Les influenceurs voient leurs propres remises, les admins voient toutes.
    """
    if request.method == 'GET':
        # Filtrer par influenceur si ce n'est pas un admin
        current_influenceur = get_influenceur_from_user(request.user)
        if not request.user.is_superuser and current_influenceur:
            remises = Remise.objects.filter(influenceur=current_influenceur)
        else:
            remises = Remise.objects.all()
            
        serializer = RemiseSerializers(remises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([CanPayRemises])
def remise_payer_view(request, pk):
    """
    Vue API pour marquer une remise comme payée et uploader un justificatif.
    Seuls les utilisateurs avec permission de paiement peuvent accéder.
    """
    remise = get_object_or_404(Remise, pk=pk)
    
    # Vérifier les permissions pour cette remise spécifique
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and remise.influenceur != current_influenceur:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    if remise.statut == 'payee':
        return Response({'detail': 'Cette remise est déjà marquée comme payée.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # On récupère le justificatif s'il est envoyé
    justificatif = request.FILES.get('justificatif')
    remise.marquer_comme_payee()
    
    if justificatif:
        remise.justificatif = justificatif
        remise.save()
    
    # Notification de paiement à l'influenceur
    try:
        send_mail(
            subject=f"✅ Remise payée !",
            message=f"""
            Bonjour {remise.influenceur.nom},
            
            ✅ Votre remise de {remise.montant}€ a été payée !
            
            📋 Détails :
            - Montant : {remise.montant}€
            - Date de paiement : {remise.date_paiement.strftime('%d/%m/%Y à %H:%M')}
            - Description : {remise.description}
            
            💳 Le montant a été transféré sur votre compte.
            
            Merci pour votre contribution !
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[remise.influenceur.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")
    
    serializer = RemiseSerializers(remise)
    return Response({'detail': 'Remise marquée comme payée.', 'remise': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculer_remises_automatiques_view(request):
    """
    Vue API pour calculer automatiquement les remises pour tous les influenceurs.
    Seuls les admins peuvent déclencher ce calcul.
    """
    from decimal import Decimal
    
    montant_par_prospect = Decimal(request.data.get('montant_par_prospect', '10.00'))
    
    try:
        remises_creees = Remise.generer_remises_pour_tous(montant_par_prospect)
        
        if remises_creees:
            serializer = RemiseSerializers(remises_creees, many=True)
            return Response({
                'detail': f'{len(remises_creees)} remise(s) créée(s) automatiquement.',
                'remises': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'detail': 'Aucune remise à créer. Tous les prospects confirmés ont déjà une remise.'
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'Erreur lors du calcul des remises : {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculer_remise_influenceur_view(request, influenceur_id):
    """
    Vue API pour calculer une remise pour un influenceur spécifique.
    Seuls les admins peuvent déclencher ce calcul.
    """
    from influenceur.models import Influenceur
    from decimal import Decimal
    
    influenceur = get_object_or_404(Influenceur, pk=influenceur_id)
    montant_par_prospect = Decimal(request.data.get('montant_par_prospect', '10.00'))
    
    try:
        remise = Remise.calculer_remise_automatique(influenceur, montant_par_prospect)
        
        if remise:
            serializer = RemiseSerializers(remise)
            return Response({
                'detail': 'Remise créée automatiquement.',
                'remise': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'detail': 'Aucun prospect confirmé sans remise pour cet influenceur.'
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'Erreur lors du calcul de la remise : {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def statistiques_remises_view(request):
    """
    Vue API pour obtenir des statistiques sur les remises.
    Seuls les admins peuvent voir les statistiques globales.
    """
    total_remises = Remise.objects.count()
    remises_payees = Remise.objects.filter(statut='payee').count()
    remises_en_attente = Remise.objects.filter(statut='en_attente').count()
    
    montant_total = Remise.objects.aggregate(
        total=models.Sum('montant')
    )['total'] or 0
    
    montant_paye = Remise.objects.filter(statut='payee').aggregate(
        total=models.Sum('montant')
    )['total'] or 0
    
    montant_en_attente = Remise.objects.filter(statut='en_attente').aggregate(
        total=models.Sum('montant')
    )['total'] or 0
    
    stats = {
        'total_remises': total_remises,
        'remises_payees': remises_payees,
        'remises_en_attente': remises_en_attente,
        'montant_total': float(montant_total),
        'montant_paye': float(montant_paye),
        'montant_en_attente': float(montant_en_attente),
    }
    
    return Response(stats, status=status.HTTP_200_OK)

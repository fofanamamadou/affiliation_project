from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Prospect
from .serializers import ProspectSerializers
from influenceur.models import Influenceur
from influenceur.permissions import CanValidateProspects, IsInfluenceurOrAdmin
from influenceur.auth import get_influenceur_from_user
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def prospect_view(request):
    """
    Vue API pour lister tous les prospects (GET)
    Seuls les influenceurs connectés et admins peuvent accéder.
    """
    if request.method == 'GET':
        # Filtrer par influenceur si ce n'est pas un admin
        current_influenceur = get_influenceur_from_user(request.user)
        if not request.user.is_superuser and current_influenceur:
            prospects = Prospect.objects.filter(influenceur=current_influenceur)
        else:
            prospects = Prospect.objects.all()
            
        serializer = ProspectSerializers(prospects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([CanValidateProspects])
def prospect_valider_view(request, pk):
    """
    Vue API pour valider un prospect (passer son statut à 'confirme').
    Seuls les utilisateurs avec permission de validation peuvent accéder.
    """
    prospect = get_object_or_404(Prospect, pk=pk)
    
    # Vérifier les permissions pour ce prospect spécifique
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and prospect.influenceur != current_influenceur:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    if prospect.statut == 'confirme':
        return Response({'detail': 'Ce prospect est déjà confirmé.'}, status=status.HTTP_400_BAD_REQUEST)
    prospect.statut = 'confirme'
    prospect.save()
    serializer = ProspectSerializers(prospect)
    return Response({'detail': 'Prospect validé avec succès.', 'prospect': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def prospects_sans_remise_view(request):
    """
    Vue API pour lister tous les prospects sans remise associée.
    Seuls les admins peuvent voir tous les prospects sans remise.
    """
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur:
        prospects = Prospect.objects.filter(remise__isnull=True, influenceur=current_influenceur)
    else:
        prospects = Prospect.objects.filter(remise__isnull=True)
        
    serializer = ProspectSerializers(prospects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def affiliation_form_view(request, code_affiliation):
    """
    Vue pour afficher le formulaire d'affiliation et traiter les soumissions.
    Cette vue est publique (pas d'authentification requise).
    """
    try:
        influenceur = Influenceur.objects.get(code_affiliation=code_affiliation, is_active=True)
    except Influenceur.DoesNotExist:
        return HttpResponse('<h1>Code d\'affiliation invalide</h1>', status=404)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom = data.get('nom')
            telephone = data.get('telephone')
            email = data.get('email')

            if not nom or not email:
                return JsonResponse({'error': 'Nom et Telephone requis'}, status=400)
            
            # Créer le prospect
            prospect = Prospect.objects.create(
                nom=nom,
                telephone=telephone,
                email=email,
                influenceur=influenceur
            )
            
            
            return JsonResponse({
                'success': True,
                'message': 'Inscription réussie !',
                'prospect_id': prospect.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

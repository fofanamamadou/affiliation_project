from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Influenceur
from .auth import authenticate_influenceur, get_influenceur_from_user
from .serializers import InfluenceurSerializer
from .permissions import IsInfluenceurOrAdmin, IsOwnerOrAdmin
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Vue de connexion pour les influenceurs
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email et mot de passe requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentifier l'influenceur
        auth_result = authenticate_influenceur(email, password)
        
        if auth_result:
            influenceur = auth_result['influenceur']
            token = auth_result['token']
            
            serializer = InfluenceurSerializer(influenceur)
            
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'token': token,
                'influenceur': serializer.data,
                'permissions': {
                    'is_admin': influenceur.is_admin(),
                    'is_moderateur': influenceur.is_moderateur(),
                    'peut_creer_influenceurs': influenceur.has_permission('creer_influenceurs'),
                    'peut_valider_prospects': influenceur.has_permission('valider_prospects'),
                    'peut_payer_remises': influenceur.has_permission('payer_remises'),
                    'peut_voir_statistiques': influenceur.has_permission('voir_statistiques'),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Email ou mot de passe incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la connexion: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsInfluenceurOrAdmin])
def logout_view(request):
    """
    Vue de déconnexion
    """
    try:
        # Supprimer le token d'authentification
        if hasattr(request, 'auth'):
            request.auth.delete()
        
        return Response({
            'success': True,
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la déconnexion: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def profile_view(request):
    """
    Vue pour récupérer le profil de l'utilisateur connecté
    """
    try:
        influenceur = get_influenceur_from_user(request.user)
        
        if not influenceur:
            return Response({
                'error': 'Influenceur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InfluenceurSerializer(influenceur)
        
        return Response({
            'influenceur': serializer.data,
            'permissions': {
                'is_admin': influenceur.is_admin(),
                'is_moderateur': influenceur.is_moderateur(),
                'peut_creer_influenceurs': influenceur.has_permission('creer_influenceurs'),
                'peut_valider_prospects': influenceur.has_permission('valider_prospects'),
                'peut_payer_remises': influenceur.has_permission('payer_remises'),
                'peut_voir_statistiques': influenceur.has_permission('voir_statistiques'),
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la récupération du profil: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Vue d'inscription pour les nouveaux influenceurs
    """
    try:
        data = json.loads(request.body)
        nom = data.get('nom')
        email = data.get('email')
        password = data.get('password')
        
        if not nom or not email or not password:
            return Response({
                'error': 'Nom, email et mot de passe requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier si l'email existe déjà
        if Influenceur.objects.filter(email=email).exists():
            return Response({
                'error': 'Un influenceur avec cet email existe déjà'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer le nouvel influenceur
        influenceur = Influenceur.objects.create(
            nom=nom,
            email=email,
            password=password,
            role='influenceur'  # Par défaut
        )
        
        # Authentifier automatiquement
        auth_result = authenticate_influenceur(email, password)
        
        if auth_result:
            token = auth_result['token']
            serializer = InfluenceurSerializer(influenceur)
            
            return Response({
                'success': True,
                'message': 'Inscription réussie',
                'token': token,
                'influenceur': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Erreur lors de l\'authentification'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Erreur lors de l\'inscription: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsInfluenceurOrAdmin])
def change_password_view(request):
    """
    Vue pour changer le mot de passe
    """
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return Response({
                'error': 'Ancien et nouveau mot de passe requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        influenceur = get_influenceur_from_user(request.user)
        
        if not influenceur:
            return Response({
                'error': 'Influenceur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier l'ancien mot de passe
        if influenceur.password != current_password:
            return Response({
                'error': 'Ancien mot de passe incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Changer le mot de passe
        influenceur.password = new_password
        influenceur.save()
        
        return Response({
            'success': True,
            'message': 'Mot de passe modifié avec succès'
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Erreur lors du changement de mot de passe: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
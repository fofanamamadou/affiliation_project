from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Influenceur
from .jwt_auth import JWTAuthService
from .serializers import InfluenceurSerializer
from .permissions import IsInfluenceurOrAdmin, IsOwnerOrAdmin
import json
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Vue de connexion pour les superusers et influenceurs
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email et mot de passe requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentifier avec JWT (superuser ou influenceur)
        auth_result = JWTAuthService.authenticate_user(email, password)
        
        if auth_result['success']:
            access_token = auth_result['access_token']
            refresh_token = auth_result['refresh_token']
            user_type = auth_result['user_type']
            permissions = auth_result['permissions']
            
            response_data = {
                'success': True,
                'message': 'Connexion réussie',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_type': user_type,
                'permissions': permissions,
                'token_type': 'Bearer',
                'expires_in': 86400  # 24 heures en secondes
            }
            
            # Ajouter les données spécifiques selon le type d'utilisateur
            if user_type == 'superuser':
                response_data['user'] = {
                    'id': auth_result['user'].id,
                    'username': auth_result['user'].username,
                    'email': auth_result['user'].email,
                    'first_name': auth_result['user'].first_name,
                    'last_name': auth_result['user'].last_name,
                    'is_superuser': True
                }
            else:  # influenceur
                influenceur = auth_result['influenceur']
                serializer = InfluenceurSerializer(influenceur)
                response_data['influenceur'] = serializer.data
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': auth_result['error']
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {str(e)}")
        return Response({
            'error': 'Erreur lors de la connexion'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Vue pour rafraîchir un token JWT
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Rafraîchir le token
        result = JWTAuthService.refresh_token(refresh_token)
        
        if result['success']:
            return Response({
                'success': True,
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'token_type': 'Bearer',
                'expires_in': 86400
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error']
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Erreur lors du refresh token: {str(e)}")
        return Response({
            'error': 'Erreur lors du rafraîchissement du token'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Vue de déconnexion
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Déconnecter
        result = JWTAuthService.logout(refresh_token)
        
        if result['success']:
            return Response({
                'success': True,
                'message': result['message']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {str(e)}")
        return Response({
            'error': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Vue pour récupérer le profil de l'utilisateur connecté
    """
    try:
        # Récupérer l'utilisateur depuis le token JWT
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_data = JWTAuthService.get_user_from_token(token)
        else:
            return Response({
                'error': 'Token d\'authentification requis'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user_data:
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        user_type = user_data['user_type']
        permissions = user_data['permissions']
        
        response_data = {
            'user_type': user_type,
            'permissions': permissions
        }
        
        if user_type == 'superuser':
            user = user_data['user']
            response_data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_superuser': True,
                'date_joined': user.date_joined,
                'last_login': user.last_login
            }
        else:  # influenceur
            influenceur = user_data['influenceur']
            serializer = InfluenceurSerializer(influenceur)
            response_data['influenceur'] = serializer.data
            response_data['last_login'] = influenceur.date_derniere_connexion
            response_data['account_status'] = {
                'is_active': influenceur.is_active,
                'is_locked': influenceur.is_locked(),
                'login_attempts': influenceur.nombre_tentatives_connexion
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du profil: {str(e)}")
        return Response({
            'error': 'Erreur lors de la récupération du profil'
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
            password=password,  # Sera hashé automatiquement
            role='influenceur'  # Par défaut
        )
        
        # Authentifier automatiquement
        auth_result = JWTAuthService.authenticate_user(email, password)
        
        if auth_result['success']:
            access_token = auth_result['access_token']
            refresh_token = auth_result['refresh_token']
            serializer = InfluenceurSerializer(influenceur)
            
            return Response({
                'success': True,
                'message': 'Inscription réussie',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'influenceur': serializer.data,
                'permissions': influenceur.get_all_permissions(),
                'token_type': 'Bearer',
                'expires_in': 86400
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
        logger.error(f"Erreur lors de l'inscription: {str(e)}")
        return Response({
            'error': 'Erreur lors de l\'inscription'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
        
        # Récupérer l'utilisateur depuis le token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_data = JWTAuthService.get_user_from_token(token)
        else:
            return Response({
                'error': 'Token d\'authentification requis'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user_data:
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        user_type = user_data['user_type']
        
        if user_type == 'superuser':
            # Changer le mot de passe du superuser
            user = user_data['user']
            if not user.check_password(current_password):
                return Response({
                    'error': 'Ancien mot de passe incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
        else:
            # Changer le mot de passe de l'influenceur
            influenceur = user_data['influenceur']
            if not influenceur.check_password(current_password):
                return Response({
                    'error': 'Ancien mot de passe incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            influenceur.set_password(new_password)
        
        return Response({
            'success': True,
            'message': 'Mot de passe modifié avec succès'
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Données JSON invalides'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Erreur lors du changement de mot de passe: {str(e)}")
        return Response({
            'error': 'Erreur lors du changement de mot de passe'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

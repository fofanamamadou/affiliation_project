from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Influenceur
import logging

logger = logging.getLogger(__name__)

class JWTAuthService:
    """
    Service d'authentification JWT pour les influenceurs et superusers
    """
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authentifie un utilisateur (influenceur ou superuser) et retourne les tokens JWT
        """
        try:
            # D'abord, essayer d'authentifier comme superuser Django par username
            user = authenticate(username=email, password=password)
            
            if user and user.is_superuser:
                # C'est un superuser Django
                return JWTAuthService._authenticate_superuser(user)
            elif user:
                # C'est un utilisateur Django normal (non-superuser)
                return {
                    'success': False,
                    'error': 'Accès non autorisé. Seuls les administrateurs peuvent se connecter.'
                }
            
            # Si l'authentification par username a échoué, essayer par email
            # Chercher un superuser avec cet email
            try:
                superuser = User.objects.get(email=email, is_superuser=True)
                user = authenticate(username=superuser.username, password=password)
                
                if user and user.is_superuser:
                    return JWTAuthService._authenticate_superuser(user)
            except User.DoesNotExist:
                pass
            
            # Enfin, essayer comme influenceur
            return JWTAuthService._authenticate_influenceur(email, password)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification: {str(e)}")
            return {
                'success': False,
                'error': 'Erreur lors de l\'authentification'
            }
    
    @staticmethod
    def _authenticate_superuser(user):
        """
        Authentifie un superuser Django
        """
        try:
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return {
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user,
                'user_type': 'superuser',
                'permissions': {
                    'is_admin': True,
                    'is_moderateur': False,
                    'peut_creer_influenceurs': True,
                    'peut_valider_prospects': True,
                    'peut_payer_remises': True,
                    'peut_voir_statistiques': True,
                    'peut_gerer_systeme': True
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification superuser: {str(e)}")
            return {
                'success': False,
                'error': 'Erreur lors de l\'authentification'
            }
    
    @staticmethod
    def _authenticate_influenceur(email, password):
        """
        Authentifie un influenceur
        """
        try:
            # Vérifier si l'influenceur existe
            influenceur = Influenceur.objects.get(email=email)
            
            # Vérifier si le compte peut se connecter
            can_login, message = influenceur.can_login()
            if not can_login:
                influenceur.increment_login_attempts()
                return {
                    'success': False,
                    'error': message
                }
            
            # Vérifier le mot de passe
            if not influenceur.check_password(password):
                influenceur.increment_login_attempts()
                return {
                    'success': False,
                    'error': 'Email ou mot de passe incorrect'
                }
            
            # Créer ou récupérer l'utilisateur Django
            user, created = User.objects.get_or_create(
                username=influenceur.email,
                defaults={
                    'email': influenceur.email,
                    'first_name': influenceur.nom.split()[0] if influenceur.nom else '',
                    'last_name': ' '.join(influenceur.nom.split()[1:]) if len(influenceur.nom.split()) > 1 else '',
                    'is_active': influenceur.is_active,
                }
            )
            
            # Mettre à jour les informations utilisateur si nécessaire
            if not created:
                user.first_name = influenceur.nom.split()[0] if influenceur.nom else ''
                user.last_name = ' '.join(influenceur.nom.split()[1:]) if len(influenceur.nom.split()) > 1 else ''
                user.is_active = influenceur.is_active
                user.save()
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Mettre à jour la dernière connexion
            influenceur.update_last_login()
            
            return {
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'influenceur': influenceur,
                'user': user,
                'user_type': 'influenceur',
                'permissions': influenceur.get_all_permissions()
            }
            
        except Influenceur.DoesNotExist:
            return {
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification influenceur: {str(e)}")
            return {
                'success': False,
                'error': 'Erreur lors de l\'authentification'
            }
    
    @staticmethod
    def refresh_token(refresh_token):
        """
        Rafraîchit un token JWT
        """
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return {
                'success': True,
                'access_token': access_token,
                'refresh_token': str(refresh)
            }
        except TokenError as e:
            logger.error(f"Erreur lors du refresh token: {str(e)}")
            return {
                'success': False,
                'error': 'Token de rafraîchissement invalide'
            }
        except Exception as e:
            logger.error(f"Erreur lors du refresh token: {str(e)}")
            return {
                'success': False,
                'error': 'Erreur lors du rafraîchissement du token'
            }
    
    @staticmethod
    def logout(refresh_token):
        """
        Déconnecte un utilisateur en invalidant le refresh token
        """
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            
            return {
                'success': True,
                'message': 'Déconnexion réussie'
            }
        except TokenError as e:
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            return {
                'success': False,
                'error': 'Token invalide'
            }
        except Exception as e:
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            return {
                'success': False,
                'error': 'Erreur lors de la déconnexion'
            }
    
    @staticmethod
    def get_user_from_token(token):
        """
        Récupère l'utilisateur (superuser ou influenceur) à partir d'un token JWT
        """
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            user = User.objects.get(id=user_id)
            
            # Vérifier si c'est un superuser
            if user.is_superuser:
                return {
                    'user': user,
                    'user_type': 'superuser',
                    'permissions': {
                        'is_admin': True,
                        'is_moderateur': False,
                        'peut_creer_influenceurs': True,
                        'peut_valider_prospects': True,
                        'peut_payer_remises': True,
                        'peut_voir_statistiques': True,
                        'peut_gerer_systeme': True
                    }
                }
            else:
                # C'est un influenceur
                try:
                    influenceur = Influenceur.objects.get(email=user.email)
                    return {
                        'user': user,
                        'influenceur': influenceur,
                        'user_type': 'influenceur',
                        'permissions': influenceur.get_all_permissions()
                    }
                except Influenceur.DoesNotExist:
                    return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
            return None
    
    @staticmethod
    def validate_token(token):
        """
        Valide un token JWT
        """
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            return True
        except Exception:
            return False 
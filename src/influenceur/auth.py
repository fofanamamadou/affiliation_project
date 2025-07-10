from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Influenceur
from django.utils import timezone

class InfluenceurTokenAuthentication(TokenAuthentication):
    """
    Authentification personnalisée pour les influenceurs avec tokens
    """
    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
            if not token.user.is_active:
                raise AuthenticationFailed('Utilisateur inactif.')
            
            # Vérifier si l'utilisateur a un influenceur associé
            try:
                influenceur = Influenceur.objects.get(email=token.user.email)
                if not influenceur.is_active:
                    raise AuthenticationFailed('Influenceur inactif.')
                
                # Mettre à jour la dernière connexion
                influenceur.update_last_login()
                
                return (token.user, token)
            except Influenceur.DoesNotExist:
                raise AuthenticationFailed('Influenceur non trouvé.')
                
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Token invalide.')

def create_influenceur_user(influenceur):
    """
    Crée un utilisateur Django pour un influenceur
    """
    # Créer l'utilisateur Django
    user, created = User.objects.get_or_create(
        username=influenceur.email,
        defaults={
            'email': influenceur.email,
            'first_name': influenceur.nom.split()[0] if influenceur.nom else '',
            'last_name': ' '.join(influenceur.nom.split()[1:]) if len(influenceur.nom.split()) > 1 else '',
            'is_active': influenceur.is_active,
        }
    )
    
    if created:
        # Définir le mot de passe
        user.set_password(influenceur.password)
        user.save()
    
    # Créer le token d'authentification
    token, created = Token.objects.get_or_create(user=user)
    
    return user, token

def authenticate_influenceur(email, password):
    """
    Authentifie un influenceur avec email et mot de passe
    """
    try:
        influenceur = Influenceur.objects.get(email=email, is_active=True)
        
        # Vérifier le mot de passe
        if influenceur.password == password:  # Pour la simplicité, en production utiliser hashing
            # Créer ou récupérer l'utilisateur Django
            user, token = create_influenceur_user(influenceur)
            
            # Mettre à jour la dernière connexion
            influenceur.update_last_login()
            
            return {
                'user': user,
                'token': token.key,
                'influenceur': influenceur
            }
        else:
            return None
            
    except Influenceur.DoesNotExist:
        return None

def get_influenceur_from_user(user):
    """
    Récupère l'influenceur associé à un utilisateur Django
    """
    try:
        return Influenceur.objects.get(email=user.email)
    except Influenceur.DoesNotExist:
        return None 
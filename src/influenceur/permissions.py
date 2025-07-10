from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Si c'est un influenceur connecté
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.is_admin()
        
        # Si c'est un superutilisateur Django
        return request.user.is_superuser

class IsInfluenceurOrAdmin(BasePermission):
    """
    Permission pour les influenceurs ou admins
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Superutilisateur a tous les droits
        if request.user.is_superuser:
            return True
        
        # Vérifier si c'est un influenceur
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.is_active
        
        return False

class CanCreateInfluenceurs(BasePermission):
    """
    Permission pour créer des influenceurs
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.has_permission('creer_influenceurs')
        
        return False

class CanValidateProspects(BasePermission):
    """
    Permission pour valider des prospects
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.has_permission('valider_prospects')
        
        return False

class CanPayRemises(BasePermission):
    """
    Permission pour payer des remises
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.has_permission('payer_remises')
        
        return False

class CanViewStatistics(BasePermission):
    """
    Permission pour voir les statistiques
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'influenceur'):
            return request.user.influenceur.has_permission('voir_statistiques')
        
        return False

class IsOwnerOrAdmin(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est propriétaire de la ressource ou admin
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'influenceur'):
            # Admin peut tout voir
            if request.user.influenceur.is_admin():
                return True
            
            # Vérifier si l'objet appartient à l'influenceur
            if hasattr(obj, 'influenceur'):
                return obj.influenceur == request.user.influenceur
            
            # Pour les objets qui ont directement un influenceur
            if hasattr(obj, 'influenceur'):
                return obj.influenceur == request.user.influenceur
        
        return False 
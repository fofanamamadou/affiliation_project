from django.contrib.auth.hashers import check_password
from .serializers import InfluenceurSerializer
from prospect.models import Prospect
from prospect.serializers import ProspectSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Influenceur
from remise.models import Remise
from remise.serializers import RemiseSerializers
# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Influenceur
from .serializers import InfluenceurSerializer

@api_view(['GET', 'POST'])
def influenceur_view(request):
    """
    Vue API pour lister tous les influenceurs (GET) ou en créer un (POST).
    Après création, envoie automatiquement le lien d'affiliation par email à l'influenceur.
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

            # Envoi du mail avec le lien d'affiliation
            send_mail(
                subject="Votre lien d'affiliation",
                message=f"Bonjour {influenceur.nom}, voici votre lien d'affiliation : {influenceur.get_affiliation_link()}",
                from_email="noreply@tondomaine.com",
                recipient_list=[getattr(influenceur, 'email', None)],  # Assure-toi que le champ email existe
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def influenceur_detail_view(request, pk):
    influenceur = get_object_or_404(Influenceur, pk=pk)
    serializer = InfluenceurSerializer(influenceur)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def influenceur_update_view(request, pk):
    """
    Vue API pour mettre à jour un influenceur existant.
    - PUT : remplace toutes les infos de l'influenceur.
    - PATCH : modifie seulement les champs fournis.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    serializer = InfluenceurSerializer(influenceur, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def influenceur_delete_view(request, pk):
    """
    Vue API pour supprimer un influenceur existant.
    - DELETE : supprime l'influenceur d'identifiant <pk>.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    influenceur.delete()
    return Response({'detail': 'Influenceur supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def influenceur_login_view(request):
    """
    Vue API pour connecter un influenceur.
    - POST : attend 'nom' et 'password' dans le body.
    - Retourne l'influenceur si les identifiants sont corrects, sinon une erreur.
    """
    nom = request.data.get('nom')
    password = request.data.get('password')
    if not nom or not password:
        return Response({'detail': 'Nom et mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        influenceur = Influenceur.objects.get(nom=nom)
    except Influenceur.DoesNotExist:
        return Response({'detail': 'Nom ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not check_password(password, influenceur.password):
        return Response({'detail': 'Nom ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = InfluenceurSerializer(influenceur)
    return Response({'detail': 'Connexion réussie.', 'influenceur': serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET'])
def influenceur_dashboard_view(request, pk):
    """
    Vue API pour afficher le tableau de bord d'un influenceur.
    - GET : retourne stats et listes (prospects, remises) pour l'influenceur <pk>.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
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
def influenceur_prospects_view(request, pk):
    """
    Vue API pour lister tous les prospects d'un influenceur donné.
    - GET : retourne la liste des prospects pour l'influenceur <pk>.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    prospects = Prospect.objects.filter(influenceur=influenceur)
    serializer = ProspectSerializers(prospects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def influenceur_remises_view(request, pk):
    """
    Vue API pour lister toutes les remises d'un influenceur donné.
    - GET : retourne la liste des remises pour l'influenceur <pk>.
    """
    influenceur = get_object_or_404(Influenceur, pk=pk)
    remises = Remise.objects.filter(influenceur=influenceur)
    serializer = RemiseSerializers(remises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
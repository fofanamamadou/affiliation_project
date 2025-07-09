from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prospect
from .serializers import ProspectSerializers

@api_view(['GET', 'POST'])
def prospect_view(request):
    if request.method == 'GET':
        prospects = Prospect.objects.all()
        serializer = ProspectSerializers(prospects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Le statut est automatiquement "en_attente" par défaut dans le modèle
        serializer = ProspectSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def prospect_valider_view(request, pk):
    """
    Vue API pour valider un prospect (passer son statut à 'confirme').
    - POST : modifie le statut du prospect d'identifiant <pk>.
    """
    prospect = get_object_or_404(Prospect, pk=pk)
    if prospect.statut == 'confirme':
        return Response({'detail': 'Ce prospect est déjà confirmé.'}, status=status.HTTP_400_BAD_REQUEST)
    prospect.statut = 'confirme'
    prospect.save()
    serializer = ProspectSerializers(prospect)
    return Response({'detail': 'Prospect validé avec succès.', 'prospect': serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET'])
def prospects_sans_remise_view(request):
    """
    Vue API pour lister tous les prospects sans remise associée.
    - GET : retourne la liste des prospects où remise est null.
    """
    prospects = Prospect.objects.filter(remise__isnull=True)
    serializer = ProspectSerializers(prospects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
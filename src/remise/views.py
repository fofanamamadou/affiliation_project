from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Remise
from .serializers import RemiseSerializers



@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])  # Pour gérer l'upload d'image
def remise_view(request):
    if request.method == 'GET':
        remises = Remise.objects.all()
        serializer = RemiseSerializers(remises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = RemiseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def remise_payer_view(request, pk):
    """
    Vue API pour marquer une remise comme payée et uploader un justificatif.
    - POST : change le statut à 'payee' et ajoute un justificatif (image).
    """
    remise = get_object_or_404(Remise, pk=pk)
    if remise.statut == 'payee':
        return Response({'detail': 'Cette remise est déjà marquée comme payée.'}, status=status.HTTP_400_BAD_REQUEST)
    # On récupère le justificatif s'il est envoyé
    justificatif = request.FILES.get('justificatif')
    remise.statut = 'payee'
    if justificatif:
        remise.justificatif = justificatif
    remise.save()
    serializer = RemiseSerializers(remise)
    return Response({'detail': 'Remise marquée comme payée.', 'remise': serializer.data}, status=status.HTTP_200_OK)
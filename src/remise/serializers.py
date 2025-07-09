from rest_framework import serializers
from .models import Remise
from influenceur.serializers import InfluenceurSerializer
from influenceur.models import Influenceur


class RemiseSerializers(serializers.ModelSerializer) :

    # Pour voir les détails des classes (en lecture)
    influenceur_details = InfluenceurSerializer(source="influenceur", read_only=True)

    # Pour créer/modifier avec des IDs
    influenceur = serializers.PrimaryKeyRelatedField(queryset=Influenceur.objects.all(), allow_null=True)

    class Meta :
        model = Remise
        fields = '__all__'

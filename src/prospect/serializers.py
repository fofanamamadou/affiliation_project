from rest_framework import serializers
from .models import Prospect
from influenceur.serializers import InfluenceurSerializer
from influenceur.models import Influenceur
from remise.serializers import RemiseSerializers
from remise.models import Remise


class ProspectSerializers(serializers.ModelSerializer) :

    # Pour voir les détails (en lecture)
    influenceur_details = InfluenceurSerializer(source="influenceur", read_only=True)
    remise_details = RemiseSerializers(source="remise", read_only=True)

    # Pour créer/modifier avec des IDs
    influenceur = serializers.PrimaryKeyRelatedField(queryset=Influenceur.objects.all(), allow_null=True)
    remise = serializers.PrimaryKeyRelatedField(queryset=Remise.objects.all(), allow_null=True)

    class Meta :
        model = Prospect
        fields = '__all__'

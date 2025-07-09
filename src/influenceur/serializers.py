from rest_framework import serializers
from .models import Influenceur
from django.contrib.auth.hashers import make_password

class InfluenceurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influenceur
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        extracted_password = validated_data.pop('password', None)
        influenceur_instance = Influenceur(**validated_data)
        if extracted_password is not None:
            influenceur_instance.password = make_password(extracted_password)
        influenceur_instance.save()
        return influenceur_instance

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.password = make_password(password)
        return super().update(instance, validated_data)

    def get_affiliation_link(self, obj):
        return obj.get_affiliation_link()
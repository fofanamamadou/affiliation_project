from rest_framework import serializers
from .models import Influenceur
from django.contrib.auth.hashers import make_password

class InfluenceurSerializers(serializers.ModelSerializer) :

    class Meta :
        model : Influenceur
        fields = '__all__'
        # Cacher l'affichage du mot de passe dans le JSON
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validated_data):
            # Extraire le mot de passe des données validées
            extracted_password = validated_data.pop('password', None)

            # Créer l'instance de l'Influenceur avec les données restantes
            influenceur_instance = self.Meta.model(**validated_data)

            # Hacher et définir le mot de passe
            # Vérifier si un mot de passe a été fourni avant de le hacher
            if extracted_password is not None:
                influenceur_instance.password = make_password(extracted_password)

            # Sauvegarder l'instance de l'Influenceur dans la base de données
            influenceur_instance.save()

            # Retourner l'instance créée
            return influenceur_instance

        def update(self, instance, validated_data):
            # Gérer la mise à jour du mot de passe séparément si elle est présente
            if 'password' in validated_data:
                password = validated_data.pop('password')
                # Hacher et attribuer le nouveau mot de passe
                instance.password = make_password(password)

            # 2. Mettre à jour les autres champs de l'instance
            #    Appeler la méthode update originale du ModelSerializer pour les autres champs.
            #    Cela itérera sur les 'validated_data' restantes et mettra à jour l'instance.
            return super().update(instance, validated_data)
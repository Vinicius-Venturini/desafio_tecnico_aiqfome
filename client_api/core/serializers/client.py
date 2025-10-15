from rest_framework import serializers
from core.models import Client
from core.serializers.product import ClientProductSerializer

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'name']

class ClientDetailsSerializer(serializers.ModelSerializer):
    favorite_products = ClientProductSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'email', 'name', 'favorite_products']

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        client = Client.objects.create_user(
            password=password,
            **validated_data
        )
        return client
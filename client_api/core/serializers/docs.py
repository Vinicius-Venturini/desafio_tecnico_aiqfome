from rest_framework import serializers
from core.serializers.client import ClientDetailsSerializer, ClientSerializer
from core.serializers.product import ProductSerializer

class ErrorResponse(serializers.Serializer):
    detail = serializers.CharField()

class ClientResponse(serializers.Serializer):
    client = ClientDetailsSerializer()

class AllClientsResponse(serializers.Serializer):
    page = serializers.IntegerField()
    size = serializers.IntegerField()
    total = serializers.IntegerField()
    clients = ClientSerializer(many=True)

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()

class ProductResponse(serializers.Serializer):
    product = ProductSerializer()

class AllProductsResponse(serializers.Serializer):
    products = ProductSerializer(many=True)

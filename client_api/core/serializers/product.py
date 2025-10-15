from rest_framework import serializers
from core.models import ClientProduct, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "image"]

class ClientProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ClientProduct
        fields = ["product", "rating", "review"]

class FavoriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    rating = serializers.IntegerField(default=3, min_value=1, max_value=5)
    review = serializers.CharField(required=False, allow_blank=True)


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status

from core.services.product import get_all_products, get_product

class ProductView(ViewSet):
    permission_classes = [AllowAny]

    def get_all_products(self, request):
        products = get_all_products()
        return Response({'products': products})
    
    def get_product(self, request, id):
        try:
            product = get_product(id)
        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({'product': product})

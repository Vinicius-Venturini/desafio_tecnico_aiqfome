from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from core.serializers import docs

from core.services.product import get_all_products, get_product

class ProductView(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Returns all products',
        responses={
            200: docs.AllProductsResponse,
        }
    )
    def get_all_products(self, request):
        products = get_all_products()
        return Response({'products': products})
    
    @extend_schema(
        summary='Returns a specific product',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='The product ID',
                required=True,
            ),
        ],
        responses={
            200: docs.ProductResponse,
            404: docs.ErrorResponse,
        }
    )
    def get_product(self, request, id):
        try:
            product = get_product(id)
        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({'product': product})

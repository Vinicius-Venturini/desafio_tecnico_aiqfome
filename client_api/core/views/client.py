from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.services.client import update_client, favorite_product
from core.models import Client
from core.serializers.client import ClientSerializer, ClientDetailsSerializer, ClientCreateSerializer, UpdateClientSerializer
from core.serializers.product import FavoriteSerializer
from core.serializers import docs

@extend_schema(
        summary='Registers a new client in the database'
    )
class ClientRegisterView(generics.CreateAPIView):
    serializer_class = ClientCreateSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Client.objects.none()

@extend_schema(
        summary='Generates an authentication token',
        responses={
            200: docs.LoginResponseSerializer,
            400: docs.ErrorResponse,
            401: docs.ErrorResponse,
        }
    )
class ClientLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email:
            return Response({'detail': '"email" is a required field'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({'detail': '"password" is a required field'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token = AccessToken.for_user(user)

        return Response({
            'token': str(token)
        })

class ClientView(ViewSet):

    def get_permissions(self):
        if self.action in ['get_all_clients', 'get_client']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        summary='Returns all clients',
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Set the page for client listing',
                default=1,
                required=False,
            ),
            OpenApiParameter(
                name='size',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Set the amount of clients returned by page',
                default=50,
                required=False,
            ),
        ],
        responses={
            200: docs.AllClientsResponse
        }
    )
    def get_all_clients(self, request):
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        
        size = int(request.GET.get('size', 50))
        if size < 1:
            size = 50

        start = (page - 1) * size
        end = start + size

        clients = Client.objects.all()[start:end]
        total = clients.count()

        serializer = ClientSerializer(clients, many=True)

        return Response({
            'page': page,
            'size': size,
            'total': total,
            'clients': serializer.data,
        })
    
    @extend_schema(
        summary='Returns a specific client',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='The client ID',
                required=True,
            ),
        ],
        responses={
            200: docs.ClientResponse,
            404: docs.ErrorResponse,
        }
    )
    def get_client(self, request, id):
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientDetailsSerializer(client)

        return Response({'client': serializer.data})
    
    @extend_schema(
        summary='Update a client data',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='The client ID',
                required=True,
            ),
        ],
        request=UpdateClientSerializer,
        responses={
            200: docs.ClientResponse,
            400: docs.ErrorResponse,
            401: docs.ErrorResponse,
            403: docs.ErrorResponse,
            404: docs.ErrorResponse,
        }
    )
    def update_client(self, request, id):
        if request.user.pk != id:
            return Response({'detail': 'You don\'t have permission to execute this operation'}, status=status.HTTP_403_FORBIDDEN)
        
        client = request.user
        data = request.data.copy()

        try:
            updated_client = update_client(client, data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ClientDetailsSerializer(updated_client)

        return Response({'client': serializer.data})
    
    @extend_schema(
        summary='Remove a client',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='The client ID',
                required=True,
            ),
        ],
        responses={
            200: docs.ClientResponse,
            401: docs.ErrorResponse,
            403: docs.ErrorResponse,
            404: docs.ErrorResponse,
        }
    )
    def delete_client(self, request, id):
        if request.user.pk != id:
            return Response({'detail': 'You don\'t have permission to execute this operation'}, status=status.HTTP_403_FORBIDDEN)
        
        client = request.user
        serializer = ClientSerializer(client)
        client_data = serializer.data.copy()

        client.delete()

        return Response({'client': client_data})
    
    @extend_schema(
        summary='Set a product as a client favorite',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='The client ID',
                required=True,
            ),
        ],
        request=FavoriteSerializer,
        responses={
            200: docs.ClientResponse,
            400: docs.ErrorResponse,
            401: docs.ErrorResponse,
            403: docs.ErrorResponse,
            404: docs.ErrorResponse,
        }
    )
    def favorite_product(self, request, id):
        if request.user.pk != id:
            return Response({'detail': 'You don\'t have permission to execute this operation'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not data.get('product_id'):
            return Response({'detail': 'Field "product_id" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            favorite_product(client=request.user, **serializer.data)
        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'detail': 'This product is already favorite'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClientDetailsSerializer(request.user)
        return Response({'client': serializer.data})

from django.urls import path
from core.views.client import ClientRegisterView, ClientLoginView, ClientView
from core.views.product import ProductView

urlpatterns = [
    path('register/', ClientRegisterView.as_view(), name='register'),
    path('register', ClientRegisterView.as_view(), name='register'),
    path('login/', ClientLoginView.as_view(), name='login'),
    path('login', ClientLoginView.as_view(), name='login'),
    path('client/', ClientView.as_view({'get': 'get_all_clients'}), name='get_all_clients'),
    path('client/<int:id>', ClientView.as_view({'get': 'get_client', 'patch': 'update_client', 'delete': 'delete_client'}), name='client_manipulation'),
    path('client/<int:id>/', ClientView.as_view({'get': 'get_client', 'patch': 'update_client', 'delete': 'delete_client'}), name='client_manipulation'),
    path('product/', ProductView.as_view({'get': 'get_all_products'}), name='get_all_products'),
    path('product/<int:id>/', ProductView.as_view({'get': 'get_product'}), name='get_product'),
    path('client/<int:id>/favorite', ClientView.as_view({'post': 'favorite_product'}), name='favorite_product'),
]
"""
URL configuration for client_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import status
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

def custom_404(request, exception):
    return JsonResponse({'detail': f'"{request.path}" not found'}, status=status.HTTP_404_NOT_FOUND)

def custom_500(request):
    return JsonResponse({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include('core.urls'))
]

handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'

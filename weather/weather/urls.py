"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from weather_api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from weather_api import views
from weather_api.views import CreateCityAPIView, PrintCityInformationAPIView, WeatherForecastAPIView, registration_view
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Weather Fore cast Apis",
        default_version='v1',
        description="explore the weather information from tour city",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('ZxxX', views.login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('success/', views.success_view, name='success'),

    path('weather/<str:location>/', WeatherForecastAPIView.as_view(), name='weather-forecast information of single city '),
    path('', views.home, name = "home"),
    path('create-location/',views.createLocation,name="create-location"),
    path('weather_info/<str:pk>',views.display_weather,name = "display"),
     path('create-city/', CreateCityAPIView.as_view(), name='create_city_api'),
    path('print-cities/', PrintCityInformationAPIView.as_view(), name='print_all _city_weather_information_api'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token



]
   



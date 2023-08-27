from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from weather_api.forms import RegistrationForm
from weather_api.models import User
import datetime as dt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from weather_api.models import Locations
from weather_api.forms import LocationForm
from .forms import LocationForm

from .serializers import LocationSerializer, LocationWeatherSerializer, WeatherForecastSerializer

def success_view(request):
    return render(request, 'Weather_api/success.html')


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create and save the user
            User.objects.create(username=username, email=email, password=password)
            return redirect('success')  
    else:
        form = RegistrationForm()

    return render(request, 'Weather_api/register.html', {'form': form})






def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page after successful login
        else:
            
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'Weather_api/login.html', {'error_message': error_message})
    else:
        return render(request, 'weather_api/login.html') 


   





   


# def home (request,pk):
#     locations=Locations.objects.get(id=pk)
#     context = {'locations':locations}
#     return render(request,'Weather/home.html',context)

def home(request):
    locations=Locations.objects.all() 
    context={'locations':locations}
    return render(request,'weather_api/home.html',context)



def createLocation(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')  # Redirect to a success page
    else:
        form = LocationForm()

    return render(request, 'weather_api/locationForm.html', {'form': form})


def display_weather(request,pk):
    locations=Locations.objects.get(id=pk)
    api_key = 'fafc0d4443449a40deeaea503651d391'
    city = locations.name
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)
    weather_data = response.json()
    def kelvin_to_celcius(kelvin,decimal_places=2):
        celcius = round(kelvin - 273.15, decimal_places)
        return celcius 
    

    temp_kelvin=weather_data['main']['temp']
    temp_celcius=kelvin_to_celcius(temp_kelvin,decimal_places=2)
            # feels_like_kelvin=response['main']['feels_like']
            #feels_like_celcius,feels_like_fahrenheit=kelvin_to_celcius_farnheit(feels_like_kelvin)
    winds_speed= weather_data['wind']['speed']
    humidity=weather_data['main']['humidity']
    description=weather_data['weather'][0]['description']
    sunrise_time=dt.datetime.utcfromtimestamp(weather_data['sys']['sunrise']+ weather_data['timezone']) 
    sunset_time=dt.datetime.utcfromtimestamp(weather_data['sys']['sunset']+ weather_data['timezone']) 
    country= weather_data['sys']['country']
    city_name=weather_data['name']


    context = {
            'country' :country,
            'city_name': city_name,
            'temp_kelvin': temp_kelvin,
            'temp_celcius':temp_celcius,
            # 'temp_fahrenheit': temp_fahrenheit,
            # 'feels_like_celsius': feels_like_celsius,
            # 'feels_like_fahrenheit': feels_like_fahrenheit,
            'winds_speed': winds_speed,
            'humidity': humidity,
            'description': description,
            'sunrise_time': sunrise_time,
            'sunset_time': sunset_time
            }
    return render(request, 'weather_api/forecast_info.html', context)
        
        

    context = {'weather_data': weather_data}
    return render(request, 'weather_api/forecast_info.html', context)



class WeatherForecastAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]  # You can choose either
    permission_classes = [IsAuthenticated]
    serializer_class = WeatherForecastSerializer

    def retrieve(self, request, *args, **kwargs):
        location = self.kwargs['location']
        api_key = 'fafc0d4443449a40deeaea503651d391'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

        response = requests.get(url)
        data = response.json()

        serializer = self.get_serializer(data={
            'location': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            # Add more fields as needed
        })

        serializer.is_valid()
        return Response(serializer.data)
          

class CreateCityAPIView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]  # You can choose either
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PrintCityInformationAPIView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]  # You can choose either
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Print weather information for all cities",
        responses={status.HTTP_200_OK: "Your response description here"}
    )

    def get_weather_data(self, city_name):
        api_key = 'fafc0d4443449a40deeaea503651d391'
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'  # Use metric units for temperature
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather_description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed']
            }
            return weather_info
        else:
            return {
                'temperature': 'N/A',
                'humidity': 'N/A',
                'weather_description': 'N/A',
                'wind_speed': 'N/A'
            }

    def get(self, request, format=None):
        cities = Locations.objects.all()
        serializer = LocationWeatherSerializer(cities, many=True)

        city_data = serializer.data

        # Fetch and update weather information for each city
        for city_info in city_data:
            city_name = city_info['name']
            weather_info = self.get_weather_data(city_name)
            city_info.update(weather_info)

        return Response(city_data)
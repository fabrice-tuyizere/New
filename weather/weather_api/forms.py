from django import forms




class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


    
from django.forms import ModelForm

from weather_api.models import Locations



class LocationForm(ModelForm):
    class Meta:
        model= Locations
        fields= '__all__' 





from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=100)
   

    def __str__(self):
        return self.username


class Locations(models.Model):
    name= models.CharField(max_length= 20,unique=True,blank=False)
    def __str__(self):
        return self.name
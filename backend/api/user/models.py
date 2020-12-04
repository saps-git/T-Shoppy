from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser): #making a custom user model, different from the one that django provides user models
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=50, unique=True)

    username = None

    USERNAME_FIELD = 'email' #the normal username field is 'username' so changing it to email
    REQUIRED_FIELDS = [] # no particular reqd field

    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    session_token = models.CharField(max_length=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
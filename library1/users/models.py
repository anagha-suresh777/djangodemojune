from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#model definition
class Users(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    place = models.CharField(max_length=20)
    gender = models.CharField(max_length=2)


class CustomUser(AbstractUser):
    phone=models.BigIntegerField(default=0)
    address=models.CharField(max_length=20,default="")
    is_superuser = models.BooleanField(default=False)
    is_user=models.BooleanField(default=False)
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Electricity_Plan(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, default='0.00', null=False, blank=False)
    def __str__(self):
        return f'{self.name}'
    
class Electricity_Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.SET_NULL)
    pin = models.CharField(max_length=10)
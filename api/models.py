from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Electricity_Plan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    validity_period = models.CharField(max_length=50, null=True, blank=True)
    electricity_plan_price = models.DecimalField(max_digits=10, decimal_places=2, default=float('0.00'))
    def calculate_electricity_plan_price(self, validity_period):
        base_price = float(500)
        price = base_price * float(validity_period)
        return price 
    def __str__(self):
        return f'{self.name}'
    
class Electricity_Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Pricing_Detail(models.Model):
    base_price = models.DecimalField(max_digits=10, default='0.00', decimal_places=2)
    validity_period = models.CharField(max_length=255, null=True, blank=True)

class Electricity_Plan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    pricing_detail = models.OneToOneField(Pricing_Detail, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.name}'
    
class Electricity_Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Electricity_Plan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    number_of_units = models.CharField(max_length=365, null=True, blank=True)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=float('0.00'))
    def calculate_price(self, number_of_units):
        base_price = float(500)
        price = base_price * float(number_of_units)
        return price 
    def __str__(self):
        return f'{self.name}'
    
class Electricity_Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)
    pin = models.CharField(max_length=15)
    is_valid = models.BooleanField(default=True)

class ConsumptionReader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    percentage_consumed = models.FloatField()

class Paid_plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)
    card_holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    card_expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    amount_to_pay = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    meter_id = models.CharField(max_length=20)
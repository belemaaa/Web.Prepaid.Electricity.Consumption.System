from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils import timezone


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Electricity_Plan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    number_of_units = models.CharField(max_length=365, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
    number_of_units = models.CharField(max_length=365, null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=7))

class ConsumptionReader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    remaining_validity_days = models.IntegerField()
    percentage_consumed = models.FloatField()

    def update_consumption_data(self):
        # get all active electricity plans for the user
        active_plans = Electricity_Pin.objects.filter(
            user=self.user,
            is_valid=True,
            expiration_date__gte=timezone.now()
        ).values_list('electricity_plan__number_of_units', flat=True)
        # calculate remaining validity days
        min_expiration_date = min(Electricity_Pin.objects.filter(
            user=self.user,
            is_valid=True
        ).values_list('expiration_date', flat=True), default=timezone.now())
        self.remaining_validity_days = max((min_expiration_date - timezone.now()).days, 0)
        # calculate total and consumed units
        total_units = sum(active_plans)
        consumed_units = Electricity_Pin.objects.filter(
            user=self.user,
            is_valid=True
        ).aggregate(models.Sum('number_of_units'))['number_of_units__sum'] or 0
        # calculate percentage consumed
        self.percentage_consumed = (consumed_units / total_units) * 100 if total_units > 0 else 0
        self.save()

class Paid_plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    electricity_plan = models.ForeignKey(Electricity_Plan, on_delete=models.CASCADE)
    card_holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    card_expiry_date = models.CharField(max_length=10)
    cvv = models.CharField(max_length=3)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    meter_id = models.CharField(max_length=20)
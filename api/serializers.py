from rest_framework import serializers
from . import models


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password',
        ]

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class Electricity_plan_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Electricity_Plan
        fields = [
            'id',
            'name',
            'description',
            'number_of_units',
            'price'
        ]
class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.Payment
        fields = [
            'user',
            'card_holder_name',
            'card_number',
            'card_expiry_date',
            'cvv',
            'address',
            'phone_number',
            'meter_id'
        ]
    def get_user(self, obj):
        return {
            "id": obj.id,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "username": obj.username,
            "email": obj.email
        }
class PaidPlanSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    electricity_plan = serializers.SerializerMethodField()
    class Meta:
        model = models.Paid_plan
        fields = ['user', 'electricity_plan']

    def get_user(self, obj):
        return obj.user.id
    def get_electricity_plan(self, obj):
        return {
            'name': obj.electricity_plan.name,
            'description': obj.electricity_plan.description,
            'number_of_units': obj.electricity_plan.number_of_units,
            'price': obj.electricity_plan.price,
        }
class ConsumptionReaderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.ConsumptionReader
        fields = ['user', 'remaining_validity_days', 'percentage_consumed']
    def get_user(self, obj):
        return obj.user.id




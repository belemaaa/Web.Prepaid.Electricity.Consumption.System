from rest_framework import serializers
from . import models


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
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
            'number_of_unity',
            'price'
        ]

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.User
#         fields = [
#             'first_name',
#             'last_name',
#             'username',
#             'email',
#             'phone_number'
#         ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'card_holder_name',
            'card_number',
            'card_date',
            'cvv',
            'user'
        ]

class PaidPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paid_plan
        fields = [
            'user'
        ]
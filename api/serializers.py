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
        ]

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
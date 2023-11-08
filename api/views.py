from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from . import models
from . import serializers
from django.contrib.auth.hashers import make_password, check_password


class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            # hash user password
            hashed_password = make_password(password)
            user_exists = models.User.objects.filter(email=email)
            if user_exists:
                return Response({'status': 'Bad request', 'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(password=hashed_password)
            return Response({'status': 'success', 'message': 'signup successful.'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed request', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


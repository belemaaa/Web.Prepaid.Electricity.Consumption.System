from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from . import models
from . import serializers
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from .authentication import TokenAuthentication
from .permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
import json

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
            raw_password = serializer.validated_data.get('password')
            # hash user password
            hashed_password = make_password(raw_password)
            user_exists = models.User.objects.filter(email=email)
            if user_exists:
                return Response({'status': 'Bad request', 'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(password=hashed_password)
            return Response({'status': 'success', 'message': 'signup successful.'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed request', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = models.User.objects.get(email=email)
            except models.User.DoesNotExist:
                user=None
            if user is not None and check_password(password, user.password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'status': 'success',
                    'message': 'login successful',
                    'access_token': token.key,
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'email': user.email,
                        'phone_number': user.phone_number
                    }
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'failed request', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status': 'failed request', 'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class Create_Electricity_Plan(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    def post(self, request):
        serializer = serializers.Electricity_plan_serializer(data=request.data)
        if serializer.is_valid():
            plan_name = serializer.validated_data.get('name')
            plan_description = serializer.validated_data.get('description')
            validity_period = serializer.validated_data.get('validity_period')
            # calculate electricity price
            pricing_detail = models.Electricity_Plan.calculate_electricity_plan_price(validity_period)
            serializer.save(electricity_plan_price = pricing_detail)
            return Response({'status': 'success', 'message': 'new electricity plan has been created'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed request', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


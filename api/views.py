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
import random
from datetime import timedelta, timezone

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

class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = models.User.objects.get(user=request.user)
        return Response({
            'status': 'success',
            'data': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number
            }}, status=status.HTTP_200_OK)

class Electricity_Plan(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    def post(self, request):
        serializer = serializers.Electricity_plan_serializer(data=request.data)
        if serializer.is_valid():
            plan_name = serializer.validated_data.get('name')
            plan_description = serializer.validated_data.get('description')
            number_of_units = serializer.validated_data.get('number_of_units')
            # Create an instance of Electricity_Plan
            electricity_plan = models.Electricity_Plan()
            pricing_detail = electricity_plan.calculate_price(number_of_units)
            # Save the electricity plan with the calculated price
            electricity_plan.name = plan_name
            electricity_plan.description = plan_description
            electricity_plan.number_of_units = number_of_units
            electricity_plan.price = pricing_detail
            electricity_plan.save()
            return Response({'status': 'success', 'message': 'new electricity plan has been created'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed request', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        queryset = models.Electricity_Plan.objects.all()
        serializer = serializers.Electricity_plan_serializer(queryset, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

class Payment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def generate_pin(self, validity_days):
        expiration_date = timezone.now() + timedelta(days=validity_days)
        pin = str(random.randint(100000000000000, 999999999999999))
        return pin, expiration_date
    def post(self, request, plan_id):
        serializer = serializers.PaymentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            card_holder_name = serializer.validated_data.get('card_holder_name')
            card_number = serializer.validated_data.get('card_number')
            card_expiry_date = serializer.validated_data.get('card_expiry_date')
            cvv = serializer.validated_data.get('cvv')
            address = serializer.validated_data.get('address')
            phone_number = serializer.validated_data.get('phone_number')
            meter_id = serializer.validated_data.get('meter_id')
            try:
                electricity_plan = models.Electricity_Plan.objects.get(id=plan_id)
                if electricity_plan:
                    number_of_units = electricity_plan.number_of_units
                    price = electricity_plan.price
            except models.Electricity_Plan.DoesNotExist:
                electricity_plan = None
                return Response({'status': 'failed request', 'message': 'Plan id not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save(user=user, electricity_plan=electricity_plan)

            # generate electricity pin for the selected plan
            electricity_pin = models.Electricity_Pin()
            electricity_pin.pin, expiration_date = self.generate_pin(number_of_units * 2)
            electricity_pin.expiration_date = expiration_date
            electricity_pin.user = user
            electricity_pin.electricity_plan = electricity_plan
            electricity_pin.is_valid = True
            electricity_pin.number_of_units = number_of_units
            electricity_pin.save()
            # append the plan to the list of paid plans of the user
            paid_plans = models.Paid_plan.objects.create(electricity_plan=electricity_plan, user=user)  
            return Response({
                'status': 'success',
                'data': {
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'email': user.email
                    },
                    'phone_number': phone_number,
                    'address': address,
                    'meter_id': meter_id,
                    'electricity_pin': electricity_pin.pin,
                    'number_of_units': number_of_units,
                    'validity_period': f'{number_of_units * 2} days',
                    'price': price
                }}, status=status.HTTP_200_OK)
        return Response({'status': 'failed request', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Retrieve_Paid_Plans(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        queryset = models.Paid_plan.objects.get(user=user)
        serializer = serializers.PaidPlanSerializer(queryset, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
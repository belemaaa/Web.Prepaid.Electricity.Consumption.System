from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from . import models
from . import serializers


class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.UserSignupSerializer(data=request.data)
        

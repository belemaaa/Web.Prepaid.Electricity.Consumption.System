from django.urls import path 
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('create_electricity_plan/', views.Create_Electricity_Plan.as_view()),
]
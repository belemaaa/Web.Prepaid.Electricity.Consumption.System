from django.urls import path 
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('electricity_plans/create', views.Electricity_Plan.as_view()),
    path('electricity_plans/view', views.Electricity_Plan.as_view()),
    path('payment/<int:plan_id>/', views.Payment.as_view())
]
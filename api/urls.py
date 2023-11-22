from django.urls import path 
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('electricity_plans/create', views.Electricity_Plan.as_view()),
    path('electricity_plans/view', views.Get_Electricity_Plans.as_view()),
    path('electricity_plans/<int:plan_id>/delete', views.Electricity_Plan.as_view()),
    path('payment/<int:plan_id>', views.Payment.as_view()),
    path('profile/', views.Profile.as_view()),
    path('paid_plans/', views.Retrieve_Paid_Plans.as_view()),
    path('consumption_reader/', views.Consumption_Reader.as_view())
]
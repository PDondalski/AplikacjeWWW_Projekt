from django.urls import path
from budgetApp import views

urlpatterns = [
    path("", views.home, name='home'),
]
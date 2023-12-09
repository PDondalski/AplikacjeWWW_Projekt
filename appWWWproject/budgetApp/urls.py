from django.urls import path
from budgetApp import views
from . import views

urlpatterns = [
    path("", views.budget_list, name='list'),
    path("<int:id>", views.budget_detail, name='detail'),
]
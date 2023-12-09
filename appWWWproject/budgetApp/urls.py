from django.urls import path
from budgetApp import views
from . import views
from .views import BudgetDetailView

urlpatterns = [
    path("", views.budget_list, name='list'),
    path("<int:id>", views.budget_detail, name='detail'),
    path('budget/<int:id>/', BudgetDetailView.as_view(), name='budget-detail'),
]
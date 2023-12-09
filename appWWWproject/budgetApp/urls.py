from django.urls import path
from budgetApp import views
from . import views
from .views import BudgetDetail, BudgetList, CategoryDetail, CategoryList

urlpatterns = [
    path("", views.budget_list, name='list'),
    path("<int:id>", views.budget_detail, name='detail'),
    path('budgets/<int:id>/', BudgetDetail.as_view(), name='budget-detail'),
    path('budgets/', BudgetList.as_view(), name='budget-list'),
    path('categories/<int:id>', CategoryDetail.as_view(), name='category-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
]
from django.urls import path
from budgetApp import views
from . import views
from .views import (BudgetDetail, BudgetList, CategoryDetail, CategoryList,
                    ExpenseList, ExpenseDetail, SavingsList, SavingsDetail, UserDetailAPI,RegisterUserAPIView,
                    CreateBudgetView, CreateWydatekView, CreateKategoriaView)


urlpatterns = [
    path("", views.budget_list, name='list'),
    path("<int:id>", views.budget_detail, name='detail'),
    path('budgets/<int:id>/', BudgetDetail.as_view(), name='budget-detail'),
    path('budgets/', BudgetList.as_view(), name='budget-list'),
    path('budgets/add', CreateBudgetView.as_view(), name='budgets-add'),
    path('categories/add', CreateWydatekView.as_view(), name='categories-add'),
    path('expenses/add', CreateKategoriaView.as_view(), name='expenses-add'),
    path('categories/<int:id>', CategoryDetail.as_view(), name='category-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path("get-details",UserDetailAPI.as_view()),
    path('register',RegisterUserAPIView.as_view()),
    path('expenses/<int:id>', ExpenseDetail.as_view(), name='expense-detail'),
    path('expenses/', ExpenseList.as_view(), name='expense-list'),
    path('savings/<int:id>', SavingsDetail.as_view(), name='savings-detail'),
    path('savings/', SavingsList.as_view(), name='savings-list'),
    path('login/', views.LoginView.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

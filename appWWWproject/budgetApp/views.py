from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    return render(request, "budgetApp/home.html", {})

def budget_list(request):
    return render(request, "budgetApp/budget-list.html", {})

def budget_detail(request, id):
    budget = get_object_or_404(BgBudzet, pk=id)
    return render(request, "budgetApp/budget-detail.html", {'budget': budget, 'wydatek_list': budget.wydatek.all()})
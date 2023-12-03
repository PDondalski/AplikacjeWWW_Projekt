from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import *

def home(request):
    return render(request, "budgetApp/home.html", {})

def budget_list(request):
    return render(request, "budgetApp/budget-list.html", {})

def budget_detail(request, id):
    budget = get_object_or_404(BgBudzet, pk=id)
    total_wydatek = budget.wydatek.all().aggregate(Sum('wydatek_wartosc'))['wydatek_wartosc__sum']
    oszczednosci = budget.budzet_wartosc - total_wydatek if total_wydatek else budget.budzet_wartosc
    return render(request, "budgetApp/budget-detail.html",
                  {'budget': budget, 'wydatek_list': budget.wydatek.all(), 'total_wydatek': total_wydatek,
                   'oszczednosci': oszczednosci})

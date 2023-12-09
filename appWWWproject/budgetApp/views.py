from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import BgBudzetSerializer, BgWydatekSerializer
from django.http import Http404

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

class BudgetDetail(APIView):
    def get_object(self, id):
        try:
            return BgBudzet.objects.get(pk=id)
        except BgBudzet.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        budget = self.get_object(id)
        total_wydatek = budget.wydatek.all().aggregate(Sum('wydatek_wartosc'))['wydatek_wartosc__sum']
        oszczednosci = budget.budzet_wartosc - total_wydatek if total_wydatek else budget.budzet_wartosc
        budget_serializer = BgBudzetSerializer(budget)
        return Response({
            'budget': budget_serializer.data,
            'total_wydatek': total_wydatek,
            'oszczednosci': oszczednosci
        })

class BudgetList(APIView):
    def get(self, request, format=None):
        budgets = BgBudzet.objects.all().order_by('-budzet_rok', '-budzet_miesiac')
        serializer = BgBudzetSerializer(budgets, many=True)
        return Response(serializer.data)
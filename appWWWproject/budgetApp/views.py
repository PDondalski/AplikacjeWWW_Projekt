from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from rest_framework import status

from .models import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import BgBudzetSerializer, BgWydatekSerializer, BgKategoriaSerializer, BgOszczednoscSerializer
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
            'budzet': budget_serializer.data,
            'total_wydatek': total_wydatek,
            'oszczednosci': oszczednosci
        })

class BudgetList(APIView):
    def get(self, request, format=None):
        budgets = BgBudzet.objects.all().order_by('-budzet_rok', '-budzet_miesiac')
        serializer = BgBudzetSerializer(budgets, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetail(APIView):
    def get_object(self, id):
        try:
            return BgKategoria.objects.get(pk=id)
        except BgKategoria.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        category = self.get_object(id)
        serializer = BgKategoriaSerializer(category)
        return Response(serializer.data)


class CategoryList(APIView):
    def get(self, request, format=None):
        categories = BgKategoria.objects.all().order_by('budzet')
        serializer = BgKategoriaSerializer(categories, many=True)
        return Response(serializer.data)

class ExpenseDetail(APIView):
    def get_object(self, id):
        try:
            return BgWydatek.objects.get(pk=id)
        except BgWydatek.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        expense = self.get_object(id)
        serializer = BgWydatekSerializer(expense)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExpenseList(APIView):
    def get(self, request, format=None):
        expenses = BgWydatek.objects.all().order_by('-wydatek_budzet')
        serializer = BgWydatekSerializer(expenses, many=True)
        return Response(serializer.data)

class SavingsDetail(APIView):
    def get_object(self, id):
        try:
            return BgOszczednosc.objects.get(pk=id)
        except BgOszczednosc.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        saving = self.get_object(id)
        serializer = BgOszczednoscSerializer(saving)
        return Response(serializer.data)

class SavingsList(APIView):
    def get(self, request, format=None):
        savings = BgOszczednosc.objects.all()
        serializer = BgOszczednoscSerializer(savings, many=True)
        return Response(serializer.data)
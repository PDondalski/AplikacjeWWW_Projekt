from rest_framework import serializers
from .models import BgBudzet, BgKategoria, BgWydatek, BgOszczednosc

class BgBudzetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgBudzet
        fields = ['budzet_rok', 'budzet_miesiac', 'budzet_wartosc']
        read_only_fields = ['id']
class BgKategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgKategoria
        fields = ['budzet', 'kategoria_nazwa', 'kategoria_wydatek']
        read_only_fields = ['id']
class BgWydatekSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgWydatek
        fields = ['wydatek_budzet', 'wydatek_kategoria', 'wydatek_wartosc', 'wydatek_data']
        read_only_fields = ['id']
class BgOszczednoscSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgOszczednosc
        fields = ['budzet', 'osczednosc_calkowita']
        read_only_fields = ['id']
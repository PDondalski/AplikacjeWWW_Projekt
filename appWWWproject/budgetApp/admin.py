from django.contrib import admin

from .models import *

admin.site.register(BgBudzet)
admin.site.register(BgKategoria)
admin.site.register(BgOszczednosc)
admin.site.register(BgWydatek)


#@admin.register(BudgetBudzet)
''' class BudgetBudzetAdmin(admin.ModelAdmin):
    list_display = ('rok','miesiac', 'budzet_wartosc')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save() '''

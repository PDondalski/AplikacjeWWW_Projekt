# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime
from datetime import date

from django.db.models import Sum
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

######################################################################################################
class BgBudzet(models.Model):
    budzet_rok = models.IntegerField(blank=True, null=True)
    budzet_miesiac = models.IntegerField(blank=True, null=True)
    budzet_wartosc = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)  # This field type is a guess.

    def __str__(self):
        return f'{self.budzet_miesiac}/{self.budzet_rok}'


class BgKategoria(models.Model):
    budzet = models.ForeignKey(BgBudzet, on_delete=models.CASCADE, default=1)
    kategoria_nazwa = models.CharField(blank=True, null=True, max_length=55)
    kategoria_wydatek = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)  # This field type is a guess.

    def __str__(self):
        return f'{self.kategoria_nazwa} ({self.budzet.budzet_miesiac}/{self.budzet.budzet_rok})'


class BgWydatek(models.Model):
    wydatek_budzet = models.ForeignKey(BgBudzet, on_delete=models.CASCADE, default=1, related_name='wydatek')
    wydatek_kategoria = models.ForeignKey(BgKategoria, on_delete=models.CASCADE)
    wydatek_wartosc = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)  # This field type is a guess.
    wydatek_data = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.wydatek_wartosc} | {self.wydatek_data}'


class BgOszczednosc(models.Model):
    budzet = models.ForeignKey(BgBudzet, on_delete=models.CASCADE)
    osczednosc_calkowita = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.osczednosc_calkowita)

'''
    @receiver(post_save, sender=BgWydatek)
    def calculate_savings(sender, instance, **kwargs):
        budget = instance.wydatek_budzet
        total_wydatek = budget.wydatek.all().aggregate(Sum('wydatek_wartosc'))['wydatek_wartosc__sum']
        oszczednosci = budget.budzet_wartosc - total_wydatek if total_wydatek else budget.budzet_wartosc

        BgOszczednosc.objects.update_or_create(budzet=budget, defaults={'osczednosc_calkowita': oszczednosci})
'''

#######################################################################################################

class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

"""Specifies which models can be CRUDed in the admin app"""
from django.contrib import admin

# Register your models here.


from .models import Car, Constructor, Driver, Engine, EngineMaker, Season, DrivingContract, CarNumber, Rule, ConstructorTransfer

# Autopopulate slugs
# https://www.w3schools.com/django/django_slug_field.php
class DriverAdmin(admin.ModelAdmin):
#   list_display = ("firstname", "lastname", "joined_date",)
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class ConstructorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class CarAdmin(admin.ModelAdmin):
    # list_display = ("constructor", "name",)
    prepopulated_fields = {"slug": ("constructor", "name",)}

class CarNumberAdmin(admin.ModelAdmin):
    list_display = ("season", "team",)

class DrivingContractAdmin(admin.ModelAdmin):
    list_display = ("season", "driver", "team",)

# class ConstructorTransferAdmin(admin.ModelAdmin):
#     list_display = ("season", "previous", "new")

admin.site.register(Driver, DriverAdmin)
admin.site.register(Constructor, ConstructorAdmin)

admin.site.register(Car, CarAdmin)
# admin.site.register(TeamManager)
admin.site.register(Season)
# admin.site.register(Drive)
admin.site.register(DrivingContract, DrivingContractAdmin)
admin.site.register(CarNumber, CarNumberAdmin)
admin.site.register(Engine)
admin.site.register(EngineMaker)
admin.site.register(Rule)
admin.site.register(ConstructorTransfer)

  
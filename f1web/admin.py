"""Specifies which models can be CRUDed in the admin app"""
from django.contrib import admin

# Register your models here.


from .models import Car, Constructor, Driver, TeamManager, Engine, EngineMaker, Season, DrivingContract, CarNumber

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

admin.site.register(Driver, DriverAdmin)
admin.site.register(Constructor, ConstructorAdmin)

admin.site.register(Car, CarAdmin)
admin.site.register(TeamManager)
admin.site.register(Season)
# admin.site.register(Drive)
admin.site.register(DrivingContract)
admin.site.register(CarNumber)
admin.site.register(Engine)
admin.site.register(EngineMaker)

  
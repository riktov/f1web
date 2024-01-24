"""URLs for the browse app"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("driver/<slug:slug>/", views.DriverDetailView.as_view(), name="driver_detail"),
    path("driver/", views.DriverListView.as_view(), name="driver_list"),
    path("car/<slug:slug>/", views.CarDetailView.as_view(), name="car_detail"),
    path("car/", views.CarListView.as_view(), name="car_list"),
    path("constructor/<slug:slug>/", views.ConstructorDetailView.as_view(), name="constructor_detail"),
    path("constructor/", views.ConstructorListView.as_view(), name="constructor_list"),
    path("season/<int:pk>/", views.SeasonDetailView.as_view(), name="season_detail"),
    path("season/", views.SeasonListView.as_view(), name="season_list"),
    path("engine/<int:pk>/", views.EngineDetailView.as_view(), name="engine_detail"),
    path("engine/", views.EngineListView.as_view(), name="engine_list"),
    path("enginemaker/<slug:slug>/", views.EngineMakerDetailView.as_view(), name="enginemaker_detail"),
    path("enginemaker/", views.EngineMakerListView.as_view(), name="enginemaker_list"),

    path("country/", views.countries_view, name="country_list"),
    path("number/", views.numbers_view, name="number_list"),
]

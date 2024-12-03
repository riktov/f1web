from django.shortcuts import render

from browse import forms
from f1web.models import Driver
from game.forms import DriverSelectionForm

def index(request):
    get_dict = request.GET.dict()

    if len(get_dict) == 0:
        context = {
            "form": DriverSelectionForm()
        }
        return render(request, "game/index.html", context)
    
    driver_from = Driver.objects.get(pk = get_dict["driver_from"])
    driver_to = Driver.objects.get(pk = get_dict["driver_to"])
    
    seasons = driver_from.seasons
    seasons = sorted(seasons, key=lambda s:s.year)
    
    context = {
        "driver_from": driver_from,
        "driver_to": driver_from,
        "driver_to": driver_to,
        "seasons": seasons
    }

    return render(request, "game/play.html", context)

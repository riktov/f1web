from django.shortcuts import render

from browse import forms
from f1web.models import Driver, DrivingContract, Season
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
    driver = driver_from 

    if get_dict.get("driver"):
        driver = Driver.objects.get(pk = get_dict["driver"])

    season = get_dict.get("season")

    if season:
        season = Season.objects.get(pk = int(season))
        
        dcs = DrivingContract.objects.filter(driver=driver, season=season)
        team = dcs[0].team
        drives = team.drives.filter(season = season)
        drives = drives.exclude(driver = driver)
        teammates = [dr.driver for dr in drives]
        context = {
            "driver_from": driver_from,
            "driver_to": driver_to,
            "driver": driver,
            "teammates": teammates
        }
        return render(request, "game/select_teammate.html", context)

    drives = sorted(driver.drives(), key=lambda d:d.season)
    
    context = {
        "driver_from": driver_from,
        "driver_to": driver_to,
        "driver": driver,
        "drives": drives
    }

    return render(request, "game/select_season.html", context)

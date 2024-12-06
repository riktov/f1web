from django.shortcuts import render

from f1web.models import Driver, DrivingContract, Season
from game.forms import DriverSelectionForm
from game.queries import teamings, teammates_all
from game.trail import decode_trail, get_teamups
from game.util import collapse_trail

def index(request):
    get_dict = request.GET.dict()

    if len(get_dict) == 0:
        context = {
            "form": DriverSelectionForm()
        }
        return render(request, "game/index.html", context)

    if "random" in get_dict:
        driver_from = Driver.objects.all().order_by("?").first()
        driver_to = Driver.objects.exclude(pk=driver_from.pk).order_by("?").first()

    else:
        driver_from = Driver.objects.get(pk = get_dict["driver_from"])
        driver_to = Driver.objects.get(pk = get_dict["driver_to"])

    if get_dict.get("driver"):
        driver = Driver.objects.get(pk = get_dict["driver"])
    else:
        driver = driver_from 

    trail = get_dict.get("trail", "")

    if driver_to == driver:
        drivers_trail = collapse_trail(decode_trail(trail))
        drivers_trail.append(driver)
        teamups_trail = get_teamups(drivers_trail)
        context = {
            "trail": zip(drivers_trail, teamups_trail),
            "driver_from": driver_from,
            "driver_to": driver_to
        }
        return render(request, "game/finished.html", context)


    season = get_dict.get("season")

    
    if season:
        #select one of the teammates from the season 
        season = Season.objects.get(pk = int(season))
        
        dcs = DrivingContract.objects.filter(driver=driver, season=season)
        team = dcs[0].team
        drives = team.drives.filter(season = season)
        drives = drives.exclude(driver = driver)
        all_teammates = [dr.driver for dr in drives]
        context = {
            "driver_from": driver_from,
            "driver_to": driver_to,
            "driver": driver,
            "teammates": all_teammates
        }
        return render(request, "game/select_teammate.html", context)

    #pick a season of the driver

    drives = driver.drives.all()
    # drives = sorted(driver.drives(), key=lambda d:d.season)
    
    all_teammates = sorted(teammates_all(driver), key = lambda d: d.name)

    teammates_and_teamings = [(tm, teamings(driver, tm)) for tm in all_teammates]
    
    context = {
        "driver_from": driver_from,
        "driver_to": driver_to,
        "driver": driver,
        "drives": drives,
        "teammates": all_teammates,
        "teammates_and_teamings": teammates_and_teamings,
        "trail": f"{trail},d{driver.id}"
    }

    return render(request, "game/select_season.html", context)

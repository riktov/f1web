from f1web.models import Driver, DrivingContract
from django.db.models import Q, Min

def rookies(season):
    """Return a QuerySet of drivers who arrived in a specified season"""

    # Get all drivers who have a contract in this season
    this_season_drivers = DrivingContract.objects.filter(season=season).values_list('driver', flat=True)

    # Filter drivers whose first season is this season
    rookies = DrivingContract.objects.filter(driver__in=this_season_drivers).annotate(
        first_season=Min('season')
    ).filter(first_season=season).values_list('driver', flat=True).distinct()

    return rookies

def enders(season):
    """Return a QuerySet of drivers who left immediately following a specified season"""
    enders = []
    # Get all drivers who have a contract in this season
    this_season_drivers = { dc.driver for dc in DrivingContract.objects.filter(season=season) }

    # For each, get the last season they drove in
    for driver in this_season_drivers:
        last_season = driver.seasons.last()
        if last_season == season:
            enders.append(driver)
    # If it is this season, they are an ender

    # Sort the drivers by order of their first season
    enders.sort(key=lambda d: d.seasons.first().year)

    return Driver.objects.filter(pk__in=[d.pk for d in enders])

def single_driver_countries():
    """Return a set (not a QuerySet!) of all countries that have never had more than one driver in a single season"""

    countries = { dr.country for dr in Driver.objects.all() }

    singles = set()

    for country in countries:
        if Driver.objects.filter(country=country).count() < 2:
            singles.add(country)
        else:   #countries that have had more than one driver, but maybe never more than one in the same season
            is_single = True
            seasons = {dc.season for dc in DrivingContract.objects.filter(driver__country=country)}
            for season in seasons:
                drivers_count = season.drivers().filter(country=country).count()
                if drivers_count > 1:
                    is_single = False
                    break
            if is_single:
                singles.add(country)

    return singles


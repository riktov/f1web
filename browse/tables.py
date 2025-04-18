"""tables that are created in views and passed to templates"""
from f1web.models import Driver, DrivingContract
from browse.forms import CreateDriveForSeasonForm, CreateNumberForm
from django.db.models import Q, Min

# TODO: We could probably use annotations. Annotations add ad-hoc fields to the query result.
def team_car_drivers_for_season(season):
    """For a Season, return a list of teams containing team name, cars, and drivers"""
    team_car_drivers = []

    for team in season.constructors():
        row = {
            "team": team,
            "cars": season.cars.filter(constructor=team),
            # "drivers": [(dr, dr.car_number_in(season, team), dr.is_lead_in(season, team)) for dr in drivers],
            "drives": season.drives.filter(team=team).order_by('starting_round', '-is_lead'),
            "numbers": team.car_numbers(season),
            "form": CreateNumberForm(initial = {'team':team }),
            "form_drives" : CreateDriveForSeasonForm(initial = {'season':season, 'team':team})
        }
        team_car_drivers.append(row)

    rows_with_car_numbers = sorted([ r for r in team_car_drivers if r["numbers"] ],
                                   key = lambda r: r["numbers"][0])
    rows_without_car_numbers = [ r for r in team_car_drivers if not r["numbers"] ]

    return rows_with_car_numbers + rows_without_car_numbers

def cars_grouped_by_season(cars):
    """Sort a list of cars by season. If a car has no season, place at end of list"""
    cars_dict = {}
    cars_without_seasons = []

    for car in cars:
        earliest = car.earliest_season()
        if earliest is None:
            cars_without_seasons.append(car)
        else:
            if earliest not in cars_dict:
                cars_dict[earliest] = []
            cars_dict[earliest].append(car)

    seasons = sorted(cars_dict.keys(), key=lambda s:s.year)

    table = [[s, cars_dict[s]] for s in seasons]

    return table + [[None, [car]] for car in cars_without_seasons]

def season_drivers_for_car(car):
    """For a Car, return a list of seasons in which it ran, containing season and drivers"""
    pass

def xxxdriver_history(driver, season):
    """Return
    driver
    this season's team
    total seasons (including this one) in F1
    total seasons (up to this one) in this team. So earlier stints do not count
    previous team, if applicable
    """
    this_season_teams = [dc.team for dc in DrivingContract.objects.filter(driver=driver, season=season)]
    
    prev_seasons= [ s for s in driver.seasons if s < season ]

    if not prev_seasons:
        #rookie
        return [ driver, this_season_teams, None , 1, 1]
    
    last_season = sorted(prev_seasons)[-1]
    last_season_teams = [dc.team for dc in DrivingContract.objects.filter(driver=driver, season=last_season)]

    if len(last_season_teams) == 1 and len(this_season_teams) == 1 and  last_season_teams[0] == this_season_teams[0]:
        #same as last season
        #better to find common in the two
        se = season
        current_stint = 1 
        while se.previous() and DrivingContract.objects.filter(driver=driver, season=se.previous(), team=this_season_teams[0]):
            current_stint = current_stint + 1
            se = se.previous()
        return [ driver, this_season_teams, None, current_stint, len(prev_seasons) + 1]

    #moved from another team
    return [ driver, this_season_teams, last_season_teams,  1, len(prev_seasons) +1 ]

def driver_country_histogram(drivers):
    """Return a dict of the number of drivers of each country.
    The driver set would typically be those in one season"""
    countries = [dr.country for dr in drivers]

    counts = {}

    for c in countries:
        if c.code in counts:
            counts[c.code] = counts[c.code] + 1
        else:
            counts[c.code] = 1

    return counts

def driver_country_tally(season, starters_only=True):
    drives = DrivingContract.objects.filter(season=season)
    if starters_only:
        drives = drives.filter(starting_round = 1)

    tally = {}
    
    for drive in drives:
        country = drive.driver.country.code
        if country in tally:
            tally[country] += 1
        else:
            tally[country] = 1 

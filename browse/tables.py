"""tables that are created in views and passed to templates"""
from f1web.models import DrivingContract

def team_car_drivers_for_season(season):
    """For a Season, return a list of dictionaries containing team, cars, drivers"""
    team_car_drivers = []

    for team in season.constructors():
        try:
            drives = season.drives.filter(team=team)

            drivers = [drive.driver for drive in drives]

            if team.car_numbers(season):
                drivers.sort(key = lambda d: d.car_number_in(season, team))
            row = {
                "team": team,
                "cars": season.cars.filter(constructor=team),
                "drivers": [(dr, dr.car_number_in(season, team), 
                             dr.is_lead_in(season, team)) for dr in drivers],
                "numbers": team.car_numbers(season)
            }
            team_car_drivers.append(row)

        except DrivingContract.DoesNotExist:
            pass

    rows_with_car_numbers = sorted([ r for r in team_car_drivers if r["numbers"] ],
                                   key = lambda r: r["numbers"][0])
    rows_without_car_numbers = [ r for r in team_car_drivers if not r["numbers"] ]

    return rows_with_car_numbers + rows_without_car_numbers

def cars_grouped_by_season(cars):
    """Table or cars"""
    cars_dict = {}

    for car in cars:
        earliest = car.earliest_season()
        if earliest not in cars_dict:
            cars_dict[earliest] = []
        cars_dict[earliest].append(car)

    seasons = sorted(cars_dict.keys(), key=lambda s:s.year)

    table = [[s, cars_dict[s]] for s in seasons]

    return table

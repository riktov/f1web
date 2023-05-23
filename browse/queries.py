"""Queries that a are too complex to place directly in Views or Models"""
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
                "drivers": [(dr, dr.car_number_in(season, team)) for dr in drivers],
                "numbers": team.car_numbers(season)
            }
            team_car_drivers.append(row)

        except DrivingContract.DoesNotExist:
            pass

    rows_with_car_numbers = sorted([ r for r in team_car_drivers if r["numbers"] ], key = lambda r: r["numbers"][0])
    rows_without_car_numbers = [ r for r in team_car_drivers if not r["numbers"] ]
    
    return rows_with_car_numbers + rows_without_car_numbers
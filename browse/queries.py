"""Queries that a are too complex to place directly in Views or Models"""
from f1web.models import DrivingContract

def team_car_drivers_for_season(season):
    """For a Season, return a list of dictionaries containing team, cars, drivers"""
    teams_with_cars = { car.constructor for car in season.cars.all() }    #set comprehension
    teams_with_drivers = { drive.team for drive in season.drives.all() }

    teams = teams_with_cars.union(teams_with_drivers)
    #sort by car number

    team_car_drivers = []

    # drive = self.drives.filter(season=self)

    for team in teams:
        try:
            drives = season.drives.filter(team=team)

            drivers = [drive.driver for drive in drives]
            #TODO: sort by car number
            
            team_dict = {
                "team": team,
                "cars": season.cars.filter(constructor=team),
                "drivers": [(dr, dr.car_number_in(season, team)) for dr in drivers],
                "numbers": team.car_numbers(season)
            }
            team_car_drivers.append(team_dict)

        except DrivingContract.DoesNotExist:
            pass

    return team_car_drivers
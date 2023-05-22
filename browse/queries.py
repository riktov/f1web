from f1web.models import DrivingContract

def team_car_drivers_for_season(season):
    teams = { car.constructor for car in season.cars.all() }    #set comprehension
    #sort by car number

    team_car_drivers = []

    # drive = self.drives.filter(season=self)

    for team in teams:
        try:
            drives = season.drives.filter(season=season, team=team)

            drivers = [drive.driver for drive in drives]
            team_dict = {
                "team": team,
                "cars": season.cars.filter(constructor=team),
                "drivers": [(dr, dr.car_number_in(season, team)) for dr in drivers]
            }
            team_car_drivers.append(team_dict)

        except DrivingContract.DoesNotExist:
            pass

    return team_car_drivers
from f1web.models import Car, DrivingContract, Season


def run(*args):
    year = int(args[0])

    previous_season = Season.objects.get(year=year-1)
    this_season = Season.objects.get(year=year)

    prev_season_cars =  Car.objects.filter(season=previous_season)

    for car in prev_season_cars:
        car_designation_number = ''.join(filter(str.isdigit, car.name))
        car_designation_text = ''.join(filter(str.isalpha, car.name))
        # print((car_designation_text, car_designation_number))

        this_season_car = Car(name=f"{car_designation_text}{int(car_designation_number)+1}", season=Season.objects.get(year=year))
        this_season_car.engine = car.engine
        this_season_car.constructor = car.constructor
        this_season_car.save()
        print(this_season_car)
        this_season.cars.add(this_season_car)
    
    last_season_drives = DrivingContract.objects.filter(season=previous_season)

    for drive in last_season_drives:
        driver = drive.driver
        team = drive.team
        this_season_driving_contract = DrivingContract(driver=driver, team=team, season=this_season)
        this_season_driving_contract.save()
        print(this_season_driving_contract)

    prev_season_teams  = [car.constructor for car in prev_season_cars]
    print(prev_season_teams)


if __name__ == "__main__":
    run()

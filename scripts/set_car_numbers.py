import sys

from f1web.models import CarNumber, Season

#runscript set_car_numbers --script-args 1983

def numbers_1996(year):
    # Reigning driver's champion gets #1 on his current car
    # All other teams get numbers based on constructor's results        
    prev_season = year - 1
    print(f"-- Reigning (won in {prev_season}) --")
    prev_season = Season.objects.get(year=prev_season)
    driver_champ = prev_season.drivers_champion
    driver_champ_team = prev_season.drivers_champion_team
    print(f"Driver: {driver_champ} for {driver_champ_team}")
    print(f"Constructor: {prev_season.constructors_champion}")

    print(f"-- This Season ({year}) --")
    this_season = Season.objects.get(year=year)
    champions_new_ride = driver_champ.drives.get(season = this_season)
    print(f"{champions_new_ride.driver} drives for {champions_new_ride.team}")
    print(f"{champions_new_ride.team} gets #1")

def numbers_1973_1995(year):
    # Reigning driver's champion gets #1 on his current car, swaps with previous #1
    # If reigning champion has no drive, the team he won in gets #0

    prev_season = year - 1
    print(f"-- Reigning (won in {prev_season}) --")
    prev_season = Season.objects.get(year=year - 1)
    driver_champ = prev_season.drivers_champion
    driver_champ_team = prev_season.drivers_champion_team
    print(f"Driver: {driver_champ} for {driver_champ_team}")
    print(f"Constructor: {prev_season.constructors_champion}")


    print(f"-- This Season ({year}) --")
    this_season = Season.objects.get(year=year)

    champions_new_rides = driver_champ.drives.filter(season = this_season)
    if champions_new_rides:
        new_ride = champions_new_rides[0]
        print(f"{new_ride.driver} drives for {new_ride.team}")
        print(f"{new_ride.team} gets #1")
    else:
        print("The reigning champion is not driving this season!")
    

    # cn_champ = CarNumber.objects.create(season = this_season, team = new_ride.team, number = 1)
    
    old_number = driver_champ_team.car_numbers(prev_season)
    print(f"Gives away {new_ride.team}'s {prev_season} numbers {old_number} to the team that had #1 in {prev_season}")
    old_1 = None
    try:
        old_1 = CarNumber.objects.get(season=prev_season, number__lt = 2)
        print(old_1.team)
    except CarNumber.DoesNotExist:
        print(f"Can't find {prev_season} holder of #1")
    
    this_year_entrants = this_season.constructors()
    # print(this_year_entrants)

    print("-- Teams with the same numbers --")
    for ent in this_year_entrants:
        if ent == new_ride.team :
            continue
        if old_1 and ent == old_1.team :
            continue
        print(ent)
        try:
            prev_num = CarNumber.objects.get(team = ent, season = prev_season)
            print(prev_num)
            this_nums = CarNumber.objects.filter(team = ent, season = this_season)
            if this_nums:
                print(f"{ent} already has numbers for {this_season}! : {this_nums[0].number}")
            else:
                cn = CarNumber.objects.create(season = this_season, team = ent, number = prev_num.number)
                print(cn)
        except CarNumber.DoesNotExist:
            print(f"No numbers for {ent} in {prev_season}")

def run(*args):
    print(f"Setting car numbers for season {args[0]}")
    year = int(args[0])

    if year < 1996:
        numbers_1973_1995(year)
    else:
        numbers_1996(year)

if __name__ == "main":
    run()
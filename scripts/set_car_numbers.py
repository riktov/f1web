"""Set car numbers based on regulations"""

from f1web.models import CarNumber, Season

# runscript set_car_numbers --script-args 1983

def champ_gets_number1(this_season, prev_season):
    driver_champ = prev_season.drivers_champion

    print(f"-- Reigning (won in {prev_season}) --")
    print(f"Driver: {driver_champ}")

    print(f"-- This Season ({this_season}) --")
    champions_new_rides = driver_champ.drives.filter(season = this_season)

    cn = None
    if champions_new_rides:
        new_ride = champions_new_rides[0]
        print(f"{driver_champ} drives for {new_ride.team}")
        print(f"{new_ride.team} gets #1")
        cn = CarNumber.objects.create(season = this_season, team = new_ride.team, number = 1)
    else:
        print("The reigning champion is not driving this season! Give #0 to the constructors champ")
        cn = CarNumber.objects.create(season = this_season, team = prev_season.constructors_champion, number = 0)

    return cn

def numbers_1996(this_season, prev_season):
    # Reigning driver's champion gets #1 on his current car
    # All other teams get numbers based on constructor's standings        
    this_season = Season.objects.get(year=year)
    prev_season = this_season.prev
    driver_champ = prev_season.drivers_champion
    driver_champ_team = prev_season.drivers_champion_team
    champions_new_ride = driver_champ.drives.get(season = this_season)
    
    
    print(f"-- Reigning (won in {prev_season}) --")
    print(f"Driver: {driver_champ} for {driver_champ_team}")
    print(f"Constructor: {prev_season.constructors_champion}")

    print(f"-- This Season ({year}) --")
    print(f"{champions_new_ride.driver} drives for {champions_new_ride.team}")
    print(f"{champions_new_ride.team} gets #1")

def numbers_1973_1995(this_season, prev_season):
    # Reigning driver's champion gets #1 on his current car, swaps with previous #1
    # If reigning champion has no drive, the constructor's champ gets #0

    cn_unsaved = champ_gets_number1(this_season, prev_season)

    driver_champ_team = prev_season.drivers_champion_team    
    old_number = driver_champ_team.car_numbers(prev_season)

    if cn_unsaved:
        print(f"Gives away {cn_unsaved.team}'s {prev_season} numbers {old_number} to the team that had #1 in {prev_season}")

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
        if ent == cn_unsaved.team :
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

    this_season = Season.objects.get(year=year)
    prev_season = this_season.previous()

    if year < 1996:
        numbers_1973_1995(this_season, prev_season)
    else:
        numbers_1996(this_season, prev_season)

if __name__ == "main":
    run()
"""Set car numbers based on regulations"""

from django.db import IntegrityError
from f1web.models import CarNumber, Season

# runscript set_car_numbers --script-args 1983

def champ_gets_number1(this_season, prev_season):
    champ = prev_season.drivers_champion

    print(f"-- Reigning driver's champ (won in {prev_season}) is {champ}")
    # print(f"-- This Season ({this_season}) --")
    champions_new_rides = champ.drives.filter(season = this_season)

    number_one = None

    if champions_new_rides:
        new_ride = champions_new_rides[0]   #just assuming
        print(f"-- This season he drives for {new_ride.team}")
        print(f"{new_ride.team} gets #1")

        number_one = CarNumber.objects.filter(season = this_season, team = new_ride.team)
        if number_one:
            number_one = number_one[0]
            if number_one.number != 1:
                print(f"Car Number for the reigning champ exists, but it's not 1, it's {number_one.number}! We will fix it.") 
                number_one.number = 1
        else:
            number_one = CarNumber(season = this_season, team = new_ride.team, number=1)

    else:
        print("The reigning champion is not driving this season! Give #0 to the constructors champ")
        number_one = CarNumber(season = this_season, team = prev_season.constructors_champion, number = 0)

    return number_one

def numbers_1996(this_season, prev_season):
    # From 1996, Reigning driver's champion gets #1 on his current car
    # All other teams get numbers based on constructor's standings        
    this_season = Season.objects.get(year=this_season)
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
    # Reigning driver's champion gets #1 on his current car, swaps with previous holder of #1
    # If reigning champion has no drive, the constructor's champ gets #0

    number_1 = champ_gets_number1(this_season, prev_season)
    # number_1.save()
    driver_champ_team = prev_season.drivers_champion_team

    # There are three teams we need to identify, they may overlap
    # - the team the reigning champ drove for last season.
    # - the team the reigning champ drives for this season, they will wear #1 this season. May be none
    # - the team that wore #1 last season

    ## Driver for non-winning team wins and switches to non-winning team
    # 87 Piquet won for Williams with #5
    # 88 Piquet goes to Lotus with #1
    # Lotus gives its #11 to McLaren which is losing #1 that it wore in 87
    # Williams retains #5

    ## Driver for winning team wins and switches to non-winning team
    # 89 Prost won for McLaren with #1
    # 90 Prost goes to Ferrari with #1
    # Ferrari gives its #27 to McLaren which is losing #1 that it wore in 89

    ## Driver for non-winning team wins and retires
    # 92 Mansell won for Williams with #5
    # 93 Mansell retires, Williams gets #0/2
    # Special case - McLaren, which had #1 in 92, decides to take Brabham's vacated 7/8 instead of Williams 5/6, letting Benetton have them.

    ## Driver for winning team wins and retires
    # 93 Prost won for Williams with #2
    # 94 Prost retires, Williams gets #0/2


    # old_number = driver_champ_team.car_numbers(prev_season)

    old_number = number_1.team.car_numbers(prev_season)

    if old_number and old_number[0] < 2:
        print("The champ's team for this season had #1 the previous season, no swapping needed")

    if number_1:
        print(f"Gives away {number_1.team}'s {prev_season} numbers {old_number} to the team that had #1 in {prev_season}")

    old_1 = None
    try:
        old_1 = CarNumber.objects.get(season=prev_season, number__lt = 2)
        print(f"{old_1.team}")
        
        try:
            cn_old_1 = CarNumber(season=this_season, number = old_number[0], team = old_1.team)
            print(f"The newly created CarNumber object: {cn_old_1}")
            cn_old_1.save()
        except IntegrityError:
            print("Already exists")


    except CarNumber.DoesNotExist:
        print(f"Can't find {prev_season} holder of #1")


    print("-- Teams with the same numbers --")
    for ent in this_season.constructors():
        if ent == number_1.team :
            print(f"Skipping {ent}, new #1")
            continue
        if ent == driver_champ_team :
            print(f"Skipping {ent}, champ's team last year")
            continue
        try:
            prev_num = CarNumber.objects.get(team = ent, season = prev_season)
            this_num = CarNumber.objects.filter(team = ent, season = this_season)
            
            if this_num:
                print(f"{ent} already has number for {this_season}! : {this_num[0].number}")
            else:
                cn = CarNumber(season = this_season, team = ent, number = prev_num.number)
                print(f"{ent}: {prev_num.number} -> {cn.number}")
                cn.save()
        except CarNumber.DoesNotExist:
            print(f"No numbers for {ent} in {prev_season}")

def run(*args):
    if len(args) < 1:
        print("Please specify a year after --script-args")
        return
    
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
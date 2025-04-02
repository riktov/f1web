from f1web.models import Constructor, Driver, DrivingContract, Season

def prompt_overlapping(drives):
    drive=drives[0]
    print(f"{drive.driver} drove in {drive.season} for ")

    num = 1

    for dr in drives:
        print(f"{num}) {dr.team} - {dr.starting_round}")
        num = num+1

    resp = input("Enter a number to change the starting round, or N\n")
    if resp.lower() == 'n':
        return
    
    selected_num = int(resp)
    drive = drives[selected_num - 1]

    print(drive)
    resp = input("Enter a new starting round\n")
    starting = int(resp)

    drive.starting_round = starting
    drive.save()


def overlapping_stints():
    """Find cases where one driver has multiple drives in a season (for different teams or even the same), 
    and they do not have different starting rounds"""
    for driver in Driver.objects.all():
        all_drives = driver.drives.all()

        if len(all_drives) > 1:
            for season in driver.seasons:
                drives_in_season = DrivingContract.objects.filter(season = season, driver = driver)
                if len(drives_in_season) > 1:
                    starting_rounds = { dr.starting_round for dr in drives_in_season }
                    if len(starting_rounds) != len(drives_in_season):
                        prompt_overlapping(drives_in_season)

                        # print(driver, season)
                        # for dr in drives_in_season:
                            # print(' -', dr.team, dr.starting_round)

                        # print(drives_in_season)
                    # print("\n")

def prompt_overlapping_seats(drives):
    counter = 1
    for drive in drives:
        print(f"{counter}) {drive}")
        counter = counter + 1
    
    resp = input("Enter a number or N\n")

    if resp.lower() == 'n':
        return 
    
    idx = int(resp) - 1
    drive = drives[idx]
    print(drive)

    resp = input("Enter a starting round\n")
    drive.starting_round = int(resp)
    drive.save()

def overlapping_seats():
    """Find cases where multiple drivers are on the same team, season, place (1/2), and starting round. 
    They must have different starting round or place"""
    cons = Constructor.objects.all()

    for season in Season.objects.all():
        for team in cons:
            for is_lead in [True, False]:
                drives = DrivingContract.objects.filter(season=season, team=team, is_lead=is_lead)        
                if len(drives) > 1:
                    starting_rounds = [dc.starting_round for dc in drives]
                    if all(s == starting_rounds[0] for s in starting_rounds):
                        prompt_overlapping_seats(drives)
                        # print(" -- ")
                        # for dc in drives:
                        #     # pass
                        #     print(f"   {dc}")

    return 
    for driver in Driver.objects.all():
        all_drives = driver.drives.all().order_by('season')

        if len(all_drives) > 1:
            for drive in all_drives:
                overlapping_drives = DrivingContract.objects.filter(season = drive.season, team=drive.team, starting_round=drive.starting_round, is_lead=drive.is_lead).exclude(driver = driver)
                if overlapping_drives:
                    print(f"Overlapping Seats for {driver}:")

                    for od in overlapping_drives:
                        print(f"  {drive}")
                        print(f"  {od}")

def run():
    print("housecleaning script") 
    overlapping_seats()
    overlapping_stints()

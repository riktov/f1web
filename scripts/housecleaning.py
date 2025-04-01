from f1web.models import Driver, DrivingContract

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
    """Find cases where one driver has multiple drives in a season (for different teams), 
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

def run():
    print("housecleaning script") 
    overlapping_stints()

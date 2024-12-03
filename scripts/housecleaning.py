from f1web.models import Driver, DrivingContract


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
                        print(drives_in_season)
                    # print("\n")

def run():
    print("housecleaning script") 
    overlapping_stints()

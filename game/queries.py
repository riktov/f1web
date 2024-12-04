from f1web.models import DrivingContract


def teammates_in_season(driver, season):
    ds = driver.drives.filter(season=season)
    
    all_teammates = []

    for d in ds:
        teammate_dcs = DrivingContract.objects.filter(season = d.season, team=d.team)
        teammate_dcs = teammate_dcs.exclude(driver = driver)
        for tm in teammate_dcs:
            all_teammates.append(tm.driver)

    return all_teammates

def teammates_all(driver):
    all_teammates = set()

    seasons = driver.seasons

    for season in seasons:
        teammates = teammates_in_season(driver, season)
        for tm in teammates:
            all_teammates.add(tm)

    return all_teammates
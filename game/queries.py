from f1web.models import DrivingContract


def teammates_in_season(driver, season):
    ds = driver.drives.filter(season=season)
    
    all_teammates = []

    for d in ds:
        teammate_dcs = DrivingContract.objects.filter(season = d.season, team=d.team).exclude(driver = driver)
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

def teamings(driver1, driver2):
    """Return the seasons and teams in which the two drivers were teamed"""
    #get the intersection of both drivers' seasons
    common_seasons = driver1.seasons & driver2.seasons

    teamups = []

    for s in common_seasons:
        #get driver1's teams for this year
        this_season_drives = DrivingContract.objects.filter(season = s)

        d1_teams = { dc.team for dc in this_season_drives.filter(driver = driver1)}
        d2_teams = { dc.team for dc in this_season_drives.filter(driver = driver2)}

        common_teams = d1_teams & d2_teams
        if common_teams:
            teamups.append([s, list(common_teams)])
        
    #for each of those seasons, get all drives with either driver
    #find common teams
    
    return teamups
    

from f1web.models import Driver, DrivingContract

def run():
    print("This is the convert driveto contract")

    drivers = Driver.objects.all()

    for driver in drivers:
        print(driver)
        drives = driver.drives.all()
        
        for drive in drives:
            contract = DrivingContract(season = drive.year, team = drive.team, driver=driver)
            contract.save()


if __name__ == "main":
    run()
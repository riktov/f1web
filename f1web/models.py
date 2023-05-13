"""The core models are defined here"""

from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.


class EngineMaker(models.Model):
    """Engine Maker, examples: Honda, Ford"""
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class Engine(models.Model):
    """examples: BWM Turbo 4 cyl"""
    maker = models.ForeignKey(EngineMaker, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True)
    # displacement = models.IntegerField(default=3000)
    # cylinders = models.IntegerField(default=6)
    # configuration = inline, flat, v
    # is_turbo

    class Meta:
        ordering = ('maker', 'name',)

    def __str__(self):
        return self.maker.name + " " + self.name
        # return "%s %s %s cylinder" % (self.maker, self.name, self.cylinders)

class Constructor(models.Model):
    """A Formula 1 constructor (team)"""
    name = models.CharField(max_length=64, unique=True,
                            blank=False, null=False)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 32, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    @property
    def cars(self):
        """return all the cars that this Constructor has raced"""
        all_cars = Car.objects.filter(constructor=self)

        cars_with_year = [
            car for car in all_cars if car.earliest_season is not None]
        cars_without_year = [
            car for car in all_cars if car.earliest_season is None]

        return sorted(cars_with_year, key=lambda c: c.earliest_season.year) + cars_without_year

    def cars_in_year(self, year):
        """return all the cars that this Constructor has raced in the specified year"""
        return Season.objects.get(year=year).cars.filter(constructor=self)

    def drivers_in_year(self, year):
        """return all the drivers that have driven for this Constructor in the specified year"""
        drives = self.drives.get(year=year, team=self)

        if not drives:
            return []
        return drives.drivers()

class TeamManager(models.Model):
    """The person who manages the Constructor, e.g., Ron Dennis, Bernie Ecclestone"""
    name = name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class Car(models.Model):
    """A Formula 1 Car"""
    name = models.CharField(max_length=64, blank=False)
    constructor = models.ForeignKey(
        Constructor, on_delete=models.SET_NULL, null=True)
    engine = models.ForeignKey(
        Engine, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length = 64, blank=True, null=True)

    def __str__(self):
        if self.constructor:
            return self.constructor.name + " " + self.name
        return self.name

    class Meta:
        ordering = ('constructor', 'name')
        unique_together = ('constructor', 'name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Car, self).save(*args, **kwargs)

    @property
    def season_list(self):
        """A list of the seasons in which this car raced"""
        return Season.objects.filter(cars=self)

    @property
    def earliest_season(self):
        """Return the first season in which this car raced"""
        seasons = self.season_list
        if seasons:
            return seasons[0]
        else:
            return None

    @property
    def wikipedia_link(self):
        """Returns the Wikipedia link for this car"""
        return f"https://en.wikipedia.org/wiki/{self}"

    @property
    def seasons_and_drivers_list(self):
        """Return a list of years and drivers of this car"""
        seasons_and_drivers = []

        #NOTE: constructor is None.
        print(f"Hey, I am {self}. My team is {self.constructor}.")
        
        drives = DrivingContract.objects.all()
        print(f"All drives: {drives}")


        for season in self.season_list:

            print(f"filtered on {season} season and constructor {self.constructor}")
            drives = DrivingContract.objects.filter(season = season, team = self.constructor)
            

            for drive in drives:
                print(f"{drive}")

            line = [
                season,
                [ drive.driver for drive in drives ]
            ]
            seasons_and_drivers.append(line)

        return seasons_and_drivers
    

class Season(models.Model):
    """Season contains only cars, because we can get everything else ---
    teams, drivers, etc., from cars
    """
    year = models.IntegerField(
        primary_key=True, default=1980, blank=False, unique=True)
    cars = models.ManyToManyField(Car, blank=True)

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return str(self.year)

    @property
    def car_list(self):
        """A list of cars that raced in this season"""
        if self.cars:
            return self.cars.all()
        else:
            return []

    @property
    def car_and_driver_list(self):
        """Return a list of cars and drivers (of all teams) in this season"""
        teams = [car.constructor for car in self.car_list]
        team_car_drivers = []

        # drive = self.drives.filter(season=self)

        for team in Constructor.objects.all():
            try:
                drives = self.drives.filter(season=self, team=team)
                if drives:
                    drivers = [drive.driver for drive in drives]
                    team_dict = {
                        "team": team,
                        "cars": self.car_list.filter(constructor=team),
                        "drivers": drivers
                    }
                    team_car_drivers.append(team_dict)
            except DrivingContract.DoesNotExist:
                pass

        return team_car_drivers

#################

        # drives = Drive.objects.filter(year=self.year)
        # for drive in drives:
        #     team = drive.team
        #     # year = drive.year

        # c_and_d = [(dr, dr.drivers()) for dr in drives]
        # return c_and_d

    @property
    def previous(self):
        """The year before this one"""
        return Season.objects.filter(year__lt=self.year).last

    @property
    def next(self):
        """The year after this one"""
        return Season.objects.filter(year__gt=self.year).first

    @property
    def wikipedia_link(self):
        """Returns the Wikipedia link for this season"""
        this_year = self.year
        return f"https://en.wikipedia.org/wiki/{this_year}_Formula_One_World_Championship"

# class Drive(models.Model):
#     """A Drive represents participation, for a year with a team"""
#     team = models.ForeignKey(Constructor, on_delete=models.CASCADE, blank=False, null=False)
#     year = models.ForeignKey(Season, on_delete=models.CASCADE, blank=False, null=False)

#     class Meta:
#         unique_together = (("team", "year"),)
#         ordering = ('year', 'team')

#     def __str__(self):
#         return  str(self.year) + " " + self.team.name

#     def drivers(self):
#         """Return the drivers who have had this Drive"""
#         return Driver.objects.filter(drives = self)


class Driver(models.Model):
    """A Driver participates in Drives"""
    name = models.CharField(max_length=256)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 64, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    @property
    def drives_list(self):
        return self.drives.all()

    def __str__(self):
        return str(self.name)


class DrivingContract(models.Model):
    """A driving gig, containing a season, team, and driver"""
    season = models.ForeignKey(
        Season, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')
    team = models.ForeignKey(Constructor, blank=False, null=False,
                             on_delete=models.CASCADE, related_name='drives')
    driver = models.ForeignKey(
        Driver, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')

    class Meta:
        ordering = ('season', 'team', 'driver',)
        unique_together = ('season', 'team', 'driver')

    def __str__(self):
        return f"{self.season} for {self.team} by {self.driver}"

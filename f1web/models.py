"""The core models are defined here"""

from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.

### Models which do not reference other f1web models
class EngineMaker(models.Model):
    """Engine Maker, examples: Honda, Ford"""
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length = 32, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

class Driver(models.Model):
    """A Driver"""
    name = models.CharField(max_length=256)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 64, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    @property
    def drives_list(self):
        return self.drives.all()

    def team_in_season(self, season):
        teams = [dc.team for dc in DrivingContract.objects.filter(driver = self, season=season)]

    def car_number_in(self, season, team):
        dc = DrivingContract.objects.get(driver = self, season=season, team= team)
        return dc.car_number

    def __str__(self):
        return str(self.name)
    
class Constructor(models.Model):
    """A Formula 1 constructor (team)"""
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 32, blank=True, null=True)
    # predecessor = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    @property
    def cars(self):
        """return all the cars that this Constructor has raced"""
        all_cars = Car.objects.filter(constructor=self)

        cars_with_season = [
            car for car in all_cars if car.earliest_season() is not None]
        cars_without_season = [
            car for car in all_cars if car.earliest_season() is None]

        return sorted(cars_with_season, key=lambda c: c.earliest_season().year) + cars_without_season

    def cars_in_season(self, season):
        """return all the cars that this Constructor has raced in the specified season"""
        return season.cars.filter(constructor=self)

    def drivers_in_season(self, season):
        """return all the drivers that have driven for this Constructor in the specified season"""
        drives = self.drives.filter(season=season, team=self)

        if not drives:
            return []
        return [drive.driver for drive in drives]
    
    def seasons(self):
        return Season.objects.filter(cars__constructor = self).distinct() 

    def seasons_and_cars_and_drivers(self):
        return [(s, s.cars.filter(constructor = self), self.drivers_in_season(s)) for s in self.seasons() ]
    
    def full_name_in_season(self, season):
        "Combination of chassis and engine, e.g., McLaren-Honda, Benetton-Ford"
        return self.name()

    def car_number(self, season):
        dc = DrivingContract.objects.filter(team = self, season=season, car_number__isnull=False)
        if dc:
            num = dc.first().car_number
            if num % 2 == 0:
                num = num - 1
            return num
        return None

class TeamManager(models.Model):
    """The person who manages the Constructor, e.g., Ron Dennis, Bernie Ecclestone"""
    name = name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)

### Models which reference other f1web models
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

    def earliest_season(self):
        """Return the first season in which this car raced"""
        seasons = self.season_list
        if seasons:
            return seasons[0]
        return None

    @property
    def seasons_and_drivers_list(self):
        """Return a list of years and drivers of this car"""
        seasons_and_drivers = []

        #NOTE: constructor is None.
        
        drives = DrivingContract.objects.all()

        for season in self.season_list:
            drives = DrivingContract.objects.filter(season = season, team = self.constructor)
            
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
    drivers_champion = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    constructors_champion = models.ForeignKey(Constructor, null=True, blank=True, on_delete=models.SET_NULL)
    
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
    def xxxcar_and_driver_list(self):
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

    @property
    def previous(self):
        """The season before this one"""
        return Season.objects.filter(year__lt=self.year).last

    @property
    def next(self):
        """The season after this one"""
        return Season.objects.filter(year__gt=self.year).first
    
    @property 
    def drivers_champion_team(self):
        teams = [ dc.team for dc in DrivingContract.objects.filter(season=self, driver=self.drivers_champion)]
        return teams[0]

    @property
    def is_double_champion(self):
        #need to compare id. "is" comparison with Constructor objects doesn't work
        if self.drivers_champion and self.constructors_champion :
            return self.drivers_champion_team.id == self.constructors_champion.id
        return False

class DrivingContract(models.Model):
    """A driving gig, containing a season, team, and driver"""
    season = models.ForeignKey(
        Season, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')
    team = models.ForeignKey(Constructor, blank=False, null=False,
                             on_delete=models.CASCADE, related_name='drives')
    driver = models.ForeignKey(
        Driver, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')
    car_number = models.IntegerField(null=True, blank=True)
    # is_lead = models.BooleanField(default=False)

    class Meta:
        ordering = ('season', 'team', 'driver',)
        unique_together = ('season', 'team', 'driver')

    def __str__(self):
        return f"{self.season} for {self.team} by {self.driver}"

class CarNumber(models.Model):
    """The lead number (lower of two, always odd) assigned to a constructor for one season"""
    # Handle Damon Hill #0
    season = models.ForeignKey(Season, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Constructor, blank=False, null=False, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
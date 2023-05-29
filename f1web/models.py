"""The core models are defined here"""

from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.

class NameModelManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name = name)
    
### Models which do not reference other f1web models
class EngineMaker(models.Model):
    """Engine Maker, examples: Honda, Ford"""
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length = 32, blank=True, null=True, unique=True)

    objects = NameModelManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def natural_key(self):
        return (self.name,)

 
class Driver(models.Model):
    """A Driver"""
    name = models.CharField(max_length=256)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 64, blank=True, null=True, unique=True)

    objects = NameModelManager()

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return str(self.name)
    
    def natural_key(self):
        return (self.name,)

    @property
    def drives_list(self):
        return self.drives.all()

    def team_in(self, season):
        teams = [dc.team for dc in DrivingContract.objects.filter(driver = self, season=season)]

    def is_lead_in(self, season, team):
        dcs = self.drives.filter(season = season, team=team)
        if dcs:
            return dcs[0].is_lead
        return False

    def car_number_in(self, season, team):
        dc = self.drives.get(season = season, team=team)
        # dc = DrivingContract.objects.get(driver = self, season=season, team= team)

        cn = team.car_numbers(season=season)
        if cn:
            if dc.is_lead:
                return cn[0]
            else:
                return cn[1]

        return None
    
    @property 
    def seasons(self):
        return { dr.season for dr in self.drives.all() }
    
    @property
    def season_range(self):
        se = self.seasons
        if se:
            ss = sorted(se, key=lambda s:s.year)
            return(ss[0], ss[-1])
        return None
    
class Constructor(models.Model):
    """A Formula 1 constructor (team)"""
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    country = CountryField(null=True)
    slug = models.SlugField(max_length = 32, blank=True, null=True)
    is_factory = models.BooleanField(default=False) #Constructor full (season) name
    # predecessor = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)

    objects = NameModelManager()
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def natural_key(self):
        return (self.name,)
    
    def cars_ordered_by_season(self):
        """return all the cars that this Constructor has raced"""
        all_cars = self.car_set.all()
        #Car.objects.filter(constructor=self)

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
        drives = self.drives.filter(season=season)

        if not drives:
            return []
        return [drive.driver for drive in drives]
    
    def seasons(self):
        return Season.objects.filter(cars__constructor = self).distinct() 

    def seasons_and_cars_and_drivers(self):
        return [(s, self.car_set.filter(season=s), self.drivers_in_season(s)) for s in self.seasons() ]
    
    def full_name(self, season):
        """Combination of chassis and engine, e.g., McLaren-Honda, Benetton-Ford"""
        return self.name

    def car_numbers(self, season):
        # cn = CarNumber.objects.get(team = self, season=season)
        try:
            cn = self.carnumber_set.get(season=season)
            return cn.pair()
        except CarNumber.DoesNotExist:
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

    def natural_key(self):
        return (self.maker.name, self.name)

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

    def natural_key(self):
        return (self.constructor.name, self.name)
    
    class Meta:
        ordering = ('constructor', 'name')
        unique_together = ('constructor', 'name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Car, self).save(*args, **kwargs)

    def earliest_season(self):
        """Return the first season in which this car raced"""
        seasons = self.season_set.all()
        if seasons:
            return seasons[0]
        return None

    def seasons_and_drivers_table(self):
        """Return a table of years and drivers of this car"""
        seasons_and_drivers = []

        #NOTE: constructor is None.
        
        # drives = DrivingContract.objects.all()

        for season in self.season_set.all():
            # drives = season.drives.filter(team = self.constructor)
            
            row = [
                season,
                [ drive.driver for drive in season.drives.filter(team = self.constructor) ]
            ]
            seasons_and_drivers.append(row)

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
    def xxxcar_list(self):
        """A list of cars that raced in this season"""
        if self.cars:
            return self.cars.all()
        else:
            return []

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
        teams = [ dc.team for dc in self.drives.filter(driver=self.drivers_champion)]
        # teams = [ dc.team for dc in DrivingContract.objects.filter(season=self, driver=self.drivers_champion)]
        return teams[0]

    @property
    def is_double_champion(self):
        """Did we win the constructor's title and one of our drives won the driver's title?"""
        if self.drivers_champion and self.constructors_champion :
            return self.drivers_champion_team == self.constructors_champion
        return False
    
    def constructors(self):
        teams_with_cars = { car.constructor for car in self.cars.all() }
        teams_with_drivers = { dr.team for dr in self.drives.all() }
        teams_with_numbers = { cn.team for cn in self.carnumber_set.all() }

        return teams_with_cars.union(teams_with_drivers, teams_with_numbers)


class DrivingContract(models.Model):
    """A driving gig, containing a season, team, and driver"""
    season = models.ForeignKey(
        Season, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')
    team = models.ForeignKey(Constructor, blank=False, null=False,
                             on_delete=models.CASCADE, related_name='drives')
    driver = models.ForeignKey(
        Driver, blank=False, null=False, on_delete=models.CASCADE, related_name='drives')
    # car_number = models.IntegerField(null=True, blank=True)
    is_lead = models.BooleanField(default=False)

    class Meta:
        ordering = ('season', 'team', '-is_lead', 'driver',)
        unique_together = ('season', 'team', 'driver')

    def __str__(self):
        lead = ''
        if self.is_lead:
            lead = '+'
        return f"{self.season} for {self.team} by {self.driver}{lead}" 
    
    @property
    def is_champion(self):
        return self.season.drivers_champion == self.driver

class CarNumber(models.Model):
    """The lead number (lower of two consecutive) assigned to a constructor for one season"""
    #normally odd, but in some cases even: 1981 Fittipaldi and Alfa Romeo, 1993 Williams (special case)
    season = models.ForeignKey(Season, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Constructor, blank=False, null=False, on_delete=models.CASCADE)
    number = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ('season', 'number',)
        unique_together = ('season', 'team', )
    
    def __str__(self):
        return f"{self.season} {self.number} {self.team}"
    
    def pair(self):
        """Return a tuple of the two car numbers"""
        #damonhill
        if self.number == 0:
            return (0, 2,)
        return(self.number, self.number + 1,)
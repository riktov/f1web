"""The core models are defined here"""

from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.

class NameModelManager(models.Manager):
    """model manager for various model classes, allows getting by name"""
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

    def team_in(self, season):
        teams = [dc.team for dc in self.drives.filter(season=season)]
        return teams

    def teams_in(self, season):
        team_ids = [dc.team.id for dc in self.drives.filter(season = season)]
        return Constructor.objects.filter(pk__in = team_ids)
    
    def teammates(self):
        mate_driver_ids = []

        for team, season in [(dr.team, dr.season) for dr in self.drives.all() ]:
            mate_drives = DrivingContract.objects.filter(team=team, season=season).exclude(driver=self)
            for md in mate_drives:
                mate_driver_ids.append(md.driver.id)
        
        return Driver.objects.filter(pk__in = mate_driver_ids)

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
        return Season.objects.filter(year__in = [dc.season.year for dc in self.drives.all()])
    
    @property
    def season_range(self):
        se = self.seasons
        return [se.first(), se.last()]
    
    def last_drive_before(self, season):
        prev_season_drives = self.drives.filter(season__lt = season)
        if not prev_season_drives:
            return None
        
        return prev_season_drives.order_by('season', 'starting_round').last()

    def history(self, season):
        """Return this driver's team(s) at the end of previous season, if different
        total seasons (up to this one) in this team. So earlier stints do not count
        total seasons (including this one) in F1
        """
        this_season_teams = [ dr.team for dr in self.drives.filter(season = season).order_by('starting_round') ]
        
        # prev_seasons = {dr.season for dr in self.drives.filter(season__lt = season)}
        last_drive = self.last_drive_before(season)

        if not last_drive:
            #rookie
            return [ this_season_teams, None , 1, 1]

        prev_seasons = { dr.season for dr in self.drives.filter(season__lt = season) }

        # continuing from previous season
        if last_drive.team in this_season_teams:
            se = season
            current_stint = 1 
            while se.previous() and self.drives.filter(season=se.previous(), team=last_drive.team):
                current_stint = current_stint + 1
                se = se.previous()
            return [ this_season_teams, None, current_stint, len(prev_seasons) + 1]

        #TODO: but could be from the same team renamed

        #moved from another team
        return [ this_season_teams, last_drive.team,  1, len(prev_seasons) +1 ]

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

    def drivers_in_season(self, season):
        """return all the drivers that have driven for this Constructor in the specified season"""
        driver_ids = [dc.driver.id for dc in self.drives.filter(season=season)]
        return Driver.objects.filter(pk__in = driver_ids)
    
    def seasons(self):
        return Season.objects.filter(cars__constructor = self).distinct() 

    def seasons_and_cars_and_drivers(self):
        return [(s, self.car_set.filter(season=s), self.drivers_in_season(s), self.car_numbers(s)) for s in self.seasons() ]
    
    def full_name(self, season):
        """Combination of chassis and engine, e.g., McLaren-Honda, Benetton-Ford"""
        # For factory constructors we can omit the engine. 
        # We currently do this in the season detail page template, based on the is_factory flag
        # But there are also some non-factories that built their own engines for some seasons.
        # So we should also check if the constructor name is the same as the engine maker name
        # and omit the engine if so.
        return self.name

    def car_numbers(self, season):
        # cn = CarNumber.objects.get(team = self, season=season)
        try:
            cn = self.carnumber_set.get(season=season)
            return cn.pair()
        except CarNumber.DoesNotExist:
            return None
  
    def previous_identity(self, season):
        prev_transfers=ConstructorTransfer.objects.filter(new=self, season__lte=season)
        if not prev_transfers:
            return None
        return prev_transfers.last().previous



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
    
    def earliest_season(self):
        seasons = [car.earliest_season() for car in self.car_set.all() if car.earliest_season() is not None ]

        if seasons:
            return sorted(seasons)[0]
        return None

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
    year = models.PositiveSmallIntegerField(
        primary_key=True, default=1980, blank=False, unique=True)
    cars = models.ManyToManyField(Car, blank=True)
    drivers_champion = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    constructors_champion = models.ForeignKey(Constructor, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ('year',)

    def __str__(self):
        return str(self.year)


    def __lt__(self, other):
        return self.year < other.year
    
    def __gt__(self, other):
        return self.year > other.year
    
    def __eq__(self, other):
        return other and self.year == other.year

    #seems this is also needed if we add the above
    def __hash__(self):
        return self.year

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
        """The team that reigning driver's champion drove for in the previous season"""
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
        team_ids_with_cars = {car.constructor.id for car in self.cars.all()}
        team_ids_with_drivers = {dr.team.id for dr in self.drives.all()}
        team_ids_with_numbers = {cn.team.id for cn in self.carnumber_set.all()}
        
        return Constructor.objects.filter(id__in = team_ids_with_cars | team_ids_with_drivers | team_ids_with_numbers)

    def drivers(self):
        return Driver.objects.filter(id__in = { dc.driver.id for dc in self.drives.all()})

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
    starting_round = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ('season', 'team', '-is_lead', 'driver',)
        unique_together = ('season', 'team', 'driver', 'is_lead')

    def __str__(self):
        lead = ''
        if self.is_lead:
            lead = '+'
        return f"{self.season} ({self.starting_round}-) for {self.team} by {self.driver}{lead}" 
    
    @property
    def is_champion(self):
        return self.season.drivers_champion == self.driver
    
    @property
    def number(self):
        car_number = CarNumber.objects.get(team = self.team, season = self.season)
        if car_number:
            if self.is_lead:
                return car_number.pair()[0]
            else:
                return car_number.pair()[1]
        else:
            return None
    
    @property
    def is_maybe_lead(self):
        teammate_drives = DrivingContract.objects.filter(season = self.season, team = self.team).exclude(driver = self.driver)
        teammate_leads = teammate_drives.filter(is_lead = True)
        return not self.is_lead and len(teammate_leads) < 1
        # return teammate_drives
        # return true if none of these is_lead


class CarNumber(models.Model):
    """The lead number (lower of two consecutive) assigned to a constructor for one season"""
    #normally odd from 0 to 11, then even after skipping 13
    season = models.ForeignKey(Season, blank=False, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Constructor, blank=False, null=False, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(blank=False, null=False)
    span = models.PositiveSmallIntegerField(default=2)

    class Meta:
        ordering = ('season', 'number',)
        unique_together = [['season', 'number'], ['season', 'team']]
    
    def __str__(self):
        return f"{self.season} {self.number} {self.team}"
    
    def pair(self):
        """Return a tuple of the two car numbers"""
        #Damon Hill
        if self.number == 0:
            return (0, 2,)
        if self.span == 1:
            return(self.number)
        return(self.number, self.number + 1,)
    
class Rule(models.Model):
    """A rule which affects the cars or engines"""
    season = models.ForeignKey(Season, blank=False, null=False, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=False)

    def __str__(self):
        return f"{self.season} {self.description}"

    class Meta:
         ordering = ('season',)

class ConstructorTransfer(models.Model):
    previous = models.ForeignKey(Constructor, blank=False, null=False, on_delete=models.DO_NOTHING, related_name='subsequently')
    new = models.ForeignKey(Constructor, blank=False, null=False, on_delete=models.DO_NOTHING, related_name='previously')
    season = models.ForeignKey(Season, blank=False, null=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.previous} to {self.new} in {self.season}"
    
    class Meta:
         ordering = ('season',)

class PermanentSet(models.Model):
    """A fixture class defining a set that other objects can be a permanent member of
    This is so we can create a permanent set of countries that have certain unchanging characteristics
    That would require a lengthy query to retrieve dynamically.
    """
    set_name = models.CharField(max_length=64, blank=False, null=False)
    set_description = models.CharField(max_length=64, blank=True, null=True)
    def __str__(self) -> str:
        return self.set_name

class PermanentSetCountry(models.Model):
    """A class indicating that this country is a member of the PermanentSet
    """
    set = models.ForeignKey(PermanentSet, related_name='countries', on_delete=models.CASCADE)
    country = CountryField()
    def __str__(self) -> str:
        return f"{self.country} in {self.set}"
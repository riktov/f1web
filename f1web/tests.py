"""Tests for the models"""
from django.test import TestCase

# Create your tests here.
from f1web.models import Car, Engine, EngineMaker, Season, Driver, DrivingContract, Constructor

from browse.templatetags import sort as templatetag_sort

class CarTest(TestCase):
    "class for testing Car model"
    def setUp(self):
        self.team = Constructor.objects.create(name="FooBar")

        enginemaker = EngineMaker.objects.create(name="Empire")

        engine1 = Engine.objects.create(name="e1", maker=enginemaker)
        engine2 = Engine.objects.create(name="e2", maker=enginemaker)
        engine3 = Engine.objects.create(name="e3", maker=enginemaker)
        engine4 = Engine.objects.create(name="e4", maker=enginemaker)

        car1 = Car.objects.create(name = "FB1", constructor = self.team, engine=engine1)
        car2 = Car.objects.create(name = "FB2", constructor = self.team, engine=engine2)
        car3 = Car.objects.create(name = "FB3", constructor = self.team, engine=engine3)
        car4 = Car.objects.create(name = "FB4", constructor = self.team, engine=engine4)
        car5 = Car.objects.create(name = "FB5", constructor = self.team, engine=engine3)

        s70 = Season.objects.create(year = 1970)
        s80 = Season.objects.create(year = 1980)
        s90 = Season.objects.create(year = 1990)

        s90.cars.add(car2)
        s90.cars.add(car3)
        s70.cars.add(car2)
        s70.cars.add(car1)
        # s80.cars.add(car2)

        alex = Driver.objects.create(name="Alex")
        bob = Driver.objects.create(name="Bob")
        chris = Driver.objects.create(name="Chris")

        DrivingContract.objects.create(season=s70, driver=bob, team=self.team)
        DrivingContract.objects.create(season=s80, driver=chris, team=self.team)
        DrivingContract.objects.create(season=s90, driver=alex, team=self.team)

        # print(car1.constructor)
        self.car_with_no_season = car4


        self.engine_in_multiple_cars = engine3  #in car 3 which has one season, and car 4 which has no seasons
        self.engine_with_no_season = engine4
        self.engine_with_season = engine2
        


    def test_car_earliest_season(self):
        """Test that car's earliest season is valid, 
        regardless of how they are ordered in the DB"""

        constructor = Constructor.objects.first()
        engine = Engine.objects.first()
        car = Car.objects.create(constructor=constructor, engine=engine)

        s70 = Season.objects.get(year=1970)
        s80 = Season.objects.get(year=1980)
        s90 = Season.objects.get(year=1980)

        s90.cars.add(car)
        s80.cars.add(car)
        s70.cars.add(car)
        
        #car2 has been added to all years, in the order 90, 70, 80
        #so the database order should not have 70 at the head

        self.assertEqual(car.earliest_season(), s70)
    
    def test_car_earliest_season_none(self):
        constructor = Constructor.objects.first()
        engine = Engine.objects.first()
        car = Car.objects.create(constructor=constructor, engine=engine)

        self.assertIsNone(car.earliest_season())

    def test_car_seasons_and_drivers(self):
        s70 = Season.objects.get(year = 1970)
        car2 = Car.objects.get(name = "FB2")
        bob = Driver.objects.get(name = "Bob")
        
        table = car2.seasons_and_drivers_table()

        #1970 Bob
        line = table[0]
        # print(table)
        season = line[0]
        driver_list = line[1]
        self.assertEqual(season, s70)
        self.assertIn(bob, driver_list)

    def test_engine_earliest_season_car_with_no_season(self):
        """An engine used only in a car with no season
        is reported as not having an earliest season"""
        eng = self.car_with_no_season.engine
        season = eng.earliest_season()
        self.assertIsNone(season)

    def test_engine_earliest_season_car_with_no_season_and_car_with_season(self):
        """An engine used in one car with a season and another with no season
        is reported as used in the the season of the first car, without causing an error
        on the second car"""
        season = self.engine_in_multiple_cars.earliest_season()
        self.assertIsNotNone(season)
        self.assertEqual(season.year, 1990)
    
    def test_sort_earliest_seasons(self):
        """A collection of engines can be sorted by earliest_season, even if one of the engines has no seasons;
        in this case it will be placed at the beginning"""
        result = templatetag_sort.sort_by_season([self.engine_with_season, self.engine_with_no_season])

        self.assertIsNone(self.engine_with_no_season.earliest_season())
        self.assertIs(result[0], self.engine_with_no_season)
        self.assertIs(result[1], self.engine_with_season) 

class ConstructorTest(TestCase):
    def setUp(self):
        self.team = Constructor.objects.create(name="FooBar")
        
        alex  = Driver.objects.create(name="Alex")
        bob   = Driver.objects.create(name="Bob")
        chris = Driver.objects.create(name="Chris")

        s80 = Season.objects.create(year = 1980)
        s70 = Season.objects.create(year = 1970)
        s90 = Season.objects.create(year = 1990)

        c70 = Car.objects.create(name="C70", constructor = self.team)
        c80 = Car.objects.create(name="C80", constructor = self.team)

        s70.cars.add(c70)
        s80.cars.add(c80)

        # DrivingContract.objects.create(season=s70, driver=bob, team=self.team)
        # DrivingContract.objects.create(season=s80, driver=chris, team=self.team)
        # DrivingContract.objects.create(season=s90, driver=alex, team=self.team)
    
    def test_constructor_seasons(self):
        seasons = self.team.seasons()
        # print(seasons)
        s70 = Season.objects.get(year=1970)
        self.assertIn(s70, seasons)

class EngineTest(TestCase):
    def setUp(self):
        e1 = Engine.objects.create(name="Engine 1")
        e2 = Engine.objects.create(name="Engine 2")

        self.c1 = Car.objects.create(name="Car 1", engine=e1)
        self.c2 = Car.objects.create(name="Car 2", engine=e2)
    
class DriverTest(TestCase):
    def setUp(self):
        Season.objects.create(year = 1990)
        Season.objects.create(year = 1991)
        Season.objects.create(year = 1992)

        Constructor.objects.create(name="Lotus")
        Constructor.objects.create(name="Benetton")
        Constructor.objects.create(name="Ferrari")
        Constructor.objects.create(name="McLaren")

            
    def test_stint(self):
        nelson = Driver.objects.create(name="Nelson")

        benetton = Constructor.objects.get(name="Benetton")
        lotus = Constructor.objects.get(name="Lotus")

        s90 = Season.objects.get(year=1990)
        s91 = Season.objects.get(year=1991)

        DrivingContract.objects.create(driver=nelson, team=lotus, season=s90)
        DrivingContract.objects.create(driver=nelson, team=benetton, season=s91)

        hist = nelson.history(s91)
        
        self.assertIsNotNone(hist)
        self.assertEqual(hist[2], 2)
    
    def test_last_drive(self):
        nelson = Driver.objects.create(name="Nelson")

        s90 = Season.objects.get(year=1990)
        s91 = Season.objects.get(year=1991)

        benetton = Constructor.objects.get(name="Benetton")
        lotus = Constructor.objects.get(name="Lotus")

        dc90 = DrivingContract.objects.create(driver=nelson, team=lotus, season=s90)
        dc91 = DrivingContract.objects.create(driver=nelson, team=benetton, season=s91)

        benetton = Constructor.objects.get(name="Benetton")
        lotus = Constructor.objects.get(name="Lotus")

        self.assertEqual(nelson.last_drive_before(s91), dc90)
        
"""Tests for the models"""
from django.test import TestCase

# Create your tests here.
from f1web.models import Car, Engine, EngineMaker, Season, Driver, DrivingContract, Constructor

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



    def test_car_earliest_season(self):
        """Test that car's earliest season is valid, 
        regardless of how they are ordered in the DB"""

        #car2 has been added to all years, in the order 90, 70, 80
        #so the database order should not have 70 at the head

        s70 = Season.objects.get(year = 1970)
        car2 = Car.objects.get(name = "FB2")
        self.assertEqual(car2.earliest_season(), s70)
    
    def test_car_earliest_season_none(self):
        car_with_no_season = Car.objects.get(name="FB4")
        self.assertIsNone(car_with_no_season.earliest_season())


    def test_car_set_constructor(self):
        car1 = Car.objects.get(name="FB1")
        car1.constructor = self.team
        

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

    def test_engine_earliest_season_car_with_none_earliest_season(self):
        e3 = Engine.objects.get(name="e3")
        print(e3.car_set.all())
        season = e3.earliest_season()
        self.assertIsNotNone(season)


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
    


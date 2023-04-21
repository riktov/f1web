"""Tests for the models"""
from django.test import TestCase

# Create your tests here.
from f1web.models import Car, Season, Driver, DrivingContract, Constructor

class CarTest(TestCase):
    "class for testing Car model"
    def setUp(self):

        self.team = Constructor.objects.create(name="FooBar")
        car1 = Car.objects.create(name = "FB1")
        car2 = Car.objects.create(name = "FB2")
        car3 = Car.objects.create(name = "FB3")
        car4 = Car.objects.create(name = "FB4")

        s80 = Season.objects.create(year = 1980)
        s70 = Season.objects.create(year = 1970)
        s90 = Season.objects.create(year = 1990)


        s90.cars.add(car2)
        s90.cars.add(car3)
        s70.cars.add(car2)
        s70.cars.add(car1)
        # s80.cars.add(car2)

        alex = Driver.objects.create(name="Alex")
        bob = Driver.objects.create(name="Bob")
        chris = Driver.objects.create(name="Chris")

        footeam = Constructor.objects.get(name = "FooBar")
        car1.constructor = footeam
        car2.constructor = footeam
        car3.constructor = footeam

        print(f"FB2: {car2}")
        DrivingContract.objects.create(season=s70, driver=bob, team=self.team)
        DrivingContract.objects.create(season=s80, driver=chris, team=self.team)
        DrivingContract.objects.create(season=s90, driver=alex, team=self.team)

        print(car1.constructor)

    def test_car_earliest_season(self):
        """Test that car's earliest season is valid, 
        regardless of how they are ordered in the DB"""

        #car2 has been added to all years, in the order 90, 70, 80
        #so the database order should not have 70 at the head

        s70 = Season.objects.get(year = 1970)
        car2 = Car.objects.get(name = "FB2")
        self.assertEqual(car2.earliest_season, s70)

    def test_car_set_constructor(self):
        print(f"Team: {self.team}")
        car1 = Car.objects.get(name="FB1")
        car1.constructor = self.team
        

    def test_car_seasons_and_drivers(self):
        s70 = Season.objects.get(year = 1970)
        car2 = Car.objects.get(name = "FB2")
        bob = Driver.objects.get(name = "Bob")
        
        list = car2.seasons_and_drivers_list

        #1970 Bob
        line = list[0]

        print(DrivingContract.objects.all())
        print(line)

        self.assertEqual(line[0], s70)
        self.assertEqual(line[1], bob)


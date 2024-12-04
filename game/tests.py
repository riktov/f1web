from django.test import TestCase

from f1web.models import Constructor, Driver, DrivingContract, Season
from game.queries import teammates_all, teammates_in_season

# Create your tests here.

class TeammatesTest(TestCase):
    """Test Case for drivers' teammates"""
    def setUp(self):
        Season.objects.create(year=1980)
        Season.objects.create(year=1981)
        Season.objects.create(year=1982)
        Season.objects.create(year=1986)

        Constructor.objects.create(name="Ferrari")
        Constructor.objects.create(name="Brabham")
        Constructor.objects.create(name="McLaren")
        Constructor.objects.create(name="Williams")

        Driver.objects.create(name="Nelson")
        Driver.objects.create(name="Niki")
        Driver.objects.create(name="Riccardo")
        Driver.objects.create(name="Nigel")     

    def test_teammates_in_season(self):
        """A driver's teammates in a single season can be acquired"""
        nelson = Driver.objects.get(name="Nelson")
        riccardo = Driver.objects.get(name="Riccardo")
        niki = Driver.objects.get(name="Niki")

        brabham = Constructor.objects.get(name="Brabham")
        ferrari = Constructor.objects.get(name="Ferrari")
        s1982 = Season.objects.get(year = 1982)

        DrivingContract.objects.create(driver=nelson, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=riccardo, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=niki, team=ferrari, season=s1982)
                
        teammates = teammates_in_season(nelson, s1982)

        self.assertIn(riccardo, teammates)
        self.assertNotIn(niki, teammates)
    
    def test_teammates_all(self):
        """a driver's teammates in all seasons can be acquired"""
        nelson = Driver.objects.get(name="Nelson")
        riccardo = Driver.objects.get(name="Riccardo")
        nigel = Driver.objects.get(name="Nigel")
        niki = Driver.objects.get(name="Niki")
        
        brabham = Constructor.objects.get(name="Brabham")
        williams = Constructor.objects.get(name="Williams")
        ferrari = Constructor.objects.get(name="Ferrari")
        s1982 = Season.objects.get(year = 1982)
        s1986 = Season.objects.get(year = 1986)

        DrivingContract.objects.create(driver=nelson, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=nelson, team=williams, season=s1986)
        DrivingContract.objects.create(driver=riccardo, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=niki, team=ferrari, season=s1982)
        DrivingContract.objects.create(driver=nigel, team=williams, season=s1986)

        teammates = teammates_all(nelson)

        self.assertIn(riccardo, teammates)
        self.assertIn(nigel, teammates)
        self.assertNotIn(niki, teammates)





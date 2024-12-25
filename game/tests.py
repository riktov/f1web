from django.test import TestCase

from f1web.models import Constructor, Driver, DrivingContract, Season
from game.queries import teamings, teammates_all, teammates_in_season


# Create your tests here.

class TeammatesTest(TestCase):
    """Test Case for drivers' teammates"""
    def setUp(self):
        s1980 =Season.objects.create(year=1980)
        s1981 = Season.objects.create(year=1981)
        s1982 = Season.objects.create(year=1982)
        s1986 = Season.objects.create(year=1986)

        ferrari = Constructor.objects.create(name="Ferrari")
        brabham = Constructor.objects.create(name="Brabham")
        mclaren = Constructor.objects.create(name="McLaren")
        williams = Constructor.objects.create(name="Williams")

        nelson = Driver.objects.create(name="Nelson")
        niki = Driver.objects.create(name="Niki")
        riccardo =Driver.objects.create(name="Riccardo")
        nigel = Driver.objects.create(name="Nigel")     
        alain = Driver.objects.create(name = "Alain")

        DrivingContract.objects.create(driver=nelson, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=riccardo, team=brabham, season=s1982)
        DrivingContract.objects.create(driver=niki, team=ferrari, season=s1982)
        DrivingContract.objects.create(driver=nelson, team=williams, season=s1986)
        DrivingContract.objects.create(driver=nigel, team=williams, season=s1986)
        DrivingContract.objects.create(driver=alain, team=mclaren, season=s1986)
        

    def test_teammates_in_season(self):
        """A driver's teammates in a single season can be acquired"""
        nelson = Driver.objects.get(name="Nelson")
        riccardo = Driver.objects.get(name="Riccardo")
        niki = Driver.objects.get(name="Niki")

        s1982 = Season.objects.get(year = 1982)
                
        teammates82 = teammates_in_season(nelson, s1982)

        self.assertIn(riccardo, teammates82)
        self.assertNotIn(niki, teammates82)
    
    def test_teammates_all(self):
        """a driver's teammates in all seasons can be acquired"""
        nelson = Driver.objects.get(name="Nelson")
        riccardo = Driver.objects.get(name="Riccardo")
        nigel = Driver.objects.get(name="Nigel")
        alain = Driver.objects.get(name="Alain")

        nelsons_teammates = teammates_all(nelson)

        self.assertIn(riccardo, nelsons_teammates)
        self.assertIn(nigel, nelsons_teammates)
        self.assertNotIn(alain, nelsons_teammates)

    def test_teamed(self):
        nelson = Driver.objects.get(name="Nelson")
        riccardo = Driver.objects.get(name="Riccardo")
        nigel = Driver.objects.get(name="Nigel")
        niki = Driver.objects.get(name="Niki")

        s1986 = Season.objects.get(year=1986)
        williams = Constructor.objects.get(name = "Williams") 


        gig1 = teamings(nelson, nigel)[0]
        season, teams = gig1

        self.assertEqual(season, s1986)
        self.assertIn(williams, teams)

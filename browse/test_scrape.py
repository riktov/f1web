from unittest import TestCase

from browse.scrape import scrape_season


class ScrapeTest(TestCase):
    def setUp(self):
        self.seasons = [
            "1987_Formula_One_World_Championship",
            "1988_Formula_One_World_Championship",
            "1989_Formula_One_World_Championship",
        ]

    def test_valid_constructors(self):
        for season in self.seasons:
            specs = scrape_season(season)
            for constructor in specs:
                self.assertIsNotNone(constructor['constructor'])
                self.assertIsNotNone(constructor['cars'])
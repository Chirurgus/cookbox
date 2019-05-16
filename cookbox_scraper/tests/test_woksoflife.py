from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestBBCFoodScraper(RecipeScraperTestMixin, TestCase):
    def setUp(self):
        

        super().setUp()

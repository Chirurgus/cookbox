import os

from cookbox_scraper import scrape_me

class RecipeScraperTestMixin(object):
    """
    Abstract base class for recipe-scraper tests.
    For every scraper this class should be inhered from
    and the SetUp method overridden.
    Call setUp AFTER you initialized the following variables: 
    self.host = URL of the recipe to be scraped
    self.name = Name of the recipe
    etc.
    """
    def setUp(self):
        self.scraper = scrape_me(self.url)

    def test_host(self):
        self.assertEqual(
            self.host,
            self.scraper.host()
        )
    
    def test_title(self):
        self.assertEqual(
            self.title,
            self.scraper.title()
        )
    
    def test_description(self):
        self.assertEqual(
            self.description,
            self.scraper.description()
        )
    
    def test_yield_unit(self):
        self.assertEqual(
            self.yield_unit,
            self.scraper.yield_unit()
        )

    def test_yield(self):
        self.assertTupleEqual(
            self.yields,
            self.scraper.yields()
        )
    
    def test_ingredients(self):
        self.assertListEqual(
            self.ingredients,
            self.scraper.ingredients()
        )

    def test_instructions(self):
        self.assertListEqual(
            self.instructions,
            self.scraper.instructions()
        )
    
    def test_notes(self):
        self.assertListEqual(
            self.notes,
            self.scraper.notes()
        )
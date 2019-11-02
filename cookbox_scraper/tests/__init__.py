import os

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
)
    
from cookbox_scraper import scrape_me, scrape

class RecipeScraperTestMixin(object):
    """
    Abstract base class for recipe-scraper tests.
    For every scraper this class should be inhered from
    and the SetUp method overridden.
    Call setUp AFTER you initialized the following variables: 
    self.host = URL of the recipe to be scraped
    self.name = Name of the recipe
    etc.
    To make this easier you can use the following code to generate
    the code needed to fill out this information.
    Just replace the url with one form website you're testing.

    from cookbox_scraper import scrape_me
    s = scrape_me("https://www.bbcgoodfood.com/recipes/mango-lassi")
    code = '''cls.url = "{url}"
    cls.host = "{host}"
    cls.title = "{title}"
    cls.description = "{description}"
    cls.time_unit = "{time_unit}"
    cls.time = {time}
    cls.yield_unit = "{yield_unit}"
    cls.yields = {yields}
    cls.ingredients = {ingredients}
    cls.instructions = {instructions}
    cls.notes = {notes}'''.format(
        url=s.url,
        host=s.host(),
        title=s.title(),
        description=s.description(),
        time_unit=s.time_unit(),
        time=s.time(),
        yield_unit=s.yield_unit(),
        yields=s.yields(),
        ingredients=s.ingredients(),
        instructions=s.instructions(),
        notes=s.notes()
    )
    print(code)
    """
    @classmethod
    def setUpClass(cls):
        cls.scraper = scrape_me(cls.url)
        cls.maxDiff = None
    
    def test_save_recipe(self):
        # If this doesn't throw anything we're happy
        recipe = scrape(self.url)
        recipe.save()

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

    def test_title_length(self):
        title = self.scraper.title()
        self.assertTrue(
            len(title) <= Recipe._meta.get_field('name').max_length
        )
    
    def test_description(self):
        self.assertEqual(
            self.description,
            self.scraper.description()
        )

    def test_time_unit(self):
        self.assertEqual(
            self.time_unit,
            self.scraper.time_unit()
        )

    def test_time(self):
        self.assertTupleEqual(
            self.time,
            self.scraper.time()
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
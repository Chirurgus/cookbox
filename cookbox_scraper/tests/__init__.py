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
    To make this easier you can use the following code to generate
    the code needed to fill out this information.
    This was done for the BBCFood test

    from cookbox_scraper import scrape_me
    s = scrape_me("https://thewoksoflife.com/mongolian-beef-recipe/")
    code = '''self.url = '{url}'
    self.host = '{host}'
    self.title = '{title}'
    self.description = '{description}'
    self.time = {time}
    self.yield_unit = '{yield_unit}'
    self.yields = {yields}
    self.ingredients = {ingredients}
    self.instructions = {instructions}
    self.notes = {notes}'''.format(
        url=s.url,
        host=s.host(),
        title=s.title(),
        description=s.description(),
        time=s.time(),
        yield_unit=s.yield_unit(),
        yields=s.yields(),
        ingredients=s.ingredients(),
        instructions=s.instructions(),
        notes=s.notes()
    )
    print(code)
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
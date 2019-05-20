from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestBBCGoodFoodScraper(RecipeScraperTestMixin, TestCase):
    def setUp(self):
        self.url = 'https://www.bbcgoodfood.com/recipes/spiced-halloumi-pineapple-burger-zingy-slaw'
        self.host = 'bbcgoodfood.com'
        self.title = 'Spiced halloumi & pineapple burger with zingy slaw'
        self.description = 'Pack four of your 5-a-day into these tasty veggie burgers with barbecued halloumi. Wrap in lettuce cups instead of buns for a healthy, low-calorie option'
        self.time = (25, 20, 5)
        self.yield_unit = 'serving'
        self.yields = (2.0, 1)
        self.ingredients = [('All', [(0.0, None, '½ red cabbage'), (2.0, None, 'carrots'), (0.0, None, '100g radishes, sliced'), (1.0, None, 'small pack coriander, chopped'), (2.0, None, 'limes'), (1.0, None, 'tbsp cold-pressed rapeseed oil'), (0.0, None, 'big pinch of chilli flakes'), (1.0, None, 'tbsp chipotle paste'), (0.0, None, '60g halloumi'), (2.0, None, 'small slices of fresh pineapple'), (1.0, None, 'Little Gem lettuce, divided into 4 lettuce cups, or 2 small seeded burger buns, cut in half, to serve (optional)')])]
        self.instructions = ['Heat the barbecue', ' Put the cabbage, carrot, radish and coriander in a bowl', ' Pour over the lime juice, add ½ tbsp oil and the chilli flakes, then season with salt and pepper', ' Give everything a good mix with your hands', ' This can be done a few hours before and kept in the fridge', 'Mix the remaining oil with the chipotle paste then coat the halloumi slices in the mixture', ' Put the halloumi slices on a sheet of foil and put on the barbecue with the pineapple (or use a searing hot griddle pan if cooking inside)', ' Cook for 2 mins on each side until the cheese is golden, and the pineapple is beginning to caramelise', ' Brush the buns with the remaining chipotle oil, then put your burger buns, if using, cut-side down, on the barbecue for the last 30 seconds of cooking to toast', 'Assemble your burgers with the lettuce or buns', ' Start with a handful of the slaw, then add halloumi and pineapple', ' Serve with the remaining slaw']
        self.notes = []

        super().setUp()

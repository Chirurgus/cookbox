from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestBBCGoodFoodScraper(RecipeScraperTestMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'https://www.bbcgoodfood.com/recipes/spiced-halloumi-pineapple-burger-zingy-slaw'
        cls.host = 'bbcgoodfood.com'
        cls.title = 'Spiced halloumi & pineapple burger with zingy slaw'
        cls.description = 'Pack four of your 5-a-day into these tasty veggie burgers with barbecued halloumi. Wrap in lettuce cups instead of buns for a healthy, low-calorie option'
        cls.time_unit = "min"
        cls.time = (25, 20, 5)
        cls.yield_unit = 'serving(s)'
        cls.yields = (2.0, 1)
        cls.ingredients = [('All', [(0.0, "", '½ red cabbage'), (2.0, "", 'carrots'), (0.0, "", '100g radishes, sliced'), (1.0, "", 'small pack coriander, chopped'), (2.0, "", 'limes'), (1.0, "", 'tbsp cold-pressed rapeseed oil'), (0.0, "", 'big pinch of chilli flakes'), (1.0, "", 'tbsp chipotle paste'), (0.0, "", '60g halloumi'), (2.0, "", 'small slices of fresh pineapple'), (1.0, "", 'Little Gem lettuce, divided into 4 lettuce cups, or 2 small seeded burger buns, cut in half, to serve (optional)')])]
        cls.instructions = ['Heat the barbecue', ' Put the cabbage, carrot, radish and coriander in a bowl', ' Pour over the lime juice, add ½ tbsp oil and the chilli flakes, then season with salt and pepper', ' Give everything a good mix with your hands', ' This can be done a few hours before and kept in the fridge', 'Mix the remaining oil with the chipotle paste then coat the halloumi slices in the mixture', ' Put the halloumi slices on a sheet of foil and put on the barbecue with the pineapple (or use a searing hot griddle pan if cooking inside)', ' Cook for 2 mins on each side until the cheese is golden, and the pineapple is beginning to caramelise', ' Brush the buns with the remaining chipotle oil, then put your burger buns, if using, cut-side down, on the barbecue for the last 30 seconds of cooking to toast', 'Assemble your burgers with the lettuce or buns', ' Start with a handful of the slaw, then add halloumi and pineapple', ' Serve with the remaining slaw']
        cls.notes = []

        super().setUpClass()

class TestBBCGoodFoodScraper2(RecipeScraperTestMixin, TestCase):
    '''
    Test BBCGF scraper on a case where serving size is not trivial
    '''
    @classmethod
    def setUpClass(cls):
        cls.url = "https://www.bbcgoodfood.com/recipes/marathon-burritos"
        cls.host = "bbcgoodfood.com"
        cls.title = "Marathon burritos"
        cls.description = "If you're a keen runner, eat nutritious meals to fit in with your training programme. These energy-boosting Mexican wraps are perfect fitness fodder"
        cls.time_unit = 'min'
        cls.time = (80, 20, 60)
        cls.yield_unit = "as a meal with extra for snacking"
        cls.yields = (4.0, 1)
        cls.ingredients = [('All', [(0, '', '300g brown rice'), (0, '', '½ small pack coriander, chopped'), (0, '', 'juice 1 lime'), (1.0, '', 'tsp olive oil'), (2.0, '', 'garlic cloves, crushed'), (1.0, '', 'tbsp chipotle paste'), (2.0, '', 'tbsp ground cumin'), (1.0, '', 'tbsp brown sugar'), (1.0, '', 'tbsp cider vinegar'), (2.0, '', 'x 400g cans black beans, drained and rinsed'), (0, '', '400g can chopped tomato'), (2.0, '', 'large tomatoes'), (1.0, '', 'red onion, finely chopped'), (0, '', '½ small pack coriander, chopped'), (0, '', 'juice 2 limes'), (2.0, '', 'avocados'), (0, '', 'large wholemeal tortilla')])]
        cls.instructions = ['Put the rice in a medium saucepan with 600ml cold water and a pinch of salt if you like', ' Bring to the boil, then turn the heat down low, cover and gently simmer for about 20 mins until all the water has been absorbed', ' Turn off the heat and leave for another 10 mins undisturbed', ' Stir the rice and add the coriander and lime juice', 'For the black beans, heat the oil in a large frying pan and add the garlic, chipotle, cumin, sugar and vinegar, and cook everything for 1 min', ' Tip in the beans and tomatoes, give everything a stir and simmer, uncovered, for 20 mins until thickened', 'For the salsa and guacamole, mix the tomatoes with the onion, coriander, lime juice and seasoning', ' Tip half the salsa into another bowl and mash the avocados into it to make guacamole', ' Wrap everything up together in warmed wholemeal tortillas topped with natural yogurt, lime juice and grated cheese, if you like']
        cls.notes = []

        super().setUpClass()

class TestBBCGoodFoodScraper3(RecipeScraperTestMixin, TestCase):
    '''
    Test BBCGF scraper on a case where cook_time does not exist.
    '''
    @classmethod
    def setUpClass(cls):
        cls.url = "https://www.bbcgoodfood.com/recipes/mango-lassi"
        cls.host = "bbcgoodfood.com"
        cls.title = "Mango lassi"
        cls.description = "Blitz up mangoes with yogurt, cardamom, lime and honey and you have the most delicious Indian drink\xa0–\xa0a bit like a smoothie and great for breakfast"
        cls.time_unit = "min"
        cls.time = (10, 10, 0)
        cls.yield_unit = "serving(s)"
        cls.yields = (6.0, 1)
        cls.ingredients = [('All', [(0, '', '3-4 ripe mangoes (honey mangoes if possible)'), (0, '', '500g natural yogurt'), (2.0, '', 'tsp ground cardamom'), (1.0, '', 'tbsp honey'), (2.0, '', 'limes')])]
        cls.instructions = ['Put all the ingredients apart from the lime juice in a food processor and blitz', ' Add the lime juice along with a pinch of salt, to taste, then pour into glasses with some ice cubes and serve']
        cls.notes = []

        super().setUpClass()
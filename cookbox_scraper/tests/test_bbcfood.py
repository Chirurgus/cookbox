from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestBBCFoodScraper(RecipeScraperTestMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'https://www.bbc.com/food/recipes/tom_kerridges_spaghetti_51800'
        cls.host = 'bbc.com'
        cls.title = 'Tom Kerridge’s spaghetti Bolognese'
        cls.description = 'Tom Kerridge’s delicious spaghetti Bolognese uses restaurant know-how to enhance this cheap-as-chips dish.'
        cls.time_unit = "min"
        cls.time = (30, 30, 0)
        cls.yield_unit = 'serving'
        cls.yields = (4.0, 1)
        cls.ingredients = [('All', [(0.0, "", '500g/1lb 2oz beef mince'), (0.0, "", 'splash vegetable oil'), (0.0, "", '100g/3½oz smoked streaky bacon, diced'), (1.0, "", 'onion, finely chopped'), (2.0, "", 'celery stalks, trimmed, thinly sliced'), (2.0, "", 'carrots, finely diced'), (2.0, "", 'garlic cloves, grated'), (1.0, "", 'bay leaf'), (0.0, "", '3-4 tbsp red wine vinegar'), (1.0, "", 'tsp demerara sugar'), (1.0, "", 'tbsp dried oregano'), (0.0, "", '400g tin chopped tomatoes'), (0.0, "", '300ml/10½fl oz beef stock (made from beef stock cubes)'), (0.0, "", '150g/5oz button mushrooms, quartered'), (0.0, "", 'salt and freshly ground black pepper'), (0.0, "", '400g/14oz dried spaghetti'), (0.0, "", 'grated Parmesan cheese, to garnish (optional)')])]
        cls.instructions = ['Preheat the oven to 190C/180C Fan/Gas 5', 'Put the beef mince in a colander and rinse under the cold tap to separate it into smaller pieces', ' Drain well and pat dry with kitchen paper', 'Transfer the mince to a roasting tray and roast for 35-60 minutes, or until completely crisp and golden-brown', ' This intensifies the flavour and helps it to absorb the sauce ingredients', ' Drain off the fat', 'Heat the oil in a large, heavy-based casserole over a medium heat', ' Add the bacon and fry for 4-5 minutes, stirring from time to time, until the fat melts and the bacon starts to brown', 'Add the onion, celery, carrots, garlic and bay leaf and cook for 4-5 minutes, or until they begin to soften', 'Stir in the vinegar, then the sugar and oregano', ' Add the cooked mince, tomatoes, stock and mushrooms', ' Stir well and bring to the boil, then reduce the heat and simmer for 45-60 minutes, stirring occasionally, until thickened', ' Season, to taste, with salt and pepper, then set aside', 'Meanwhile, cook the spaghetti in a pan of boiling, salted water, stirring often with a fork, until just tender (al dente)', ' Drain immediately in a colander, shaking it', 'To serve, twirl the spaghetti onto 4 plates', ' Spoon over the Bolognese sauce and garnish with Parmesan, if desired']
        cls.notes = []

        super().setUpClass()

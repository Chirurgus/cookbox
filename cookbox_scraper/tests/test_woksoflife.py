from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestBBCFoodScraper(RecipeScraperTestMixin, TestCase):
    def setUp(self):
        self.url = 'https://thewoksoflife.com/mongolian-beef-recipe/'
        self.host = 'thewoksoflife.com'
        self.title = 'Mongolian Beef Recipe, An "Authentic" version'
        self.description = 'This Mongolian Beef Recipe is a crispy, flavorful homemade version that\'s less sweet than the gloopy restaurant Mongolian Beef you\'re probably used to.'
        self.time = (85, 0, 10)
        self.yield_unit = 'servings'
        self.yields = (4.0, 1)
        self.ingredients = [('All', [(8.0, None, 'ounces flank steak, sliced against the grain into ¼-inch thick slices'), (1.0, None, 'teaspoon oil'), (1.0, None, 'teaspoon low sodium soy sauce'), (1.0, None, 'tablespoon plus ¼ cup cornstarch'), (0.0, None, '⅓ cup vegetable oil, for frying the beef'), (0.0, None, '½ teaspoon minced ginger'), (5.0, None, 'dried red chili peppers (optional)'), (2.0, None, 'cloves garlic, chopped'), (0.0, None, '¼ cup low sodium soy sauce'), (0.0, None, '¼ cup water or low sodium chicken stock'), (2.0, None, 'tablespoons brown sugar'), (1.0, None, 'tablespoon cornstarch, mixed with 1 tablespoon water'), (2.0, None, 'scallions, cut into 1-inch long slices on the diagonal')])]
        self.instructions = ['Marinate the beef for 1 hour in 1 teaspoon oil, 1 teaspoon soy sauce, and 1 tablespoon cornstarch', 'Once marinated, dredge the meat in the remaining ¼ cup of cornstarch until lightly coated', 'Heat ⅓ cup vegetable oil in the wok over high heat', ' Just before the oil starts to smoke, spread the flank steak pieces evenly in the wok, and let sear for 1 minute (depending upon the heat of your wok)', ' Turn over and let the other side sear for another 30 seconds', ' Remove to a sheet pan; tilt it slightly to let the oil drain to one side (lean it on a cookbook or cutting board)', ' The beef should be seared with a crusty coating', 'Drain the oil from the wok, leaving 1 tablespoon behind, and turn the heat to medium-high', ' Add the ginger and dried chili peppers, if using', ' After about 15 seconds, add the chopped garlic', ' Stir for another 10 seconds and add the ¼ cup low sodium soy sauce and chicken stock (or water)', 'Bring the sauce to a simmer, add the brown sugar, and stir until dissolved', 'Let the sauce simmer for about 2 minutes and slowly stir in the cornstarch slurry mixture--until the sauce coats the back of a spoon', 'Add the beef and scallions and toss everything together for another 30 seconds', ' There should be almost no liquid, as the sauce should be clinging to the beef', ' If you still have sauce, increase the heat slightly and stir until thickened', 'Plate and serve with steamed rice!']
        self.notes = []

        super().setUp()

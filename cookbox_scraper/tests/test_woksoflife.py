from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestWoksOfLifeScraper(RecipeScraperTestMixin, TestCase):
    '''
    This class tests WoksOfLife scraper on newer recipes.
    See WoksOfLifeScraper docs for details.
    '''
    def setUp(self):
        self.url = 'https://thewoksoflife.com/beef-with-broccoli-all-purpose-stir-fry-sauce/'
        self.host = 'thewoksoflife.com'
        self.title = 'Beef and Broccoli'
        self.description = 'Beef and Broccoli was one of the most popular dishes in our family’s Chinese takeout restaurant. Get our restaurant secrets in this authentic beef and broccoli recipe.'
        self.time = (50, 35, 15)
        self.yield_unit = 'servings'
        self.yields = (6.0, None)
        self.ingredients = [('For the beef and marinade:', [('1', 'pound', 'flank steak , (450g, sliced 1/4 inch thick)'), ('1/4', 'teaspoon', 'baking soda, (optional)'), ('3', 'tablespoons', 'water'), ('1 1/2', 'teaspoons', 'cornstarch'), ('2', 'teaspoons', 'vegetable oil'), ('1', 'teaspoon', 'oyster sauce')]), ('For the sauce:', [('2/3', 'cup', 'chicken stock, (warmed)'), ('1 1/2', 'teaspoons', 'granulated sugar, (or brown sugar)'), ('1 1/2', 'tablespoons', 'soy sauce'), ('1', 'teaspoon', 'dark soy sauce, (or double black dark soy sauce)'), ('1', 'tablespoon', 'oyster sauce'), ('1/2', 'teaspoon', 'sesame oil'), ('1/8', 'teaspoon', 'white pepper'), ('1/8', 'teaspoon', 'five spice powder, (optional)')]), ('For the rest of the dish:', [('4', 'cups', 'broccoli florets, (300g)'), ('3', 'tablespoons', 'vegetable oil, (divided)'), ('2', 'cloves', 'garlic, (minced)'), ('1/4', 'teaspoon', 'ginger, (grated/minced, optional)'), ('1', 'tablespoon', 'Shaoxing wine'), ('2 1/2', 'tablespoons', 'cornstarch, (mixed with 3 tablespoons water)')])]
        self.instructions = ['In a bowl, add the sliced beef, ¼ teaspoon baking soda, and 3 tablespoons water (if you don’t want your beef tenderized too much, omit the baking soda)', ' Massage the beef with your hands until all the liquid is absorbed', ' Mix in 1 ½ teaspoons cornstarch, 2 teaspoons oil, and 1 teaspoon oyster sauce, and set aside to marinate for at least 30 minutes', 'Make the sauce mixture by mixing together the chicken stock, sugar, soy sauce, dark soy sauce, oyster sauce, sesame oil, white pepper, and five spice powder (if using)', ' Set aside', 'Bring 6 cups of water to a boil and blanch your broccoli for 30 to 60 seconds (depending on whether you like your broccoli crunchy or a little soft)', ' Drain and set aside', 'Heat your wok over high heat until smoking', ' Add 2 tablespoons oil and sear the beef on both sides until browned (this should only take 2-3 minutes)', ' Turn off the heat, remove the beef from the wok, and set aside', 'Set the wok over medium heat and add another tablespoon of oil to the along with the garlic and ginger (if using)', ' Stir the garlic and ginger for 5 seconds and then pour the Shaoxing wine around the perimeter of the wok', 'Next, add in the sauce mixture you made earlier', ' Stir the sauce around the sides of the wok to deglaze it (all those nice bits from stir-frying the beef should be absorbed into the sauce)', ' Bring the sauce to a simmer', ' Stir the cornstarch and water slurry to ensure it’s well combined, and drizzle the mixture into sauce while stirring constantly', ' Allow it to simmer and thicken for 20 seconds', 'Toss in the blanched broccoli and seared beef (along with any juices)', ' Mix everything together over medium heat until the sauce coats the beef and broccoli', ' If the sauce seems thin, turn up the heat and reduce it further, or add a bit more cornstarch slurry', ' If the sauce is too thick, add a splash of chicken stock or water', ' Serve with plenty of steamed rice!']
        self.notes = []

        super().setUp()

class TestWoksOfLifeOldScraper(RecipeScraperTestMixin, TestCase):
    '''
    This class tests WoksOfLife scraper on old recipes.
    See WoksOfLifeScraper docs for details.
    '''
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
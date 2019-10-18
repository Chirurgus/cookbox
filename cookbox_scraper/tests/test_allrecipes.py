from unittest import TestCase

from cookbox_scraper.bbcfood import BBCFood

from . import RecipeScraperTestMixin


class TestAllRecipesScraper(RecipeScraperTestMixin, TestCase):
    def setUp(self):
        self.url = "https://www.allrecipes.com/recipe/228953/california-roll/"
        self.host = 'allrecipes.com'
        self.title = 'California Roll'
        self.description = '\r\n"A California roll is a fresh take on traditional Japanese rice rolls. Filled with avocado, crab, and cucumber, it\'s fresh and crunchy and makes a filling meal. You can use real or imitation crab."        '
        self.time = (110.0, None, None)
        self.yield_unit = 'servings'
        self.yields = (5.0, 1.0)
        self.ingredients = [
            ('All', [
                (4.0, "", 'cups water'),
                (2.0, "", 'cups uncooked white rice'),
                (0.5, "", 'cup seasoned rice vinegar'),
                (1.0, "", 'teaspoon white sugar, or as needed'),
                (1.0, "", 'teaspoon salt, or as needed'),
                (0.25, "", 'pound cooked crab meat, drained of excess liquid and shredded'),
                (1.0, "", 'tablespoon mayonnaise'),
                (5.0, "", 'sheets nori (dry seaweed)'),
                (1.0, "", 'avocado, sliced'),
                (0.25, "", 'cup red caviar, such as tobiko'),
                (1.0, "", 'English cucumber, seeded and sliced into strips'),
                (2.0, "", 'tablespoons drained pickled ginger, for garnish'),
                (2.0, "", 'tablespoons soy sauce, or to taste'),
                (1.0, "", 'tablespoon wasabi paste')
                ]
            )
        ]
        self.instructions = [
            'Wrap a sushi rolling mat completely in plastic wrap and set aside',
            'Bring water and rice to a boil in a saucepan over high heat',
            ' Reduce heat to medium-low, cover, and simmer until the rice is tender and the liquid has been absorbed, 20 to 25 minutes',
            ' Transfer rice to a bowl and cut in rice vinegar using a rice paddle or wooden spoon',
            ' Season with 1 teaspoon sugar and 1 teaspoon salt, or to taste',
            ' Allow to cool to room temperature, about 30 minutes',
            'Combine crab meat with mayonnaise in a small bowl',
            'Place a sheet of nori on a flat work surface',
            ' Spread a thin layer of rice on top of the nori',
            ' Place the nori, rice side down, on the prepared rolling mat',
            ' Place 2 to 3 avocado slices on top of the nori in one layer',
            ' Top with 2 to 3 tablespoons of the crab mixture',
            ' Spoon 1 to 2 teaspoons tobiko lengthwise on one side of the avocado-crab mixture, and 2 cucumber strips on the other side',
            ' Using the mat as a guide, carefully roll the California roll into a tight log',
            ' Remove the rolling mat',
            ' Top roll with more tobiko, cover with plastic wrap, and gently press the tobiko into the top of the roll',
            ' Remove the plastic and cut roll into 6 even pieces using a wet knife',
            ' Repeat with remaining sheets of nori and filling',
            ' Serve garnished with pickled ginger, soy sauce, and wasabi paste'
        ]
        self.notes = []

        super().setUp()

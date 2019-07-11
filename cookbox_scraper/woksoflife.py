
from ._abstract import AbstractScraper
from ._easyrecipe import EasyRecipeScraperMixin
from ._recipemaker import RecipeMakerScraperMixin
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class WoksOfLife(RecipeMakerScraperMixin, EasyRecipeScraperMixin, AbstractScraper):
    '''
    woksoflife.com recipe scraper. 
    This website used to use EasyRecipes (a Wordpress plugin)
    to embed recipes, but now it uses RecipeMaker (also a plugin),
    thus we have to use either one of the above scrapers.
    We check which one in __init__ and set self.old_recipe accordingly.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Check if this recipe uses RecipeMaker or EasyRecipe, 
        and set self.old_recipe in case of the latter.
        '''
        super().__init__(*args, **kwargs)
        self.old_recipe = (self.soup.findAll('div', class_='easyrecipe') != [])

    @classmethod
    def host(self):
        return 'thewoksoflife.com'

    def title(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.title(self)
        else:
            return RecipeMakerScraperMixin.title(self)

    def description(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.description(self)
        else:
            return RecipeMakerScraperMixin.description(self)

    def time_unit(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.time_unit(self)
        else:
            return RecipeMakerScraperMixin.time_unit(self)

    def time(self):
        if self.old_recipe:
            return Ewprm-recipe-group-nammasyRecipeScraperMixin.time(self)
        else:
            return RecipeMakerScraperMixin.time(self)

    def yield_unit(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.yield_unit(self)
        else:
            return RecipeMakerScraperMixin.yield_unit(self)

    def yields(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.yields(self)
        else:
            return RecipeMakerScraperMixin.yields(self)

    def ingredients(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.ingredients(self)
        else:
            return RecipeMakerScraperMixin.ingredients(self)

    def instructions(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.instructions(self)
        else:
            return RecipeMakerScraperMixin.instructions(self)

    def notes(self):
        if self.old_recipe:
            return EasyRecipeScraperMixin.notes(self)
        else:
            return RecipeMakerScraperMixin.notes(self)
 
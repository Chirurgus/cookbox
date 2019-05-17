
from ._abstract import AbstractScraper
from ._easyrecipe import EasyRecipeScraperMixin
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class WoksOfLife(EasyRecipeScraperMixin, AbstractScraper):
    '''
    Only works with old WoksOfLife recipes.
    '''
    @classmethod
    def host(self):
        return 'thewoksoflife.com'
from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, parse_ingredients

class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'allrecipes.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def description(self):
        return self.soup.find('div',
                              {'itemprop' : 'description'}
                              ).get_text()

    def time(self):
        mins = get_minutes(self.soup.find(
            'span',
            {'class': 'ready-in-time'})
        )
        return (float(mins), None, None)
    
    def yield_unit(self):
        return 'servings'
    
    def yields(self):
        s = self.soup.find('meta', {'id' : 'metaRecipeServings'})['content']
        return (float(s), 1.0)

        
    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {'class': "checkList__line"}
        )
        ingredient_strings = [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
            if ingredient.get_text(strip=True) not in (
                'Add all ingredients to list',
                '',
                'ADVERTISEMENT'
            )
        ]

        return [('All', parse_ingredients(ingredient_strings))]

        
    def instructions(self):
        instructions = self.soup.findAll(
            'span',
            {'class': 'recipe-directions__list--item'}
        )

        return [
            normalize_string(instruction.get_text())
            for instruction in instructions
        ]

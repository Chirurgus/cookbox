import re

from ._abstract import DOMScraper
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions

class BBCGoodFood(DOMScraper):

    @classmethod
    def host(self):
        return 'bbcgoodfood.com'

    def title(self):
        return self.soup.find('h1', {'itemprop': 'name'}).get_text()

    def description(self):
        return self.soup.find('div', {'itemprop': 'description'}).get_text()

    def time(self):
        prep_container = self.soup.find(
            'span',
            {'class': 'recipe-details__cooking-time-prep'}
        )
        if prep_container:
            prep_time = get_minutes(prep_container.find('span')) 
        else:
            prep_time = 0

        cook_container = self.soup.find(
            'span',
            {'class': 'recipe-details__cooking-time-cook'}
        )
        if cook_container:
            cook_time = get_minutes(cook_container.find('span'))
        else:
            cook_time = 0

        total_time = prep_time + cook_time
        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        serves = self.soup.find(
            'span',
            {'itemprop': 'recipeYield'}
        ).get_text().strip()

        servings = re.search('([1-9]+)([^0-9]+)', serves)

        return servings.group(2).strip() if servings else 'serving(s)'


    def yields(self):
        serves = self.soup.find(
            'span',
            {'itemprop': 'recipeYield'}
        ).get_text().strip()

        servings = re.search('([1-9]+)', serves)
        if servings:
            nservings = float(servings.group(1))
        else:
            nservings = 0
        
        return (nservings, 1)


    def ingredients(self):
        ingredients = self.soup.find(
            'section',
            {'id': "recipe-ingredients"}
        ).findAll('li')
        
        ingredients_str = [
            normalize_string(
                '{normal_text}{tooltip_text}'.format(
                    normal_text=ingredient.find(text=True),
                    tooltip_text=ingredient.find('a').get_text() if ingredient.find('a') is not None else ''
                )
            )
            for ingredient in ingredients
       ]

        return [('All', parse_ingredients(ingredients_str))]

    def instructions(self):
        instructions = self.soup.find(
            'section',
            {'id': 'recipe-method'}
        ).findAll('li')

        return normalize_instructions(
            [
            normalize_string(instruction.get_text())
            for instruction in instructions
            ]
        )

    def notes(self):
        return []
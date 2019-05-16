from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class BBCGoodFood(AbstractScraper):

    @classmethod
    def host(self):
        return 'bbcgoodfood.com'

    def title(self):
        return self.soup.find('h1', {'itemprop': 'name'}).get_text()

    def description(self):
        return self.soup.find('div', {'itemprop': 'description'}).get_text()

    def time(self):
        prep_time = get_minutes(self.soup.find(
            'span',
            {'class': 'recipe-details__cooking-time-prep'}
        ).find('span'))

        cook_time =get_minutes(self.soup.find(
            'span',
            {'class': 'recipe-details__cooking-time-cook'}
        ).find('span'))

        total_time = prep_time + cook_time
        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        return 'serving'

    def yields(self):
        serves= self.soup.find('span', {'itemprop': 'recipeYield'}).get_text()

        servings_sz_range = serves.strip().split(' ', 1)[1]
        nservings = servings_sz_range.split('-')[-1]

        return (float(nservings), 1)

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
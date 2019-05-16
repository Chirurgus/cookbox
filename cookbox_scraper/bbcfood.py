from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class BBCFood(AbstractScraper):

    @classmethod
    def host(self):
        return 'bbc.com'

    def title(self):
        return self.soup.find(
            'h1',
            {'class',"content-title__text"}
        ).get_text()

    def description(self):
        return self.soup.find(
            'p',
            { 'class' : "recipe-description__text" }
        ).get_text()

    def time(self):
        prep_time = get_minutes(self.soup.find(
            'p',
            {'class': 'recipe-metadata__prep-time'})
        )
        cook_time = get_minutes(self.soup.find(
            'p',
            {'class': 'recipe-metadata__cook-time'})
        )

        total_time = prep_time + cook_time
        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        return 'serving'
    
    def yields(self):
        serves = self.soup.find(
            'p',
            {'class': 'recipe-metadata__serving'}
        ).get_text()

        servings_sz_range = serves.split(' ', 1)[1]
        nservings = float(servings_sz_range.split('-')[-1])
        
        return (nservings, 1)

    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {'class': "recipe-ingredients__list-item"}
        )

        ingredients_str = [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ]

        return [('All', parse_ingredients(ingredients_str))]

    def instructions(self):
        instructions = self.soup.findAll(
            'p',
            {'class': 'recipe-method__list-item-text'}
        )

        return normalize_instructions(
            [
            normalize_string(instruction.get_text())
            for instruction in instructions
            ]
        )

    def notes(self):
        return []
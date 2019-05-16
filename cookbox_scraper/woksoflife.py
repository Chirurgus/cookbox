from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class WoksOfLife(AbstractScraper):

    @classmethod
    def host(self):
        return 'thewoksoflife.com'

    def title(self):
        return self.soup.find('div', {'itemprop': 'name'}).get_text()

    def description(self):
        return self.soup.find('div', {'itemprop': 'description'}).get_text()

    def time(self):
        prep_time = get_minutes(self.soup.find(
            'time',
            {'itemprop': 'prepTime'}
        ))

        cook_time = get_minutes(self.soup.find(
            'time',
            {'itemprop': 'cookTime'}
        ))

        total_time = get_minutes(self.soup.find(
            'time',
            {'itemprop': 'totalTime'}
        ))

        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        serves= self.soup.find('span', {'itemprop': 'recipeYield'}).get_text()

        servings_unit = serves.strip().split(' ', 1)[-1]

        return servings_unit

    def yields(self):
        serves= self.soup.find('span', {'itemprop': 'recipeYield'}).get_text()

        servings_sz_range = serves.strip().split(' ', 1)[0]
        nservings = servings_sz_range.split('-')[-1]

        return (float(nservings), 1)

    def ingredients(self):
        ing_div = self.soup.find(
            'div',
            { 'class' : 'ERSIngredients'}
        )

        ing_group_names = [
            normalize_string(name.get_text())
            for name in ing_div.findAll(
            'div',
            { 'class' : 'ERSSectionHead' })
        ]

        if ing_group_names == []:
            ing_group_names = ['All']

        ing_group_ul = ing_div.findAll('ul')
        
        ing_groups = []

        for name, group in zip(ing_group_names, ing_group_ul):
            ingredients = group.findAll(
                'li',
                {'itemprop': "ingredients"}
            )
            
            ingredients_str = [
                normalize_string(ingredient.get_text())
                for ingredient in ingredients
            ]

            ing_groups.append( (name, parse_ingredients(ingredients_str)) )

        return ing_groups

    def instructions(self):
        instructions = self.soup.findAll(
            'li',
            {'itemprop': 'recipeInstructions'}
        )

        return normalize_instructions(
            [
            normalize_string(instruction.get_text())
            for instruction in instructions
            ]
        )

    def notes(self):
        return []
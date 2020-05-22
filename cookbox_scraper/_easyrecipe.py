""" Created by Oleksandr Sorocynskyi """
""" On 16/05/2019 """

from ._utils import (
    get_minutes,
    normalize_string,
    parse_ingredients,
    normalize_instructions,
)

class EasyRecipeScraperMixin(object):
    '''
    EasyRecipe is a plugin for Wordpress that takes care of formatting
    recipes. This class should be used to scrap recipes from blogs
    using this plugin. Just inherit form this, THEN from DOMScraper.
    ''' 
    def title(self):
        return self.soup.find('div', {'class': 'ERSName'}).get_text()

    def description(self):
        return self.soup.find('div', {'class': 'ERSSummary'}).get_text()

    def time_unit(self):
        return 'min'

    def time(self):
        times = self.soup.find('div', {'class': 'ERSTimes'})
        prep_time = get_minutes(times.find('times', {'itemprop': 'prepTime'}))
        cook_time = get_minutes(times.find('time', {'itemprop': 'cookTime'}))
        total_time = get_minutes(times.find('time', {'itemprop': 'totalTime'}))

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
        ingredient_div = self.soup.find('div', { 'class' : 'ERSIngredients'})

        ingredient_group_names = [
            normalize_string(name.get_text())
            for name in ingredient_div.findAll(
                'div',
                { 'class' : 'ERSSectionHead' }
            )
        ]

        if ingredient_group_names == []:
            ingredient_group_names = ['All']

        ingredient_group_ul = ingredient_div.findAll('ul')
        
        ingredient_groups = []

        for name, group in zip(ingredient_group_names, ingredient_group_ul):
            ingredients = group.findAll('li', {'itemprop': "ingredients"})
            
            ingredients_str = [
                normalize_string(ingredient.get_text())
                for ingredient in ingredients
            ]

            ingredient_groups.append(
                (name, parse_ingredients(ingredients_str))
            )

        return ingredient_groups

    def instructions(self):
        instructions = self.soup.findAll(
            'li', {'itemprop': 'recipeInstructions'}
        )

        return normalize_instructions(
            [
                normalize_string(instruction.get_text())
                for instruction in instructions
            ]
        )

    def notes(self):
        return []
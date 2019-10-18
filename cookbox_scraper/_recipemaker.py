# Created by Oleksandr Sorochynskyi
# On 19/05/2019

from fractions import Fraction

from ._utils import (
    get_minutes,
    normalize_string,
    parse_quantity,
    parse_ingredients,
    normalize_instructions,
)

class RecipeMakerScraperMixin(object):
    '''
    Recipe Maker is a plugin for Wordpress that takes care of formatting
    recipes. This class should be used to scrap recipes from blogs
    using this plugin. Just inherit form this, THEN from AbstractScraper.
    ''' 
    def title(self):
        return self.soup.find('h2', {'class': 'wprm-recipe-name'}).get_text()

    def description(self):
        return self.soup.find('div', {'class': 'wprm-recipe-summary'}).get_text()

    def time_unit(self):
        return 'min'

    def time(self):
        times = self.soup.find('div', class_='wprm-recipe-times-container')
        '''
        prep_time = get_minutes(times.find('span', {'class': 'wprm-recipe-prep_time'}))
        cook_time = get_minutes(times.find('span', {'class': 'wprm-recipe-cook_time'}))
        total_time = get_minutes(times.find('span', {'class': 'wprm-recipe-total_time'}))
        '''

        prep_time_container = times.find(
            'div',
            class_ = 'wprm-recipe-prep-time-container'
        )
        prep_time = get_minutes(
            prep_time_container.find('span', class_='wprm-recipe-time')
        )

        cook_time_container= times.find(
            'div',
            class_= 'wprm-recipe-cook-time-container'
        )
        cook_time = get_minutes(
            cook_time_container.find('span', class_='wprm-recipe-time')
        )

        total_time_container= times.find(
            'div',
            class_= 'wprm-recipe-total-time-container'
        )
        total_time = get_minutes(
            total_time_container.find('span', class_='wprm-recipe-time')
        )

        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        servings_container = self.soup.find('div', class_='wprm-recipe-servings-container')
        # Sometimes users don't fill out the yield unit, return 'servings'
        field_unit_container = servings_container.find('span', class_='wprm-recipe-servings-unit')
        if field_unit_container:
            servings_unit = field_unit_container.get_text()
        else:
            servings_unit = 'servings'
        return servings_unit

    def yields(self):
        servings_container = self.soup.find('div', class_='wprm-recipe-servings-container')
        num_servings = servings_container.find('span', class_='wprm-recipe-servings').get_text()

        return (float(num_servings), None)

    def ingredients(self):
        ingredients_container = self.soup.find('div', class_='wprm-recipe-ingredients-container')

        # Initialize empty ingredient group list
        group_list = []

        # Look for all ingredient group containers
        group_containers = ingredients_container.findAll('div', class_='wprm-recipe-ingredient-group')
        # Check if there are any ingredients groups
        # If not we just put all ingredients into
        for group_container in group_containers:
            group_name_container = group_container.find('h4', class_='wprm-recipe-group-name')
            if group_name_container:
                ingredient_group_name = group_name_container.get_text()
            else:
                ingredient_group_name = 'All'

            ingredient_list = []
            ingredient_containers = group_container.findAll('li', class_='wprm-recipe-ingredient')
            for ingredient in ingredient_containers:
                quantity = ingredient.find('span', class_='wprm-recipe-ingredient-amount').get_text()

                unit_container = ingredient.find('span', class_='wprm-recipe-ingredient-unit')
                unit =  unit_container.get_text() if unit_container else ""

                description = ingredient.find('span', class_='wprm-recipe-ingredient-name').get_text()

                notes_container = ingredient.find('span', class_='wprm-recipe-ingredient-notes')
                # Append notes to description
                if notes_container:
                    description += (", " + notes_container.get_text())

                try:
                    quantity = parse_quantity(quantity)
                except ValueError:
                    description = ' '.join([quantity, description,])
                
                # append the ingredient tuple to ingredient list
                ingredient_list.append( (quantity, unit, description) )
            
            # append ingredient group to its list
            group_list.append( (ingredient_group_name, ingredient_list) )
        
        return group_list

    def instructions(self):
        instructions_container = self.soup.find('div', class_='wprm-recipe-instructions-container')

        instructions = instructions_container.findAll('li', class_='wprm-recipe-instruction')

        return normalize_instructions(
            [
                normalize_string(instruction.get_text())
                for instruction in instructions
            ]
        )

    def notes(self):
        notes_container = self.soup.findAll('div', class_='wprm-recipe-notes')
        return [ note.get_text for note in notes_container ]
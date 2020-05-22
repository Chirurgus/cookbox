import re

from django.db import transaction

from cookbox_core.models import Recipe

from ._abstract import WebsiteNotImplementedError
from ._screma_org import SchemaOrgRecipeScraper

def scrape(url):
    """
    Get a cookbox recipe from a URL.
    Does not save the recipe, but returns its instance.
    """
    scraper = SchemaOrgRecipeScraper(url)

    with transaction.atomic():
        recipe = Recipe.objects.create(name = scraper.title(),
                                    description = scraper.description(),
                                    unit_time = scraper.time_unit(),
                                    total_time = scraper.time()[0],
                                    preparation_time = scraper.time()[1],
                                    cook_time = scraper.time()[2],
                                    unit_yield = scraper.yield_unit(),
                                    total_yield = scraper.yields()[0],
                                    serving_size = scraper.yields()[1],
                                    source = url)
        for pos_group, ing_group in enumerate(scraper.ingredients()):
            group = recipe.ingredient_groups.create(name = ing_group[0], position = pos_group)
            for idx, ing in enumerate(ing_group[1]):
                group.ingredients.create(
                    quantity = ing[0],
                    unit = ing[1],
                    description= ing[2],
                    position= idx)

        for idx, instruction in enumerate(scraper.instructions()):
            recipe.instructions.create(instruction = instruction, position= idx)
        
        return recipe

__all__ = ['scrape', 'WebsiteNotImplementedError']

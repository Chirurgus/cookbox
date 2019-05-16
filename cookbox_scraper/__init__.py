import re

from cookbox_core.models import Recipe

from .allrecipes import AllRecipes
from .bbcfood import BBCFood
from .bbcgoodfood import BBCGoodFood
from .woksoflife import WoksOfLife
from .marmiton import Marmiton


SCRAPERS = {
    AllRecipes.host(): AllRecipes,
    BBCFood.host(): BBCFood,
    BBCGoodFood.host(): BBCGoodFood,
    WoksOfLife.host(): WoksOfLife,
    Marmiton.host(): Marmiton,
}


def url_path_to_dict(path):
    pattern = (r'^'
               r'((?P<schema>.+?)://)?'
               r'((?P<user>.+?)(:(?P<password>.*?))?@)?'
               r'(?P<host>.*?)'
               r'(:(?P<port>\d+?))?'
               r'(?P<path>/.*?)?'
               r'(?P<query>[?].*?)?'
               r'$'
               )
    regex = re.compile(pattern)
    matches = regex.match(path)
    url_dict = matches.groupdict() if matches is not None else None

    return url_dict


class WebsiteNotImplementedError(NotImplementedError):
    '''Error for when the website is not supported by this library.'''
    pass


def scrape_me(url_path):
    host_name = url_path_to_dict(url_path.replace('://www.', '://'))['host']

    try:
        scraper = SCRAPERS[host_name]
    except KeyError:
        raise WebsiteNotImplementedError(
            "Website ({}) is not supported".format(host_name))

    return scraper(url_path)


def scrape(url):
    """
    Get a cookbox recipe from a URL.
    Does not save the recipe, but returns its instance.
    """
    scraper = scrape_me(url)

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

__all__ = ['scrape']

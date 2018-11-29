from recipe_scrapers import scrape_me

from cookbox_core.models import Recipe


def scrape(url):
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
                description= ing[1],
                position= idx)

    for idx, instruction in enumerate(scraper.instructions()):
        recipe.instructions.create(instruction = instruction, position= idx)
    
    return recipe

# Created by Oleksandr Sorochynskyi
# On 18/05/2020

# Scrape recipes found in schema.org Recipe type
import re

import requests
from extruct import extract

from django.db import transaction
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from cookbox_core.models import Recipe

from cookbox_scraper._utils import (
    parse_ingredients,
    normalize_instructions,
    parse_iso8601,
    normalize_string,
)

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

COOKIES = {
    'euConsentFailed': 'true',
    'euConsentID': 'e48da782-e1d1-0931-8796-d75863cdfa15',
}

class WebsiteNotImplementedError(NotImplementedError):
    '''Error for when the website is not supported by this library.'''
    pass

def recipe_title(dd):
    return normalize_string(dd['name'])

def recipe_description(dd):
    if 'description' in dd.keys():
        return normalize_string(dd['description'])
    else:
        return "Description missing"

def recipe_time_unit(dd):
    return Recipe.HRS

def recipe_time(dd):
    if 'prepTime' in dd.keys():
        prep_time = parse_iso8601(dd['prepTime'])
    else:
        prep_time = (Recipe.HRS, 0.0)
    
    if 'cookTime' in dd:
        cook_time = parse_iso8601(dd['cookTime'])
    else:
        cook_time = (Recipe.HRS, 0.0)
    return (prep_time[1] + cook_time[1], prep_time[1], cook_time[1])

def recipe_yield(dd):
    return "serving"

def recipe_yields(dd):
    if not'recipeYield' in dd.keys():
        return (1.0, 1.0)
    
    if isinstance(dd['recipeYield'], list):
            dd['recipeYield'] = dd['recipeYield'][0]
    
    if not isinstance(dd['recipeYield'], str):
        dd['recipeYield'] = str(dd['recipeYield'])

    m = re.search(r"(\d+)", dd['recipeYield'])
    if m:
        return (m.group(), 1.0)

    return (1.0, 1.0)

def get_recipe_data(url):
    
    def _find_recipe(c):
        if isinstance(c, dict):
            if "@type" in c.keys() and c["@type"] == "Recipe":
                return c
            for i in c.values():
                res = _find_recipe(i)
                if res:
                    return res
        if isinstance(c, list):
            for i in c:
                res = _find_recipe(i)
                if res:
                    return res
        return []

    html = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data_list = extract(html.text, uniform=True)

    recipe_data = _find_recipe(data_list)
    if not recipe_data:
        raise WebsiteNotImplementedError(
            "Website does not provide a schema.org Recipe schema in a json-ld format"
        )
    return recipe_data

def save_image_url_in_field(url, field, file_name):
    img = requests.get(url, headers=HEADERS, cookies=COOKIES).content

    with NamedTemporaryFile() as file:
        file.write(img)
        file.flush()
        img_name = file_name 
        field.save(img_name, File(file), save=True)
    return field

def scrape_recipe(data):
    time_tuple = recipe_time(data)
    yield_tuple = recipe_yields(data)

    recipe = Recipe.objects.create(
        name = recipe_title(data),
        description = recipe_description(data),
        unit_time = recipe_time_unit(data),
        total_time = time_tuple[1] + time_tuple[0],
        preparation_time = time_tuple[0],
        cook_time = time_tuple[1],
        unit_yield = "serving",
        total_yield = yield_tuple[0],
        serving_size = yield_tuple[1],
        source = data['url'] if 'url' in data.keys() else ""
    )

    if isinstance(data["image"], str):
        data["image"] = [ data["image"] ]

    # Get image
    save_image_url_in_field(
        data["image"],
        recipe.image,
        str(recipe.id) + "_thumb.png"
    )

    # Ingredients
    if 'recipeIngredient' in data.keys():
        group = recipe.ingredient_groups.create(name = "", position = 0)
        for idx, ing in enumerate(parse_ingredients(data['recipeIngredient'])):
            group.ingredients.create(
                quantity = ing[0],
                unit = ing[1],
                description= ing[2],
                position= idx
            )

    # Instructions
    if not 'recipeInstructions' in data.keys():
        data['recipeInstructions'] = []

    if not isinstance(data['recipeInstructions'], list):
        data['recipeInstructions'] = [ data['recipeInstructions'] ]

    if all(
        isinstance(elem, str)
        for elem in data['recipeInstructions']
    ):
        for idx, instruction in normalize_instructions(
            data['recipeInstructions']
        ):
            recipe.instructions.create(
                instruction = instruction,
                position= idx
            )

    if all(
        isinstance(elem, dict)
        for elem in data['recipeInstructions']
    ):
        def list_from_howtostep_list(lst):
            ret = []
            for item in lst:
                if "@type" not in item.keys():
                    continue
                if item["@type"] == "HowToStep":
                    ret.append(item["text"])
            return ret

        ins = [] 
        for item in data['recipeInstructions']:
            if "@type" not in item.keys():
                continue
            if item["@type"] == "HowToSection":
                if "name" in item.keys():
                    ins.append("# " + item["name"])
                ins += list_from_howtostep_list(item["itemListElement"])
            if item["@type"] == "HowToStep":
                ins.append(item["text"])
        for idx, instruction in enumerate(normalize_instructions(ins)):
            recipe.instructions.create(
                instruction = instruction,
                position= idx
            )
    
    return recipe

def scrape(url):
    """
    Get a cookbox recipe from a URL.
    Does not save the recipe, but returns its instance.
    """
    data = get_recipe_data(url)
    
    with transaction.atomic():
        return scrape_recipe(data)

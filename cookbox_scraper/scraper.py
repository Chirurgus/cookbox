# Created by Oleksandr Sorochynskyi
# On 18/05/2020

# Scrape recipes found in schema.org Recipe type
import re
from collections import namedtuple

import requests
from requests.exceptions import MissingSchema
from extruct import extract

from django.db import transaction
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from cookbox_core.models import Recipe, Tag

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
    Recipe_yield = namedtuple("Recipe_yield", ["unit", "yield_size", "serving_size"])

    if not'recipeYield' in dd.keys():
        return Recipe_yield("serving", 1.0, None)
    
    if isinstance(dd['recipeYield'], list):
        # If there are two values the first one is the yield unit
        if len(dd['recipeYield']) == 2:
            return Recipe_yield(
                dd['recipeYield'][1],
                dd['recipeYield'][0],
                None
            )
        dd['recipeYield'] = dd['recipeYield'][0]
        
    if not isinstance(dd['recipeYield'], str):
        dd['recipeYield'] = str(dd['recipeYield'])

    m = re.search(r"(\d+)", dd['recipeYield'])
    if m:
        return Recipe_yield(m.group(), 1.0, None)

    return Recipe_yield("serving", 1.0, None)

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
        raise MissingSchema(
            "Website does not provide a schema.org Recipe schema in a json-ld format"
        )
    return recipe_data

def save_image_url_in_field(url, field, file_name):
    # Handle scheme relative urls
    if url.startswith("//"):
        url = "https:" + url
    img = requests.get(url, headers=HEADERS, cookies=COOKIES).content

    with NamedTemporaryFile() as file:
        file.write(img)
        file.flush()
        img_name = file_name 
        field.save(img_name, File(file), save=True)
    return field

def scrape_instructions(recipe, ri):
    '''
    Scrape instructions form 'recipeInstructions' schema

    @param ri an object form "Recipe" scema.org schema
    @param recipe an instance of cookbox_core.models.Recipe
    '''
    if not isinstance(ri, list):
        ri = [ ri ]

    if all(
        isinstance(elem, str)
        for elem in ri
    ):
        for idx, instruction in normalize_instructions(ri):
            recipe.instructions.create(
                instruction=instruction,
                position=idx
            )
        return recipe

    def _scrape_how_to_step(step, recipe, pos_counter):
        if "@type" not in step.keys() or step["@type"] != "HowToStep":
            return pos_counter

        for norm_ins in normalize_instructions([ step["text"] ]):
            ins = recipe.instructions.create(
                instruction=norm_ins,
                position=pos_counter
            )
            pos_counter += 1

        # Add images for instructions
        if "image" in step.keys():
            if isinstance(step["image"], list):
                step["image"] = step["image"][0]
            note = ins.notes.create()
            save_image_url_in_field(
                step["image"],
                note.image,
                "{id1}_{id2}_{id3}_thumb.png". format(
                    id1=str(recipe.id),
                    id2=str(ins.id),
                    id3=str(note.id)
                )
            )
        return pos_counter

    if all(
        isinstance(elem, dict)
        for elem in ri
    ):
        pos_counter = 0
        for item in ri:
            if "@type" not in item.keys():
                continue
            if item["@type"] == "HowToStep":
                pos_counter = _scrape_how_to_step(step, recipe, pos_counter)
            if item["@type"] == "HowToSection":
                if "name" in item.keys():
                    recipe.instructions.create(
                        instruction = item["name"],
                        position=pos_counter
                    )
                    pos_counter += 1
                if "itemListElement" not in item.keys():
                    continue
                for step in item["itemListElement"]:
                    pos_counter = _scrape_how_to_step(step, recipe, pos_counter)
    return recipe
     

def scrape_recipe(data):
    time_tuple = recipe_time(data)
    yield_tuple = recipe_yield(data)

    recipe = Recipe.objects.create(
        name = recipe_title(data),
        description = recipe_description(data),
        unit_time = recipe_time_unit(data),
        total_time = time_tuple[1] + time_tuple[0],
        preparation_time = time_tuple[0],
        cook_time = time_tuple[1],
        unit_yield = yield_tuple.unit,
        total_yield = yield_tuple.yield_size,
        serving_size = yield_tuple.serving_size,
        source = data['url'] if 'url' in data.keys() else ""
    )

    if isinstance(data["image"], str):
        data["image"] = [ data["image"] ]

    # Get image
    save_image_url_in_field(
        data["image"][0],
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
    if 'recipeInstructions' in data.keys():
        scrape_instructions(recipe, data["recipeInstructions"])

    # Tags
    # Collect potential tags
    tags = []
    if "keywords" in data.keys():
        tags += "".join(data["keywords"].split()).split(',')
    if "recipeCategory" in data.keys():
        if isinstance(data["recipeCategory"], str):
            data["recipeCategory"] = [ data["recipeCategory"] ]
        tags += data["recipeCategory"]
    if "recipeCuisine" in data.keys():
        if isinstance(data["recipeCuisine"], str):
            data["recipeCuisine"] = [ data["recipeCuisine"] ]
        tags += data["recipeCuisine"]
    tags = [ tag.lower() for tag in tags ]

    for tag in Tag.objects.filter(name__in=tags):
        tag.recipes.add(recipe)
    
    return recipe

def scrape(url):
    """
    Get a cookbox recipe from a URL.
    Does not save the recipe, but returns its instance.
    """
    data = get_recipe_data(url)
    
    with transaction.atomic():
        recipe = scrape_recipe(data)
        if recipe.source == "":
            recipe.source = url
        return recipe

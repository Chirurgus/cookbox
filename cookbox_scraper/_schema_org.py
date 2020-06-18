# Created by Oleksandr Sorochynskyi
# On 18/05/2020

# Scrape recipes found in schema.org Recipe type
import re

import requests
from extruct import extract
import pprint as pp

from cookbox_core.models import Recipe

from cookbox_scraper._abstract import SchemaScraper
from cookbox_scraper._utils import (
    parse_ingredients,
    normalize_instructions,
    parse_iso8601,
    normalize_string,
)

#r = requests.get('https://www.bbc.co.uk/food/recipes/shakshouka_74716')
#data = ex.extract(r.text)
#pp.pprint(data)


class SchemaOrgRecipeScraper(SchemaScraper):
    def title(self):
        return normalize_string(self.data['name'])

    def description(self):
        if 'description' in self.data.keys():
            return normalize_string(self.data['description'])
        else:
            return "Description missing"

    def time_unit(self):
        return Recipe.HRS

    def time(self):
        """
        (total_time, prep_time, cook_time) it takes to prepare the recipe in minutes
        """
        if 'prepTime' in self.data.keys():
            prep_time = parse_iso8601(self.data['prepTime'])
        else:
            prep_time = (Recipe.HRS, 0.0)
        
        if 'cookTime' in self.data:
            cook_time = parse_iso8601(self.data['cookTime'])
        else:
            cook_time = (Recipe.HRS, 0.0)
        return (prep_time[1] + cook_time[1], prep_time[1], cook_time[1])
    
    def yield_unit(self):
        return "serving"
    
    def yields(self):
        if not'recipeYield' in self.data.keys():
            return (1.0, 1.0)
        
        if isinstance(self.data['recipeYield'], list):
            self.data['recipeYield'] = self.data['recipeYield'][0]
        
        if not isinstance(self.data['recipeYield'], str):
            self.data['recipeYield'] = str(self.data['recipeYield'])

        m = re.search(r"(\d+)", self.data['recipeYield'])
        if m:
            return (m.group(), 1.0)

        return (1.0, 1.0)

    def ingredients(self):
        if not 'recipeIngredient' in self.data.keys():
            return []
        return [ ("All", parse_ingredients(self.data['recipeIngredient']) ), ]

    def instructions(self):
        if not 'recipeInstructions' in self.data.keys():
            return []

        if not isinstance(self.data['recipeInstructions'], list):
            self.data['recipeInstructions'] = [ self.data['recipeInstructions'] ]

        if all(
            isinstance(elem, str)
            for elem in self.data['recipeInstructions']
        ):
            return normalize_instructions(
                self.data['recipeInstructions']
            )

        if all(
            isinstance(elem, dict)
            for elem in self.data['recipeInstructions']
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
            for item in self.data['recipeInstructions']:
                if "@type" not in item.keys():
                    continue
                if item["@type"] == "HowToSection":
                    ins += list_from_howtostep_list(item["itemListElement"])
                if item["@type"] == "HowToStep":
                    ins.append(item["text"])
            return normalize_instructions(ins)

        return []

    def notes(self):
        '''
        List of notes
        '''
        return []
 


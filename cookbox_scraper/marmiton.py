from ._abstract import DOMScraper
from ._utils import get_minutes, normalize_string, parse_ingredients, normalize_instructions


class Marmiton(DOMScraper):

    @classmethod
    def host(self):
        return 'marmiton.org'

    def title(self):
        return self.soup.find('h1', {'class': 'main-title'}).get_text()

    def description(self):
        return ""

    def time(self):
        prep_time = get_minutes(self.soup.find(
            'span',
            {'class': 'recipe-infos__timmings__value'}
        ))

        cook_time = get_minutes(self.soup.find(
            'span',
            {'class': 'recipe-infos__timmings__value'}
        ))

        total_time = prep_time + cook_time

        return (total_time, prep_time, cook_time)

    def yield_unit(self):
        return "Servings"

    def yields(self):
        nservings = self.soup.find('span', {'class': 'recipe-infos__quantity__value'}).get_text()

        return (float(nservings), 1)

    def ingredients(self):
        ing_qty = self.soup.findAll(
            'span',
            { 'class' : 'recipe-ingredient-qt' }
        )

        ing_desc = self.soup.findAll(
            'span',
            { 'class' : 'ingredient' }
        )

        ing_desc_comp = self.soup.findAll(
            'span',
            { 'class' : 'recipe-ingredient__complement' }
        )

        qty = [
            float(q.get_text())
            if q.get_text().strip() != ''
            else 0
            for q in ing_qty
        ]

        desc = [
            normalize_string(' '.join([ di.get_text() for di in d ]))
            for d in zip(ing_desc, ing_desc_comp)
        ]

        ingredients = [ (ing[0], None, ing[1]) for ing in zip(qty, desc) ]

        return [('All', ingredients)]

    def instructions(self):
        instructions = self.soup.findAll(
            'li',
            {'class': 'recipe-preparation__list__item'}
        )

        return normalize_instructions(
            [
            normalize_string(instruction.get_text())
            for instruction in instructions
            ]
        )

    def notes(self):
        return []
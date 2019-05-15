""" Created by Oleksandr Sorochynskyi """
""" On 29/04/2019 """

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    Tag,
    TagCategory,
)
from cookbox_core.tests import RecipeBaseTest

from cookbox_webui.forms import RecipeForm

class RecipeFormTest(RecipeBaseTest):
    # Form data to be used for tests
    form_data_no_related = {
        'name': 'Test recipe',
        'description': 'A test recipe.',
        'unit_time': 'min',
        'cook_time': '0',
        'preparation_time': '3',
        'total_time': '3',
        'unit_yield': 'a cookbox recipe',
        'total_yield': '1',
        'serving_size': '1',
        'source': 'ME',
        'image': ''
    }
    form_data_ingredient_group_only = {
        'ingredient_groups-INITIAL_FORMS': '0',
        'ingredient_groups-MAX_NUM_FORMS': '1000',
        'ingredient_groups-MIN_NUM_FORMS': '0',
        'ingredient_groups-TOTAL_FORMS': '1',

        'ingredient_groups-0-id': '',
        'ingredient_groups-0-name': 'An ingredient group',
        'ingredient_groups-0-position': '0',
        'ingredient_groups-0-recipe': '',

        'ingredient_groups-0-ingredients-INITIAL_FORMS': '0',
        'ingredient_groups-0-ingredients-MAX_NUM_FORMS': '1000',
        'ingredient_groups-0-ingredients-MIN_NUM_FORMS': '0',
        'ingredient_groups-0-ingredients-TOTAL_FORMS': '2',

        'ingredient_groups-0-ingredients-0-description': 'test ingredient',
        'ingredient_groups-0-ingredients-0-group': '',
        'ingredient_groups-0-ingredients-0-id': '',
        'ingredient_groups-0-ingredients-0-position': '0',
        'ingredient_groups-0-ingredients-0-quantity': '1',
        'ingredient_groups-0-ingredients-0-unit': 'unit',

        'ingredient_groups-0-ingredients-1-description': '2nd test ingredient',
        'ingredient_groups-0-ingredients-1-group': '',
        'ingredient_groups-0-ingredients-1-id': '',
        'ingredient_groups-0-ingredients-1-position': '1',
        'ingredient_groups-0-ingredients-1-quantity': '1',
        'ingredient_groups-0-ingredients-1-unit': 'unit',

        'ingredient_groups-0-ingredients-__prefix__-description': '',
        'ingredient_groups-0-ingredients-__prefix__-group': '',
        'ingredient_groups-0-ingredients-__prefix__-id': '',
        'ingredient_groups-0-ingredients-__prefix__-position': '0',
        'ingredient_groups-0-ingredients-__prefix__-quantity': '',
        'ingredient_groups-0-ingredients-__prefix__-unit': '',

        'ingredient_groups-__prefix__-id': '',
        'ingredient_groups-__prefix__-ingredients-INITIAL_FORMS': '0',
        'ingredient_groups-__prefix__-ingredients-MAX_NUM_FORMS': '1000',
        'ingredient_groups-__prefix__-ingredients-MIN_NUM_FORMS': '0',
        'ingredient_groups-__prefix__-ingredients-TOTAL_FORMS': '0',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-description': '',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-group': '',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-id': '',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-position': '',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-quantity': '',
        'ingredient_groups-__prefix__-ingredients-__nested_prefix__-unit': '',
        'ingredient_groups-__prefix__-name': '',
        'ingredient_groups-__prefix__-position': '',
        'ingredient_groups-__prefix__-recipe': '',
    }
    form_data_instructions_only = {
        'instructions-INITIAL_FORMS': '0',
        'instructions-MAX_NUM_FORMS': '1000',
        'instructions-MIN_NUM_FORMS': '0',
        'instructions-TOTAL_FORMS': '2',

        'instructions-0-id': '',
        'instructions-0-instruction': 'A test instruction',
        'instructions-0-position': '0',
        'instructions-0-recipe': '',

        'instructions-1-id': '',
        'instructions-1-instruction': 'Another test instruction',
        'instructions-1-position': '1',
        'instructions-1-recipe': '',

        'instructions-__prefix__-id': '',
        'instructions-__prefix__-instruction': '',
        'instructions-__prefix__-position': '',
        'instructions-__prefix__-recipe': '',
    }
    form_data_notes_only = {
        'notes-INITIAL_FORMS': '0',
        'notes-MAX_NUM_FORMS': '1000',
        'notes-MIN_NUM_FORMS': '0',
        'notes-TOTAL_FORMS': '1',

        'notes-0-id': '',
        'notes-0-recipe': '',
        'notes-0-text': 'A test note',

        'notes-__prefix__-id': '',
        'notes-__prefix__-recipe': '',
        'notes-__prefix__-text': '',
    }

    def test_form_no_related_is_valid(self):
        form_data = self.form_data_no_related

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form_data = self.form_data_no_related
        form_data.update(self.form_data_ingredient_group_only)
        form_data.update(self.form_data_instructions_only)
        form_data.update(self.form_data_notes_only)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = self.form_data_no_related
        form_data.update(self.form_data_ingredient_group_only)
        form_data.update(self.form_data_instructions_only)
        form_data.update(self.form_data_notes_only)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
    
    def test_form_save_check_values_outside_related(self):
        form_data = self.form_data_no_related
        form_data.update(self.form_data_ingredient_group_only)
        form_data.update(self.form_data_instructions_only)
        form_data.update(self.form_data_notes_only)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
        recipe = form.save()
        
        for key, value in self.form_data_no_related.items():
            self.assertEqual(getattr(recipe, key), value)



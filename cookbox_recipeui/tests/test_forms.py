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

from cookbox_recipeui.forms import RecipeForm

class RecipeFormTest(RecipeBaseTest):
    form_data_recipe_no_related = {
        'name': ['Test recipe'],
        'description': ['Test description'],
        'unit_time': ['min.'],
        'total_time': ['23'],
        'preparation_time': ['23'],
        'cook_time': ['23'],
        'unit_yield': ['23'],
        'total_yield': ['23'],
        'serving_size': ['23'],
        'source': ['23'],
        'image': [''],
    }
    form_data_ingredients = {
         'formset-ingredient_groups-TOTAL_FORMS': ['2'],
         'formset-ingredient_groups-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-0-id': [''],
         'formset-ingredient_groups-0-recipe': [''],
         'formset-ingredient_groups-0-position': ['0'],
         'formset-ingredient_groups-0-name': ['Test ingredient group 1'],
         'formset-ingredient_groups-0-formset-ingredients-TOTAL_FORMS': ['2'],
         'formset-ingredient_groups-0-formset-ingredients-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-0-formset-ingredients-0-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-group': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-position': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-0-quantity': ['1'],
         'formset-ingredient_groups-0-formset-ingredients-0-unit': ['test unit'],
         'formset-ingredient_groups-0-formset-ingredients-0-description': ['ingredient1'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-TOTAL_FORMS': ['1'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-0-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-0-ingredient': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-0-text': ['test ingredeint comment1'],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-0-image': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-0-formset-ingredients-0-formset-notes-__note_prefix__-image': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-group': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-position': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-1-quantity': ['2'],
         'formset-ingredient_groups-0-formset-ingredients-1-unit': ['test units'],
         'formset-ingredient_groups-0-formset-ingredients-1-description': ['ingredient 2'],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-0-formset-ingredients-1-formset-notes-__note_prefix__-image': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-group': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-position': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-quantity': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-unit': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-description': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-0-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-image': [''],
         'formset-ingredient_groups-1-id': [''],
         'formset-ingredient_groups-1-recipe': [''],
         'formset-ingredient_groups-1-position': ['1'],
         'formset-ingredient_groups-1-name': ['Ingredient group 2'],
         'formset-ingredient_groups-1-formset-ingredients-TOTAL_FORMS': ['1'],
         'formset-ingredient_groups-1-formset-ingredients-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-1-formset-ingredients-0-id': [''],
         'formset-ingredient_groups-1-formset-ingredients-0-group': [''],
         'formset-ingredient_groups-1-formset-ingredients-0-position': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-0-quantity': ['3'],
         'formset-ingredient_groups-1-formset-ingredients-0-unit': ['unit'],
         'formset-ingredient_groups-1-formset-ingredients-0-description': ['ingredient from test group 2'],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-1-formset-ingredients-0-formset-notes-__note_prefix__-image': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-id': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-group': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-position': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-quantity': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-unit': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-description': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-1-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-image': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-id': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-recipe': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-position': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-name': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-id': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-group': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-position': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-quantity': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-unit': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-description': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-TOTAL_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-INITIAL_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-id': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-ingredient': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-text': [''],
         'formset-ingredient_groups-__ingredient_group_prefix__-formset-ingredients-__ingredient_prefix__-formset-notes-__note_prefix__-image': [''],
    }
    form_data_instructions = {
         'formset-instructions-TOTAL_FORMS': ['2'],
         'formset-instructions-INITIAL_FORMS': ['0'],
         'formset-instructions-MIN_NUM_FORMS': ['0'],
         'formset-instructions-MAX_NUM_FORMS': ['1000'],
         'formset-instructions-0-id': [''],
         'formset-instructions-0-recipe': [''],
         'formset-instructions-0-position': ['0'],
         'formset-instructions-0-instruction': ['Instrucion 1'],
         'formset-instructions-0-formset-notes-TOTAL_FORMS': ['0'],
         'formset-instructions-0-formset-notes-INITIAL_FORMS': ['0'],
         'formset-instructions-0-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-instructions-0-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-instructions-0-formset-notes-__note_prefix__-id': [''],
         'formset-instructions-0-formset-notes-__note_prefix__-instruction': [''],
         'formset-instructions-0-formset-notes-__note_prefix__-text': [''],
         'formset-instructions-0-formset-notes-__note_prefix__-image': [''],
         'formset-instructions-1-id': [''],
         'formset-instructions-1-recipe': [''],
         'formset-instructions-1-position': ['0'],
         'formset-instructions-1-instruction': ['Instruction 2'],
         'formset-instructions-1-formset-notes-TOTAL_FORMS': ['2'],
         'formset-instructions-1-formset-notes-INITIAL_FORMS': ['0'],
         'formset-instructions-1-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-instructions-1-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-instructions-1-formset-notes-0-id': [''],
         'formset-instructions-1-formset-notes-0-instruction': [''],
         'formset-instructions-1-formset-notes-0-text': ['Instruction 2 note 1'],
         'formset-instructions-1-formset-notes-0-image': [''],
         'formset-instructions-1-formset-notes-1-id': [''],
         'formset-instructions-1-formset-notes-1-instruction': [''],
         'formset-instructions-1-formset-notes-1-text': ['Instruction 2 note 2'],
         'formset-instructions-1-formset-notes-1-image': [''],
         'formset-instructions-1-formset-notes-__note_prefix__-id': [''],
         'formset-instructions-1-formset-notes-__note_prefix__-instruction': [''],
         'formset-instructions-1-formset-notes-__note_prefix__-text': [''],
         'formset-instructions-1-formset-notes-__note_prefix__-image': [''],
         'formset-instructions-__instruction_prefix__-id': [''],
         'formset-instructions-__instruction_prefix__-recipe': [''],
         'formset-instructions-__instruction_prefix__-position': [''],
         'formset-instructions-__instruction_prefix__-instruction': [''],
         'formset-instructions-__instruction_prefix__-formset-notes-TOTAL_FORMS': ['0'],
         'formset-instructions-__instruction_prefix__-formset-notes-INITIAL_FORMS': ['0'],
         'formset-instructions-__instruction_prefix__-formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-instructions-__instruction_prefix__-formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-instructions-__instruction_prefix__-formset-notes-__note_prefix__-id': [''],
         'formset-instructions-__instruction_prefix__-formset-notes-__note_prefix__-instruction': [''],
         'formset-instructions-__instruction_prefix__-formset-notes-__note_prefix__-text': [''],
         'formset-instructions-__instruction_prefix__-formset-notes-__note_prefix__-image': [''],
    }
    form_data_notes = {
         'formset-notes-TOTAL_FORMS': ['2'],
         'formset-notes-INITIAL_FORMS': ['0'],
         'formset-notes-MIN_NUM_FORMS': ['0'],
         'formset-notes-MAX_NUM_FORMS': ['1000'],
         'formset-notes-0-id': [''],
         'formset-notes-0-recipe': [''],
         'formset-notes-0-text': ['Note 1'],
         'formset-notes-0-image': [''],
         'formset-notes-1-id': [''],
         'formset-notes-1-recipe': [''],
         'formset-notes-1-text': ['Note 2'],
         'formset-notes-1-image': [''],
         'formset-notes-__note_prefix__-id': [''],
         'formset-notes-__note_prefix__-recipe': [''],
         'formset-notes-__note_prefix__-text': [''],
         'formset-notes-__note_prefix__-image': [''],
    }

    def test_form_is_valid_no_related(self):
        form_data = self.form_data_recipe_no_related

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form_data = self.form_data_recipe_no_related
        form_data.update(self.form_data_ingredients)
        form_data.update(self.form_data_instructions)
        form_data.update(self.form_data_notes)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = self.form_data_recipe_no_related
        form_data.update(self.form_data_ingredients)
        form_data.update(self.form_data_instructions)
        form_data.update(self.form_data_notes)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        instance.delete()
    
    def test_form_save_check_values_outside_related(self):
        form_data = self.form_data_recipe_no_related
        form_data.update(self.form_data_ingredients)
        form_data.update(self.form_data_instructions)
        form_data.update(self.form_data_notes)

        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
        recipe = form.save()
        
        for key, value in self.form_data_recipe_no_related.items():
            self.assertEqual(getattr(recipe, key), value)



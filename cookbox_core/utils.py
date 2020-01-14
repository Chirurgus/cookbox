# Created by Oleksandr Sorochynskyi
# On 14/01/2020

from copy import deepcopy

from django.db import transaction

def _copy_model(instance):
    copy = deepcopy(instance)
    copy.id = None
    copy.save()
    return copy

def _duplicate_recipe(recipe):
    new = _copy_model(recipe)

    for ing_grp in recipe.ingredient_groups.all():
        new_ing_grp = _copy_model(ing_grp)
        for ing in ing_grp.ingredients.all():
            new_ing = _copy_model(ing)
            new_ing_grp.ingredients.add(new_ing)
            for ing_note in ing.notes.all():
                new_note = _copy_model(ing_note)
                new_ing.notes.add(new_note)
        new.ingredient_groups.add(new_ing_grp)
    
    for ins in recipe.instructions.all():
        new_ins = _copy_model(ins)
        for ins_note in ins.notes.all():
            new_note = _copy_model(ins_note)
            new_ins.notes.add(new_note)
    
    for note in recipe.notes.all():
        new_note = _copy_model(note)
        new.notes.add(new_note)
    
    new.tags.add(recipe.tags.all())
    return new

def duplicate_recipe(recipe):
    '''
    Duplicate a `cookbox_core.models.Recipe`

    Duplicates a recipe. All database operations are done
    within a transaction.

    :param recipe Recipe: A recipe to be copied.
    :returns Recipe: A cope of the provided recipe, in a new model instance.
    '''
    with transaction.atomic():
        return _duplicate_recipe(recipe)
    
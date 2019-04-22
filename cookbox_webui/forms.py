from collections import OrderedDict

from django.forms import (
    Form,
    ModelForm,
    inlineformset_factory,
    formset_factory,
    Textarea,
    ModelChoiceField,
    ModelMultipleChoiceField,
)

from dal.autocomplete import ModelSelect2Multiple

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag,
    TagCategory,
)

from .nested_form import (
    BaseNestedModelForm,
    BaseNestedInnerFormSet,
    nestedformset_factory,
)

class RecipeForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset= Tag.objects.all(),
                                    widget= ModelSelect2Multiple(url= 'recipe-tag-autocomplete'),
                                    required= False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recipe = kwargs.get('instance')
        if not recipe is None:
            self.fields['tags'].initial = recipe.tags.all()
        else:
            self.fields['tags'].inital = []

    def save(self, commit=True):
        '''
        Same as ModelForm.save(), but also saves tags if commit=True
        '''
        ret = super(ModelForm, self).save(commit)
        if commit:
            self.save_tags()
        return ret
    
    def save_tags(self):
        '''
        Saves tags many2many field.
        Gets called automatically from save(commit=True) method.
        '''
        old_tags = self.instance.tags.all()
        new_tags = self.cleaned_data['tags'] 
        for tag in new_tags.difference(old_tags):
            self.instance.tags.add(tag)
        for tag in old_tags.difference(new_tags):
            self.instance.tags.remove(tag)
 
        
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'unit_time',
            'total_time',
            'preparation_time',
            'cook_time',
            'unit_yield',
            'total_yield',
            'serving_size',
            'source',
            'image',
            'tags',
        ]
        labels = {
            'name': 'Recipe name',
            'unit_time': 'Time measurement unit',
            'unit_yield': 'Yield measurement unit',
        }
        widgets = {
            'name': Textarea(attrs={}),
            'description': Textarea(attrs={}),
            'source': Textarea(attrs={}),
        }
    

class IngredientGroupForm(BaseNestedModelForm):
    class Meta:
        model = IngredientGroup
        fields = ['position', 'name']
        widgets = {
            'name': Textarea(attrs={}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['position', 'quantity', 'unit', 'description']
        widgets = {
            'description': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        fields = ['position', 'instruction']
        widgets = {
            'instruction': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class NoteForm(ModelForm):
    class Meta:
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={}),
        }
        abstract = True

class InstructionNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = InstructionNote
        abstract = False

class IngredientNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = IngredientNote
        abstract = False

class RecipeNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = RecipeNote
        abstract = False

class TagForm(ModelForm):
    category = ModelChoiceField(queryset= TagCategory.objects.all(),
                                required= False)

    class Meta:
        model = Tag
        fields = ['name', 'category']

class TagCategoryForm(ModelForm):
    class Meta:
        model = TagCategory
        fields = ['name']

InstructionFormset = inlineformset_factory(Recipe, Instruction, form= InstructionForm, extra=0)
IngredientFormset = inlineformset_factory(IngredientGroup, Ingredient, form= IngredientForm, formset= BaseNestedInnerFormSet, extra=0)
RecipeNoteFormset = inlineformset_factory(Recipe, RecipeNote, form= RecipeNoteForm, extra= 0)
IngredientNoteFormset = inlineformset_factory(Ingredient, IngredientNote, form= IngredientNoteForm, extra= 0)
InstructionNoteFormset = inlineformset_factory(Instruction, InstructionNote, form= InstructionNoteForm, extra= 0)
IngredientGroupFormset = nestedformset_factory(Recipe, IngredientGroup, IngredientFormset, form= IngredientGroupForm, extra= 0)

class RecipeCompleteForm():
    '''
    Class to manage all the forms used to create/edit Recipes
    '''
    RECIPE_FORM = 'recipe_form'
    INGREDIENT_GROUPS = 'ingredient_group_forms'
    INSTRUCTIONS = 'instruction_forms'
    NOTES = 'note_forms'

    def __init__(self, *args, **kwargs):
        self.forms = OrderedDict()
        self.forms[self.RECIPE_FORM] = RecipeForm(*args, **kwargs)
        self.forms[self.INGREDIENT_GROUPS] = IngredientGroupFormset(prefix= 'ingredient_groups', *args, **kwargs)
        self.forms[self.INSTRUCTIONS] = InstructionFormset(prefix= 'instructions', *args, **kwargs)
        self.forms[self.NOTES] = RecipeNoteFormset(prefix= 'notes', *args, **kwargs)

        # Create a human readable label
        self.forms[self.RECIPE_FORM].custom_label = ""
        self.forms[self.INGREDIENT_GROUPS].custom_label = "Ingredient groups"
        self.forms[self.INSTRUCTIONS].custom_label = "Instructions"
        self.forms[self.NOTES].custom_label = "Notes"

    # Inserts a new recipe instance in the database
    def create(self):
        recipe = self.forms[self.RECIPE_FORM].save()
        for key, form in self.forms.items():
            form.instance = recipe
            form.save()

    # Updates an existing recipe instance
    def save(self):
        '''
        Update an existing recipe instance.
        Note that RecipeForm.save(commit=True) method saves the tags
        '''
        for key, form in self.forms.items():
            form.save(commit=True)

    # Checks validity of the data in the form
    def is_valid(self):
        valid = True
        recipe = self.forms[self.RECIPE_FORM].save(commit= False)
        for key, form in self.forms.items():
            # Why am I assigning recipe here?
            if not form.instance:
                form.instance = recipe
            valid = form.is_valid() and valid 
        return valid

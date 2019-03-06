from collections import OrderedDict

from django.forms import (
    Form,
    ModelForm,
    inlineformset_factory,
    formset_factory,
    Textarea,
    CharField,
    BooleanField
)

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag,
    CHAR_FIELD_MAX_LEN_SHORT
)

from .nested_form import (
    BaseNestedModelForm,
    BaseNestedInnerFormSet,
    nestedformset_factory,
)

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'unit_time', 'total_time', 'preparation_time', 'cook_time', 'unit_yield', 'total_yield', 'serving_size', 'source', 'image']
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

class RecipeTagForm(Form):
    '''
    Represents a single item in a recipe tag formset.
    If it is already a tag, it just adds the recipe to it.
    If not it creates a new tag with this name.
    '''
    name = CharField(max_length= CHAR_FIELD_MAX_LEN_SHORT, min_length= 1)
    delete = BooleanField(required= False, initial= False)

    # Instance of the recipe
    instance = None

    def __init__(self, *args, instance, **kwargs):
        super(RecipeTagForm, self).__init__(*args, **kwargs)
        self.instance = instance

    def save(self, commit= True):
        if self.cleaned_data['delete']:
            pass
        tag_name = self.cleaned_data['name']
        tags = Tag.objects.filter(name=tag_name)
        tag = None
        if len(tags) == 0:
            tag = Tag(name=tag_name)
            tag.save()
        else:
            tag = tags[0]
        tag.recipes.add(self.instance)
    
    def create(self):
        self.save()

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


InstructionFormset = inlineformset_factory(Recipe, Instruction, form= InstructionForm, extra=0)
IngredientFormset = inlineformset_factory(IngredientGroup, Ingredient, form= IngredientForm, formset= BaseNestedInnerFormSet, extra=0)
RecipeTagFormset = formset_factory(RecipeTagForm, extra= 0)
RecipeNoteFormset = inlineformset_factory(Recipe, RecipeNote, form= RecipeNoteForm, extra= 0)
IngredientNoteFormset = inlineformset_factory(Ingredient, IngredientNote, form= IngredientNoteForm, extra= 0)
InstructionNoteFormset = inlineformset_factory(Instruction, InstructionNote, form= InstructionNoteForm, extra= 0)
IngredientGroupFormset = nestedformset_factory(Recipe, IngredientGroup, IngredientFormset, form= IngredientGroupForm, extra= 0)

class RecipeCompleteForm():
    RECIPE_FORM = 'recipe_form'
    INGREDIENT_GROUPS = 'ingredient_group_forms'
    INSTRUCTIONS = 'instruction_forms'
    NOTES = 'note_forms'
    TAGS = 'tag_forms'

    def __init__(self, *args, **kwargs):
        self.forms = OrderedDict()
        self.forms[self.RECIPE_FORM] = RecipeForm(*args, **kwargs)
        self.forms[self.INGREDIENT_GROUPS] = IngredientGroupFormset(prefix= 'ingredient_groups', *args, **kwargs)
        self.forms[self.INSTRUCTIONS] = InstructionFormset(prefix= 'instructions', *args, **kwargs)
        self.forms[self.NOTES] = RecipeNoteFormset(prefix= 'notes', *args, **kwargs)
        # Pass instance via kwargs for it to be passed to individual forms
        recipe = kwargs.pop('instance', None)
        self.forms[self.TAGS] = RecipeTagFormset(prefix= 'tags', form_kwargs= {'instance': recipe}, *args, **kwargs)

        # Create a human readable label
        self.forms[self.RECIPE_FORM].custom_label = ""
        self.forms[self.INGREDIENT_GROUPS].custom_label = "Ingredient groups"
        self.forms[self.INSTRUCTIONS].custom_label = "Instructions"
        self.forms[self.NOTES].custom_label = "Notes"
        self.forms[self.TAGS].custom_label = "Tags"

    # Inserts a new recipe instance in the database
    def create(self):
        recipe = self.forms[self.RECIPE_FORM].save()
        for form in self.forms:
            form.instance = recipe
            form.save()

    # Updates an existing recipe instance
    def save(self):
        for form in self.forms:
            form.save()

    # Checks validity of the data in the form
    def is_valid(self):
        valid = True
        recipe = self.forms[self.RECIPE_FORM].save(commit= False)
        for form in self.forms:
            if not form.instance:
                form.instance = recipe
            valid = form.is_valid() and valid 
        return valid

import random

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from dal.autocomplete import Select2QuerySetView

from recipe_scrapers import WebsiteNotImplementedError

from cookbox_core.models import Recipe, Tag

from .scrape import scrape

from .forms import (
    RecipeCompleteForm,
    TagForm,
)

from .filters import RecipeFilter


class BaseLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

class RecipeList(BaseLoginRequiredMixin, View):
    template_name = 'recipe_list.html'

    def get(self, request):
        queryset = Recipe.objects.all().order_by("-last_modified")
        filter = RecipeFilter(request.GET, queryset=queryset)
        return render(request,
                      self.template_name,
                      {'filter' : filter })

class RecipeDetail(BaseLoginRequiredMixin, View):
    template_name = 'recipe_detail.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        return render(request,
                      self.template_name,
                      { 'recipe' : recipe })

class RecipeNew(BaseLoginRequiredMixin, View):
    template_name = 'recipe_edit.html'

    def get(self, request):
        recipe_form = RecipeCompleteForm()

        return render(request,
                      self.template_name,
                      { 'form' : recipe_form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms, so POST is used even for new instances
    def post(self, request):
        recipe_form = RecipeCompleteForm(data= request.POST)

        if recipe_form.is_valid():
            recipe_form.create()
            return HttpResponseRedirect(reverse('recipe-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form,
                            'new'  : True  })

class RecipeImport(BaseLoginRequiredMixin, View):
    template_name = 'recipe_import.html'

    submit_button_name = 'import-url'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'submit_button_name' : self.submit_button_name})

    def post(self, request):
        import_url = request.POST.get(self.submit_button_name, None)
        try:
            recipe = scrape(import_url)
            return HttpResponseRedirect(
                reverse('recipe-edit',
                        kwargs= { 'pk': recipe.id }))

        except WebsiteNotImplementedError:
            return render(request,
                      self.template_name,
                      {'submit_button_name' : self.submit_button_name,
                       'error'              : 'This domain is not supported' })

class RecipeEdit(BaseLoginRequiredMixin, View):
    template_name = 'recipe_edit.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeCompleteForm(instance= recipe)

        return render(request,
            self.template_name,
            {'recipe'    : recipe,
             'form'      : recipe_form})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        form = RecipeCompleteForm(data= request.POST, files= request.FILES, instance= recipe)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('recipe-detail',
                        kwargs= {'pk': pk}))
        else:
            return render(request,
                          self.template_name,
                          {'recipe'  : recipe,
                           'form'    : form })

class RecipeDelete(BaseLoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'recipe_delete.html'

class TagList(BaseLoginRequiredMixin, View):
    template_name = 'tag_list.html'

    def get(self, request):
        queryset = Tag.objects.all()
        return render(request,
                      self.template_name,
                      {'tags' : queryset })

class TagCreate(BaseLoginRequiredMixin, View):
    template_name = 'tag_edit.html'

    def get(self, request):
        form = TagForm()

        return render(request,
                      self.template_name,
                      { 'form' : form })

    # PUT method is not allowed for HTML forms, so POST is used even for new instances
    def post(self, request):
        form = TagForm(data= request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tag-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form })


class TagEdit(BaseLoginRequiredMixin, View):
    template_name = 'tag_edit.html'

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)

        tag_form = TagForm(instance= tag)

        return render(request,
            self.template_name,
            {'tag'    : tag,
             'form'      : tag_form})

    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)

        form = TagForm(data= request.POST, files= request.FILES, instance= tag)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                        reverse('tag-list')
                        )
        else:
            return render(request,
                          self.template_name,
                          {'tag'  : tag,
                           'form'    : form })




class TagDelete(BaseLoginRequiredMixin, DeleteView):
    model = Tag
    sucess_url = reverse_lazy('tag-list')
    template_name = 'tag_delete.html'

class RecipeTagAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


def recipe_random(request):
    ids = Recipe.objects.values_list('id', flat= True)
    rand_id = random.choice(ids)
    return HttpResponseRedirect(reverse('recipe-detail',kwargs= {'pk': rand_id}))

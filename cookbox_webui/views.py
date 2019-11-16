# Created by Oleksandr Sorochynskyi
# On 12/10/2019

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.core.paginator import Paginator

from dal.autocomplete import Select2QuerySetView

from cookbox_core.models import (
    Tag,
    TagCategory,
)

from .forms import (
    TagForm,
    TagCategoryForm,
)

class HomePageView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse("recipe-list"))

class TagList(ListView):
    template_name = 'tag/list.html'
    queryset = TagCategory.objects.all()
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uncategorized_tags = Tag.objects.filter(category=None)
        context.update({'uncategorized_tags' :uncategorized_tags})
        return context

class TagCreate(CreateView):
    template_name = 'tag/edit.html'
    model = Tag
    context_object_name = "tag"
    form_class = TagForm
    success_url = reverse_lazy('tag-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TagEdit(UpdateView):
    template_name = 'tag/edit.html'
    model = Tag
    context_object_name = "tag"
    form_class = TagForm
    success_url = reverse_lazy('tag-list')

class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('tag-list')
    template_name = 'delete.html'

class TagCategoryCreate(CreateView):
    template_name = 'tag_category/edit.html'
    model = TagCategory
    context_object_name = "category"
    form_class = TagCategoryForm
    success_url = reverse_lazy('tag-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TagCategoryEdit(UpdateView):
    template_name = 'tag_category/edit.html'
    model = TagCategory
    context_object_name = "category"
    form_class = TagCategoryForm
    success_url = reverse_lazy('tag-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = False
        return context

class TagCategoryDelete(DeleteView):
    model = TagCategory
    success_url = reverse_lazy('tag-list')
    template_name = 'delete.html'

class TagRecipeList(View):
    template_name = 'tag/detail.html'

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        qs = tag.recipes.all()
        paginator = Paginator(qs, 20)
        page = request.GET.get('page') or 1
        recipes = paginator.get_page(page)
        return render(request,
                      self.template_name,
                      {'recipes' : recipes,
                       'tag'     : tag })

# Created by Oleksandr Sorochynskyi
# On 12/10/2019

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    DeleteView,
    UpdateView,
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

class BaseLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class TagList(BaseLoginRequiredMixin, View):
    template_name = 'tag/list.html'

    def get(self, request):
        uncategorized_tags = Tag.objects.filter(category=None)
        categories = TagCategory.objects.all()
        return render(request,
                      self.template_name,
                      {'uncategorized_tags' :uncategorized_tags,
                       'categories': categories })

class TagCreate(BaseLoginRequiredMixin, View):
    template_name = 'tag/edit.html'

    def get(self, request):
        form = TagForm()

        return render(request,
                      self.template_name,
                      { 'form' : form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms,
    # so POST is used even for new instances
    def post(self, request):
        form = TagForm(data= request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tag-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : form,
                            'new'   : True })

class TagEdit(BaseLoginRequiredMixin, View):
    template_name = 'tag/edit.html'

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
    success_url = reverse_lazy('tag-list')
    template_name = 'delete.html'

class TagCategoryCreate(BaseLoginRequiredMixin, View):
    template_name = 'tag_category/edit.html'

    def get(self, request):
        form = TagCategoryForm()

        return render(request,
                      self.template_name,
                      { 'form' : form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms
    # so POST is used even for new instances
    def post(self, request):
        form = TagCategoryForm(data= request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tag-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : form,
                            'new'   : True })

class TagCategoryEdit(BaseLoginRequiredMixin, UpdateView):
    template_name = 'tag_category/edit.html'

    def get(self, request, pk):
        category = get_object_or_404(TagCategory, pk=pk)
        form = TagCategoryForm(instance= category)

        return render(request,
                        self.template_name,
                        {'category' : category,
                         'form'     : form })

    def post(self, request, pk):
        category = get_object_or_404(TagCategory, pk=pk)
        form = TagCategoryForm(data= request.POST,
                               files= request.FILES,
                               instance= category)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tag-list'))
        else:
            return render(request,
                          self.template_name,
                          {'category' : category,
                           'form'     : form })

class TagCategoryDelete(BaseLoginRequiredMixin, DeleteView):
    model = TagCategory
    success_url = reverse_lazy('tag-list')
    template_name = 'delete.html'

class TagRecipeList(BaseLoginRequiredMixin, View):
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

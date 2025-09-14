# Created by Oleksandr Sorochynskyi
# On 12/10/2019

import logging

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    View,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
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

# Set up logger
auth_logger = logging.getLogger('auth_attempts')

class CustomLoginView(LoginView):
    template_name = "login.html"
    
    def form_valid(self, form):
        """Called when login form is valid (successful login)"""
        user = form.get_user()
        auth_logger.info(
            f"Successful login - User: {user.username}, "
            f"IP: {self.get_client_ip()}, "
            f"User Agent: {self.request.META.get('HTTP_USER_AGENT', 'Unknown')}, "
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Called when login form is invalid (failed login)"""
        username = form.cleaned_data.get('username', 'Unknown')
        auth_logger.warning(
            f"Failed login attempt - User: {username}, "
            f"IP: {self.get_client_ip()}, "
            f"User Agent: {self.request.META.get('HTTP_USER_AGENT', 'Unknown')}, "
        )
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class HomePageView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse("recipe-list"))


class TagList(ListView):
    template_name = "tag/list.html"
    queryset = TagCategory.objects.all()
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uncategorized_tags = Tag.objects.filter(category=None)
        context.update({"uncategorized_tags": uncategorized_tags})
        return context


class TagCreate(CreateView):
    template_name = "tag/edit.html"
    model = Tag
    context_object_name = "tag"
    form_class = TagForm
    success_url = reverse_lazy("tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new"] = True
        return context


class TagEdit(UpdateView):
    template_name = "tag/edit.html"
    model = Tag
    context_object_name = "tag"
    form_class = TagForm
    success_url = reverse_lazy("tag-list")


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy("tag-list")
    template_name = "delete.html"


class TagCategoryCreate(CreateView):
    template_name = "tag_category/edit.html"
    model = TagCategory
    context_object_name = "category"
    form_class = TagCategoryForm
    success_url = reverse_lazy("tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new"] = True
        return context


class TagCategoryEdit(UpdateView):
    template_name = "tag_category/edit.html"
    model = TagCategory
    context_object_name = "category"
    form_class = TagCategoryForm
    success_url = reverse_lazy("tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new"] = False
        return context


class TagCategoryDelete(DeleteView):
    model = TagCategory
    success_url = reverse_lazy("tag-list")
    template_name = "delete.html"


class TagRecipeList(View):
    template_name = "tag/detail.html"

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        qs = tag.recipes.all()
        paginator = Paginator(qs, 20)
        page = request.GET.get("page") or 1
        recipes = paginator.get_page(page)
        return render(request, self.template_name, {"recipes": recipes, "tag": tag})

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination
from .models import Recipe
import os
from django.views.generic import ListView

PER_PAGE = int(os.environ.get("PER_PAGE", 9))


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = "recipes"
    ordering = ["-id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        query_set =  super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(is_published=True)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_object, pagination_range = make_pagination(self.request, context.get("recipes"), PER_PAGE)
        context.update({
            "recipes": page_object,
            "pagination_range": pagination_range
        })

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, "recipes/pages/home.html", context= {
        "recipes": page_object,
        "pagination_range": pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by("-id")
    )

    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, "recipes/pages/category.html", context= {
        "recipes": page_object,
        "pagination_range": pagination_range,
        "title": f"{recipes[0].category.name} - Category"
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, "recipes/pages/recipe-view.html", context= {
        "recipe": recipe,
        "is_detail_page": True
    })


def search(request):
    search_term = request.GET.get("search", "").strip()
    
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains = search_term) |
            Q(description__icontains = search_term)
        ),
        is_published = True
    ).order_by("-id")

    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, "recipes/pages/search.html", {
        "page_title": f"Search for '{search_term}'",
        "search_term": search_term,
        "recipes": page_object,
        "pagination_range": pagination_range,
        "additional_url_query": f"&search={search_term}"
    })

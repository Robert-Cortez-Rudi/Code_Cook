from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from project.recipes.models import Recipe
from project.authors.forms import AuthorRecipeForm

@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, "authors/pages/dashboard.html",  context={
        "recipes": recipes
    })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published=False,
        author=request.user
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, "Sua receita foi salva com sucesso!")
        return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

    return render(request, "authors/pages/dashboard_recipe.html",  context={
        "form": form
    })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_create(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, "Sua receita foi criada com sucesso!")
        return redirect(reverse("authors:dashboard"))

    return render(request, "authors/pages/dashboard_recipe.html",  context={
        "form": form,
        "form_action": reverse("authors:dashboard_recipe_create")
    })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    id = POST.get("id")

    recipe = Recipe.objects.filter(
        pk=id,
        is_published=False,
        author=request.user
    ).first()

    if not recipe:
        raise Http404()
    
    recipe.delete()

    messages.success(request, "Deleted successfully!")

    return redirect(reverse("authors:dashboard"))

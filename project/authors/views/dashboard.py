from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from project.recipes.models import Recipe
from project.authors.forms import AuthorRecipeForm 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, "authors/pages/dashboard.html",  context={
        "recipes": recipes
    })


@method_decorator(
    login_required(login_url="authors:login", redirect_field_name="next"),
    name="dispatch"
)
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        if id is not None:
            recipe = Recipe.objects.filter(
                pk=id,
                is_published=False,
                author=self.request.user
            ).first()

            if not recipe:
                raise Http404()
            
            return recipe
        return None


    def render_recipe(self, form):
        return render(self.request, "authors/pages/dashboard_recipe.html",  context={
            "form": form
        })


    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)
    

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data = request.POST or None,
            files = request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(recipe.id,)))

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url="authors:login", redirect_field_name="next"),
    name="dispatch"
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get("id"))
        recipe.delete()

        messages.success(self.request, "Deleted successfully!")

        return redirect(reverse("authors:dashboard"))
    
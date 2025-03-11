from django.test import TestCase
from django.urls import reverse, resolve
from project.recipes.views import home, category, recipe


class RecipeHomeViewTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("codecook:home"))
        self.assertIs(view.func, home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("codecook:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("codecook:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("codecook:home"))
        self.assertIn(
            "No recipes found here!",
            response.content.decode("utf-8") 
        )



class RecipeCategoryViewTest(TestCase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:category", kwargs={"category_id": 1})
        )
        self.assertIs(view.func, category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse("codecook:category", kwargs={"category_id": 100}))
        self.assertEqual(response.status_code, 404)



class RecipeDetailViewTest(TestCase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:recipe", kwargs={"id": 1})
        )
        self.assertIs(view.func, recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse("codecook:recipe", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

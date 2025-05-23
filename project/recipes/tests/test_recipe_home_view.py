from django.urls import reverse, resolve
from project.recipes.views import home
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):

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

    def test_recipe_home_template_loads_recipes(self):
        # need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse("codecook:home"))
        content = response.content.decode("UTF-8")
        response_recipe = response.context["recipes"]

        # Check if one recipe exist
        self.assertIn("Recipe title", content)
        self.assertEqual(len(response_recipe), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""

        # need a recipe for this test
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse("codecook:home"))

        # Check if one recipe exist
        self.assertIn(
            "No recipes found here!",
            response.content.decode("utf-8") 
        )

    @patch("project.recipes.views.PER_PAGE", new=3)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(qtd=8)
        
        response = self.client.get(reverse("codecook:home"))
        recipes = response.context["recipes"]
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)


    @patch("project.recipes.views.PER_PAGE", new=3)
    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qtd=8)

        response = self.client.get(reverse("codecook:home") + "?page=1A")
        self.assertEqual(response.context["recipes"].number, 1)  

        response = self.client.get(reverse("codecook:home") + "?page=2")
        self.assertEqual(response.context["recipes"].number, 2)    


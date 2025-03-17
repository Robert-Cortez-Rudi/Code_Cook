from django.test import TestCase
from django.urls import reverse, resolve
from project.recipes.views import home, category, recipe
from .test_recipe_base import RecipeTestBase


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


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:category", kwargs={"category_id": 1})
        )
        self.assertIs(view.func, category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse("codecook:category", kwargs={"category_id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"

        # need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("codecook:category", kwargs= {"category_id": 1}))
        content = response.content.decode("UTF-8")

        # Check if one recipe exist
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""

        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(reverse("codecook:recipe", kwargs={"id": recipe.category.id}))

        self.assertEqual(response.status_code, 404)



class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:recipe", kwargs={"id": 1})
        )
        self.assertIs(view.func, recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse("codecook:recipe", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It load one recipe" 

        # need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("codecook:recipe", kwargs= {"id": 1}))
        content = response.content.decode("UTF-8")

        # Check if one recipe exist
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is published False dont show"""

        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(reverse("codecook:recipe", kwargs={"id": recipe.id}))

        self.assertEqual(response.status_code, 404)

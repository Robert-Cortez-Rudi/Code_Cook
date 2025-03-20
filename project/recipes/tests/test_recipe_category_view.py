from django.urls import reverse, resolve
from project.recipes.views import category
from .test_recipe_base import RecipeTestBase



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


from django.urls import reverse, resolve
from project.recipes.views import home, category, recipe, search
from .test_recipe_base import RecipeTestBase



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


from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, category, recipe

class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse("codecook:home")
        self.assertEqual(url, "/") 

    def test_recipe_categoy_url_is_correct(self):
        url = reverse("codecook:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/") 

    def test_recipe_detail_url_is_correct(self):
        url = reverse("codecook:recipe", kwargs={"id": 1})
        self.assertEqual(url, "/recipes/1/") 


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("codecook:home"))
        self.assertIs(view.func, home)
    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:category", kwargs={"category_id": 1})
        )
        self.assertIs(view.func, category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse("codecook:recipe", kwargs={"id": 1})
        )
        self.assertIs(view.func, recipe)

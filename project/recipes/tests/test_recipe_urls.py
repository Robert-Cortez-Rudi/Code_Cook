from django.test import TestCase
from django.urls import reverse

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

    def test_recipe_search_url_is_correct(self):
        url = reverse("codecook:search")
        self.assertEqual(url, "/recipes/search/") 

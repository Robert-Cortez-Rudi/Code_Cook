from django.urls import reverse, resolve
from project.recipes.views import search
from .test_recipe_base import RecipeTestBase



class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self): 
        resolved = resolve(reverse("codecook:search")) 
        self.assertIs(resolved.func, search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("codecook:search") + "?search=testing")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse("codecook:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_is_on_page_title_and_ecaped(self):
        url = reverse("codecook:search") + "?search=<Test>"
        response = self.client.get(url)
        self.assertIn(
            "Search for &#x27;&lt;Test&gt;&#x27;",
            response.content.decode("UTF-8")
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = "This is recipe one"
        title2 = "This is recipe two"

        recipe1 = self.make_recipe(
            slug="one", title = title1, author_data= {"username": "one"}
        )
        recipe2 = self.make_recipe(
            slug="two", title = title2, author_data= {"username": "two"}
        )

        response1 = self.client.get(reverse("codecook:search") + f"?search={title1}")
        response2 = self.client.get(reverse("codecook:search") + f"?search={title2}")
        response_booth = self.client.get(reverse("codecook:search") + "?search=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])

        self.assertIn(recipe1, response_booth.context["recipes"])
        self.assertIn(recipe2, response_booth.context["recipes"])

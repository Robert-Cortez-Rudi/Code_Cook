from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self): 
        self.browser.get(self.live_server_url)
        self.sleep(5)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here", body.text)
    
    @patch("project.recipes.views.PER_PAGE", new=3)
    def test_recipe_search_input_can_find_correct_recipes(self): 
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.CLASS_NAME, "search-input") 
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            recipes[0].title,
            self.browser.find_element(By.CLASS_NAME, "main-content-list").text
        )
        self.sleep(5)
       
    @patch("project.recipes.views.PER_PAGE", new=3)
    def test_recipe_home_page_pagination(self): 
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH,
            "//a[@aria-label='Go to page 2']"
        )
        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, "recipe")), 3
        )

        self.sleep()

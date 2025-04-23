from django.test import LiveServerTestCase # Não mostra os arquivos estaticos (CSS)
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Mostra os arquivos estaticos
from utils.browser import make_browser
from time import sleep
from selenium.webdriver.common.by import By

class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def test_the_test(self):
        browser = make_browser()
        browser.get(self.live_server_url)
        sleep(5)
        body = browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here", body.text)
        browser.quit()

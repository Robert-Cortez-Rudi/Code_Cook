from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_browser
from time import sleep
from selenium.webdriver.common.by import By

class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds = 5):
        sleep(seconds)

    def get_by_id(self, web_element, id):
        return web_element.find_element(
            By.XPATH,
            id
        )

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_browser
from time import sleep

class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds = 5):
        sleep(seconds)

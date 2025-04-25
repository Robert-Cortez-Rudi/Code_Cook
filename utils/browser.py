from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import os

ROOT_PATH = Path(__file__).parent.parent
CHROME_DRIVER_NAME = "chromedriver-win64/chromedriver.exe"
CHROME_DRIVER_PATH = ROOT_PATH / "bin" / CHROME_DRIVER_NAME


def make_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == 1:
        chrome_options.add_argument("--headless")

    chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    browser = make_browser('--headless')
    browser.get("https://www.github.com/")

    sleep(5)

    browser.quit()


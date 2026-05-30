from bs4 import BeautifulSoup
import time


class WebAux:
    browser = None
    soup = None

    def __init__(self, url, browser):

        self.browser = browser
        self.browser.get(url)
        # Use BeautifulSoup to parse the HTML content of the website
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")

    def reload(self):
        self.browser.refresh()
        time.sleep(5)
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")

    def get_browser(self):
        return self.browser

    def get_soup(self):
        return self.soup

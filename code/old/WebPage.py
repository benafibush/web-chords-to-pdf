from selenium import webdriver
from bs4 import BeautifulSoup


class WebPage:

    _url: str
    _content: BeautifulSoup
    
    def __init__(self, url: str) -> None:
        self._url = url

    def __eq__(self, other: 'WebPage') -> bool:
        return (
                self._url == other._url
        )

    def store_content(self, browser: webdriver.Edge) -> None:
        self._content = BeautifulSoup(browser.page_source, "html.parser")

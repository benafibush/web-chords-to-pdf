from threading import Lock
from selenium import webdriver
from UGWebPage import UGWebPage
from TAB4UWebPage import TAB4UWebPage
from multiprocessing.pool import ThreadPool

lock = Lock()
tasks_total = 0
tasks_completed = 0
browsers = {}


class BrowsingManager:
    _thread_num = 3

    def __init__(self, domain, max_line_len):
        self._domain = domain
        self._max_line_len = max_line_len

    def load_pages_parallely(self, urls):
        global tasks_total, tasks_completed
        webpages = []
        self.make_browsers()
        tasks_total = len(urls)
        tasks_completed = 0
        with ThreadPool(self._thread_num) as pool:
            args = [(url, self._domain, self._max_line_len) for url in urls]
            for webpage in pool.starmap(BrowsingManager.make_webpage, args):
                webpages.append(webpage)
        pool.close()
        pool.join()
        self.quit_browsers()
        return webpages

    def make_browsers(self):
        global browsers
        browsers = {}
        options = webdriver.EdgeOptions()
        extension_dir_that_i_zipped = r"C:\Users\nafta\AppData\Local\Microsoft\Edge\User Data\\" + \
                                      r"Profile 1\Extensions\uBlock.zip"
        options.add_extension(extension_dir_that_i_zipped)
        for i in range(self._thread_num):
            browsers[webdriver.Edge(options=options)] = 'free'

    @staticmethod
    def quit_browsers():
        global browsers
        for browser in browsers:
            browser.quit()

    @staticmethod
    def make_webpage(url, domain, max_line_len):
        webpage = None
        browser = BrowsingManager.acquire_browser()
        browser.implicitly_wait(3)
        if domain == 'UG':
            webpage = UGWebPage(url, max_line_len, browser)
        if domain == 'TAB4U':
            webpage = TAB4UWebPage(url, max_line_len, browser)
        BrowsingManager.release_browser(browser)
        BrowsingManager.show_progress()
        return webpage

    @staticmethod
    def acquire_browser():
        global lock
        with lock:
            for browser in browsers:
                if browsers[browser] == 'free':
                    browsers[browser] = 'taken'
                    return browser

    @staticmethod
    def release_browser(browser):
        global lock
        with lock:
            browsers[browser] = 'free'

    @staticmethod
    def show_progress():
        global lock, tasks_total, tasks_completed
        with lock:
            tasks_completed += 1
            print(f'{tasks_completed}/{tasks_total} completed, {tasks_total - tasks_completed} remain.')

from .Browser import Browser
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class ThreadManager:
    def __init__(self):
        self.browser = Browser()
        self.result = []

    def get_txt_from_web(self, df):
        with ThreadPoolExecutor(max_workers=1) as executor:
            for index, row in df.iterrows():
                executor.submit(self.process_row, row)

    def process_row(self, row):
        result = self.browser.process_row(row)
        self.result.append(result)

    def get_result(self):
        return pd.DataFrame(self.result)
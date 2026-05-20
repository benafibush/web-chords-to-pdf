from Browser import Browser
import threading

class ThreadManager:
    def __init__(self):
        self.browser = Browser()
        self.threads = []
        self.result = []

    def process_dataframe(self, df):
        """Process DataFrame in parallel using threads"""
        for index, row in df.iterrows():
            thread = threading.Thread(target=self.process_row, args=(row,))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def process_row(self, row):
        """Process a single row using the Browser"""
        result = self.browser.process_row(row)
        self.result.append(result)

    def get_result(self):
        """Get the processed DataFrame"""
        df = pd.DataFrame(self.result)
        return df
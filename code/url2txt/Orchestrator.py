from .ThreadManager import ThreadManager
from .JSONReader    import JSONReader
from .TXTWriter     import TXTWriter

import pandas as pd

class Orchestrator:
    def __init__(self, json: str, txt_dir: str) -> None:
        self.json_reader    = JSONReader()
        self.thread_manager = ThreadManager()
        self.txt_writer     = TXTWriter()
        self.df             = pd.DataFrame([])
        self.json: str      = json
        self.txt_dir: str   = txt_dir

    def process_json(self) -> None:
        self.df = self.json_reader.read_json(self.json)

    def get_txt_from_web(self) -> None:
        # self.thread_manager.get_txt_from_web(self.df)
        self.df = self.thread_manager.get_result()

    def write_to_txt_files(self) -> None:
        for index, row in self.df.iterrows():
            text   = row['text']
            ID_num = row['ID']
            self.txt_writer.write_txt(self.txt_dir, ID_num, text)

    def orchestrate(self):
        self.process_json()
        self.get_txt_from_web()
        self.write_to_txt_files()

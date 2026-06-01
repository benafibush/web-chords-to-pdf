from .DBJSONReader import DBJSONReader
from .SongJSONReader import SongJSONReader
from .PDFWriter import PDFWriter


import pandas as pd


class Orchestrator:
    def __init__(self, dbjson: str, dir: str, songids: list[int]) -> None:
        self.dbjson_reader = DBJSONReader()
        self.songjson_reader = SongJSONReader()
        self.pdf_writer = PDFWriter()
        self.df = pd.DataFrame([])
        self.dbjson: str = dbjson
        self.dir: str = dir
        self.songids: list[int] = songids

    def process_dbjson(self) -> None:
        self.df = self.dbjson_reader.read_json(self.dbjson, self.songids)

    def process_songjson(self):
        for songid in self.songids:
            self.df = self.songjson_reader.read_json(self.df, self.dir, songid)

    def generate_pdf(self):
        self.pdf_writer.generate_pdf(self.df)

    def save_pdf(self):
        self.pdf_writer.save_pdf(self.dir)

    def orchestrate(self):
        self.process_dbjson()
        self.process_songjson()
        self.generate_pdf()
        self.save_pdf()

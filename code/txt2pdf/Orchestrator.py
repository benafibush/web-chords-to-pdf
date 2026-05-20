from CSVReader import CSVReader
from TXTReader import TXTReader
from PDFWriter import PDFWriter


import pandas as pd


class Orchestrator:
    def __init__(self, csv: str, txt_dir: str):
        self.csv_reader   = CSVReader()
        self.txt_reader   = TXTReader()
        self.pdf_writer   = PDFWriter()
        self.df           = pd.DataFrame([])
        self.csv: str     = csv
        self.txt_dir: str = txt_dir

    def process_csv(self) -> None:
        self.df = self.csv_reader.read_csv(self.csv)

    def process_txt(self):
        self.df = self.txt_reader.read_txt(self.df, self.txt_dir)

    def generate_pdf(self):
        self.pdf_writer.generate_pdf(self.df)

    def save_pdf(self):
        self.pdf_writer.save_pdf(self.txt_dir)

    def orchestrate(self):
        self.process_csv()
        self.process_txt()
        self.generate_pdf()
        self.save_pdf()

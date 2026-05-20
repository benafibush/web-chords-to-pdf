import argparse

## this class extends argparse
class CommandParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        group = self.add_mutually_exclusive_group(required=True)
        group.add_argument("-url2txt", help="Browse URLs from CSV and produce text files at /path/to/output/dir/CSV_ID.txt")
        group.add_argument("-txt2pdf", help="Export all /path/to/input/dir/CSV_ID.txt to a single PDF with a table of contents")
        self. add_argument("-csv",     help="CSV file path", type=str, required=True)
        self. add_argument("-dir",     help="Directory for text files", type=str, required=True)
    
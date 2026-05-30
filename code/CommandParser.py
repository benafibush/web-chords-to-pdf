import argparse

## this class extends argparse
class CommandParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        group = self.add_mutually_exclusive_group(required=True)
        group.add_argument("-url2txt",     help="Browse URLs from JSON and produce text files at /path/to/output/dir/ID.txt",    action="store_true")
        group.add_argument("-chord_trnsp", help="Transpose chords in text files",                                                action="store_true")
        group.add_argument("-txt2pdf",     help="Export all /path/to/input/dir/ID.txt to a single PDF with a table of contents", action="store_true")
        self. add_argument("-json",        help="JSON file path",           type=str, required=True)
        self. add_argument("-dir",         help="Directory for text files", type=str, required=True)
    
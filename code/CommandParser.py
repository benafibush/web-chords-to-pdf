import argparse

## this class extends argparse
class CommandParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        group = self.add_mutually_exclusive_group(required=True)
        group.add_argument("-chord_trnsp",  help="Transpose chords in song json files",                                                  action="store_true")
        group.add_argument("-json2pdf",     help="Export specified /path/to/input/dir/ID.json to a single PDF with a table of contents", action="store_true")
        self. add_argument("-dbjson",       help="DB JSON file path",                   type=self.validate_dbjson, required=True)
        self. add_argument("-dir",          help="Directory for song JSON files",       type=self.validate_dir,    required=True)
        self. add_argument("-songids",      help="list of ID ranges (\"1-5,10\" e.g.)", type=self.parse_ranges,    required=False)

    def parse_ranges(self, s:str) -> list[int]:
        ids = set()
        for part in s.split(','):
            part = part.strip()
            if not part:
                continue
            if '-' in part:
                a, b = part.split('-', 1)
                try:
                    a, b = int(a), int(b)
                except ValueError:
                    raise argparse.ArgumentTypeError(f"invalid range: {part}")
                if a > b:
                    raise argparse.ArgumentTypeError(f"bad range: {part}")
                ids.update(range(a, b + 1))
            else:
                try:
                    ids.add(int(part))
                except ValueError:
                    raise argparse.ArgumentTypeError(f"invalid id: {part}")
        return sorted(ids)
    
    def validate_dbjson(self, dbjson: str) -> str:
        import os
        import json
        if not os.path.isfile(dbjson):
            raise argparse.ArgumentTypeError(f"DB JSON file '{dbjson}' does not exist.")
        try:
            with open(dbjson, 'r', encoding='utf-8') as f:
                json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise argparse.ArgumentTypeError(f"DB JSON file '{dbjson}' is not valid JSON: {e}")
        return dbjson
    
    def validate_dir(self, dir: str) -> str:
        import os
        if not os.path.isdir(dir):
            raise argparse.ArgumentTypeError(f"Directory '{dir}' does not exist.")
        return dir
    
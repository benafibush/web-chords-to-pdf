import pandas as pd
import json


class DBJSONReader:
    def read_json(self, json_path: str, songids: list[int]) -> pd.DataFrame:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        df = pd.DataFrame(json_data)
        df = df[df['id'].isin(songids)]
        return df
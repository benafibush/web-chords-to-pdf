import pandas as pd
import json


class SongJSONReader:
    def read_json(self, df: pd.DataFrame, dir: str, songid: int) -> pd.DataFrame:
        path = f"{dir}/{songid}.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                song_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading song JSON file '{path}': {e}")
            return df
        song_text=self.construct_text(song_data)
        df.loc[df['ID'] == songid, 'Text'] = song_text
        return df
    
    def construct_text(self, song_data: dict) -> str:
        text=""
        for part in song_data["structure"]:
            for line in song_data[part]:
                line = next(iter(line.values()))
                text+=line+"\n"
            text+="\n"
        return text
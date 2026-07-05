import pandas as pd
import json


class SongJSONReader:
    def read_json(self, df: pd.DataFrame, dir: str, songid: int) -> pd.DataFrame:
        path = f"{dir}/{songid:03d}.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                song_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Error reading song JSON file '{path}': {e}")
        song_text = self.construct_text(song_data)
        df.loc[df['ID'] == songid, 'Text'] = song_text
        return df
    
    def construct_text(self, song_data: dict) -> str:
        text=""
        for part in song_data["structure"]:
            text+=f"[{part}]\n"
            try:
                for line in song_data[part]:
                    line = next(iter(line.values()))
                    text+=line+"\n"
            except:
                raise ValueError(f"Error constructing text for part '{part}' in song data: {song_data}")
            text+="\n"
        return text
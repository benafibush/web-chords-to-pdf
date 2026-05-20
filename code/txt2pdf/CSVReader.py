import pandas as pd


class CSVReader:
    def read_csv(self, csv_data):
        # Implement CSV reading logic here
        # For demonstration purposes, assume a simple CSV parsing
        df = pd.DataFrame(csv_data)
        return df
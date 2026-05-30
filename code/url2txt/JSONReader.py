import pandas as pd
import os

class JSONReader:

    def read_json(self, json:str) -> pd.DataFrame:
        
        self.json: str = json
        self.verify_existance()

        self.df: pd.DataFrame = pd.read_json(self.json)
        self.verify_data()
        
        return self.df
    
    def verify_existance(self):
        if not os.path.exists(self.json):
            raise FileNotFoundError(f"The file '{self.json}' does not exist.")
    
    def verify_data(self):
        verification_data = {
            'Title'           : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Artist'          : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Link'            : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Order'           : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Browse Transpose': {'exists': True, 'non_empty': True, 'type_string': False, 'type_number': True , 'non_zero': False},
            'Capo Transpose'  : {'exists': True, 'non_empty': True, 'type_string': False, 'type_number': True , 'non_zero': False},
            'Singing Style'   : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Strumming Style' : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'Genre'           : {'exists': True, 'non_empty': True, 'type_string': True , 'type_number': False, 'non_zero': False},
            'ID'              : {'exists': True, 'non_empty': True, 'type_string': False, 'type_number': True , 'non_zero': True },
        }
        for column, rules in verification_data.items():
            if rules['exists']:
                self.verify_column_exists(column)
            if rules['non_empty']:
                self.verify_column_value_non_empty(column)
            if rules['type_string']:
                self.verify_column_type_string(column)
            if rules['type_number']:
                self.verify_column_type_number(column)
            if rules['non_zero']:
                self.verify_column_value_non_zero(column)

    def verify_column_exists(self, column: str) -> None:
        if not column in self.df.columns:
            raise ValueError(f"The JSON file '{self.json}' does not contain all the required columns.\nFirst missing column: {column}")
        
    def verify_column_value_non_empty(self, column: str) -> None:
        invalid_rows = self.df[~(self.df[column].notna())]
        if not invalid_rows.empty:
            raise ValueError(f"The column '{column}' in the JSON file '{self.json}' should contain values.\nFirst invalid row:\n{invalid_rows.iloc[0]}")

    def verify_column_type_string(self, column: str) -> None:
        invalid_rows = self.df[~(self.df[column].astype(str).str.len().astype(bool))]
        if not invalid_rows.empty:
            raise ValueError(f"The column '{column}' in the JSON file '{self.json}' should contain strings.\nFirst invalid row:\n{invalid_rows.iloc[0]}")
        
    def verify_column_type_number(self, column: str) -> None:
        invalid_rows = self.df[~self.df[column].astype(str).str.match(r"^-?\d*\.?\d+(,\s*-?\d*\.?\d+)*$")]
        if not invalid_rows.empty:
            raise ValueError(f"The column '{column}' in the JSON file '{self.json}' should contain numbers.\nFirst invalid row:\n{invalid_rows.iloc[0]}")
        
    def verify_column_value_non_zero(self, column: str) -> None:
        invalid_rows = self.df[~(self.df[column].astype(int) != 0)]
        if not invalid_rows.empty:
            raise ValueError(f"The column '{column}' in the JSON file '{self.json}' should contain non-zero values.\nFirst invalid row:\n{invalid_rows.iloc[0]}")
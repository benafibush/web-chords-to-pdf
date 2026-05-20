import unittest
import pandas
from InputFileReader import InputFileReader


class TestInputFileReader(unittest.TestCase):

    def setUp(self) -> None:
        self.ifr = InputFileReader()
        self.good_csv_path = "assets/good.csv"
        self.bad_csv_path = "assets/bad.csv"
        self.empty_csv_path = "assets/empty.csv"
        self.no_csv_path = "assets/no.csv"  # Make sure it doesn't exist

    def test_csv2dataframe(self) -> None:
        df = self.ifr.csv2dataframe(self.good_csv_path)
        self.assertIsInstance(df, pandas.DataFrame)

    def test_verify(self) -> None:
        df = self.ifr.csv2dataframe(self.good_csv_path)
        self.assertIsInstance(df, pandas.DataFrame)


if __name__ == '__main__':
    unittest.main()
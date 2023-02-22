import pandas as pd
import unittest
from src.utils import data_cleaner

class TestCorrectDFHeaders(unittest.TestCase):

    def test_correct_df_headers(self):
        # Test case 1: Test with a dataframe with correct headers
        df1 = pd.DataFrame({'srno': [1, 2], 'color': ['red', 'blue'], 'clarity': ['VS1', 'VVS2'], 'carat': [0.23, 0.54], 'price': [326, 352]})
        expected_df1 = pd.DataFrame({'srno': [1, 2], 'color': ['red', 'blue'], 'clarity': ['VS1', 'VVS2'], 'carat': [0.23, 0.54], 'price': [326, 352]})
        expected_row_idx1 = -1
        result_df1, result_row_idx1 = data_cleaner.correct_df_headers(df1)
        self.assertTrue(expected_df1.equals(result_df1))
        self.assertEqual(expected_row_idx1, result_row_idx1)

        # Test case 2: Test with a dataframe with incorrect headers
        df2 = pd.DataFrame({'Unnamed: 0': [1, 2], 'Djso': ['red', 'blue'], 'Unnamed: 1': ['VS1', 'VVS2'], 'unnamed: 2': [0.23, 0.54], 'unnamed: 3': [326, 352]})
        expected_df2 = pd.DataFrame({'srno': [1, 2], 'color': ['red', 'blue'], 'clarity': ['VS1', 'VVS2'], 'carat': [0.23, 0.54], 'price': [326, 352]})
        expected_row_idx2 = 0
        result_df2, result_row_idx2 = data_cleaner.correct_df_headers(df2)
        print(result_df2)
        self.assertTrue(expected_df2.equals(result_df2))
        self.assertEqual(expected_row_idx2, result_row_idx2)

        # Test case 3: Test with a dataframe with incorrect headers and no rows with correct headers
        df3 = pd.DataFrame({'Unnamed: 0': [1, 2], 'Djso': ['red', 'blue'], 'Unnamed: 1': ['VS1', 'VVS2'], 'unnamed: 2': [0.23, 0.54], 'unnamed: 3': [326, 352]})
        expected_df3 = pd.DataFrame({})
        expected_row_idx3 = -1
        result_df3, result_row_idx3 = data_cleaner.correct_df_headers(df3.iloc[0:3])
        print(result_df3)
        self.assertTrue(expected_df3.equals(result_df3))
        self.assertEqual(expected_row_idx3, result_row_idx3)

if __name__ == '__main__':
    unittest.main()

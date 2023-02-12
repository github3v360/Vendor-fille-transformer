from src.utils import data_cleaner
import unittest
import pandas as pd

class TestCorrectDFHeaders(unittest.TestCase):
  def test_correct_df_headers(self):

    # Test 1: Check if headers are already correct
    df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                      columns=['srno', 'color', 'cut', 'shape'])
    expected_output = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                                   columns=['srno', 'color', 'cut', 'shape'])
    corrected_df_headers = data_cleaner.correct_df_headers(df)
    self.assertTrue(corrected_df_headers.equals(expected_output))

    # Test 2: Check if headers are incorrect and needs to be corrected
    df = pd.DataFrame([[1, 2, 3, 4],['srno', 'color', 'cut', 'shape'], [5, 6, 7, 8], [9, 10, 11, 12]],
                      columns=['unnamed 0', 'Djso', 'unnamed 1', 'unnamed 2'])
    expected_output = pd.DataFrame([[5, 6, 7, 8], [9, 10, 11, 12]],
                                   columns=['srno', 'color', 'cut', 'shape'])

    corrected_df_headers = data_cleaner.correct_df_headers(df)
    corrected_df_headers = corrected_df_headers.reset_index(drop=True)

    self.assertTrue(all(corrected_df_headers == expected_output))
    
if __name__ == "__main__":
    unittest.main()
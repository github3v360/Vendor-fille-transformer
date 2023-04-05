import unittest
import pandas as pd
import logging
from src.single_sheet_extraction import ExtractFromSingleSheet

class TestExtractFromSingleSheet(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.date = None
        self.test_file_name = None
        self.work_sheet = None
        self.debug = None

    def test_process_with_empty_dataframe(self):
        # Test with empty input dataframe
        input_data = pd.DataFrame()
        expected_output = pd.DataFrame()
        extractor = ExtractFromSingleSheet(input_data, self.work_sheet, self.debug, self.logger, self.date, self.test_file_name)
        output_data = extractor.process()
        self.assertTrue(expected_output.equals(output_data))

    def test_process_with_cleaned_dataframe(self):
        # Test with cleaned input dataframe
        input_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c'], 'link': ['https://example.com', 'https://example.com', 'https://example.com']})
        expected_output = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c'], 'link': ['https://example.com', 'https://example.com', 'https://example.com'], 'probability': [0.5, 0.7, 0.9]})
        extractor = ExtractFromSingleSheet(input_data, self.work_sheet, self.debug, self.logger, self.date, self.test_file_name)
        output_data = extractor.process()
        self.assertFalse(expected_output.equals(output_data))

    def test_process_with_invalid_link(self):
        # Test with input dataframe containing invalid link
        input_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c'], 'link': ['invalid_link', 'https://example.com', 'https://example.com']})
        expected_output = pd.DataFrame({'col1': [2, 3], 'col2': ['b', 'c'], 'link': ['https://example.com', 'https://example.com'], 'probability': [0.7, 0.9]})
        extractor = ExtractFromSingleSheet(input_data, self.work_sheet, self.debug, self.logger, self.date, self.test_file_name)
        output_data = extractor.process()
        self.assertFalse(expected_output.equals(output_data))

if __name__ == '__main__':
    unittest.main()

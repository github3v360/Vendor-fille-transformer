import pandas as pd
import argparse
import os
from src.utils import common_utils
import unittest

class TestGetHighestProbColumn(unittest.TestCase):
    def test_get_highest_prob_column(self):
        self.assertEqual(common_utils.get_highest_prob_column([0.7, 0.6, 0.5], ["col1", "col2", "col3"]), ("col1",0.7))
        self.assertEqual(common_utils.get_highest_prob_column([0.6, 0.6, 0.6], ["col1", "col2", "col3"]), ("col1",0.6))
        self.assertEqual(common_utils.get_highest_prob_column([-1, 0.1, 0.2], ["col1", "col2", "col3"]), ("col3",0.2))

class TestAssureDataType(unittest.TestCase):
    def test_assure_data_type(self):
        self.assertEqual(common_utils.assure_data_type([0.7, 0.6, 0.5]),[0.7, 0.6, 0.5])
        self.assertEqual(common_utils.assure_data_type([0.7, "0.6", 0.5]),[0.7, 0.6, 0.5])
        self.assertEqual(common_utils.assure_data_type(["0.7", "0.6", "0.5"]),[0.7, 0.6, 0.5])
        self.assertEqual(common_utils.assure_data_type([0.7, None, 0.5]),[0.7, None, 0.5])
        self.assertEqual(common_utils.assure_data_type(["0.7", "None", 0.5]),[0.7, "None", 0.5])


class TestYourModule(unittest.TestCase):

    def test_read_yaml(self):
        data = common_utils.read_yaml('params.yaml')
        self.assertIsInstance(data, dict)

    def test_get_highest_prob_column(self):
        probs = [0.1, 0.5, 0.8, 0.3]
        cols = ['A', 'B', 'C', 'D']
        result = common_utils.get_highest_prob_column(probs, cols)
        self.assertEqual(result, ('C', 0.8))

        # Test case 1: Test with probabilities in descending order
        probs = [0.9, 0.8, 0.7, 0.6]
        cols = ['col1', 'col2', 'col3', 'col4']
        assert common_utils.get_highest_prob_column(probs, cols) == ('col1', 0.9)
        
        # Test case 2: Test with probabilities in ascending order
        probs = [0.6, 0.7, 0.8, 0.9]
        cols = ['col1', 'col2', 'col3', 'col4']
        assert common_utils.get_highest_prob_column(probs, cols) == ('col4', 0.9)
        
        # Test case 3: Test with equal probabilities
        probs = [0.8, 0.8, 0.8, 0.8]
        cols = ['col1', 'col2', 'col3', 'col4']
        assert common_utils.get_highest_prob_column(probs, cols) == ('col1', 0.8)
        
        # Test case 4: Test with only one column
        probs = [0.9]
        cols = ['col1']
        assert common_utils.get_highest_prob_column(probs, cols) == ('col1', 0.9)
        
        # Test case 5: Test with empty probabilities and columns
        probs = []
        cols = []
        assert common_utils.get_highest_prob_column(probs, cols) == (None, None)

    def test_assure_data_type(self):
        values = ['1', '2', '3.5', '4.7', None]
        result = common_utils.assure_data_type(values)
        expected = [1.0, 2.0, 3.5, 4.7, None]
        self.assertEqual(result, expected)

        # Test with integer input
        input_vals = [1, 2, 3]
        expected_output = [1, 2, 3]
        result = common_utils.assure_data_type(input_vals)
        self.assertEqual(result, expected_output)


        # Test with float input
        input_vals = [1.0, 2.0, 3.0]
        expected_output = [1.0, 2.0, 3.0]
        result = common_utils.assure_data_type(input_vals)
        self.assertEqual(result, expected_output)

        # Test with string input that can be converted to float
        input_vals = ["1.0", "2.0", "3.0"]
        expected_output = [1.0, 2.0, 3.0]
        result = common_utils.assure_data_type(input_vals)
        self.assertEqual(result, expected_output)

        # Test with string input that cannot be converted to float
        input_vals = ["1.0", "two", "3.0"]
        expected_output = [1.0, "two", 3.0]
        result = common_utils.assure_data_type(input_vals)
        self.assertEqual(result, expected_output)

        # Test with None input
        input_vals = [None, None, None]
        expected_output = [None, None, None]
        result = common_utils.assure_data_type(input_vals)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
import unittest
import logging
import pandas as pd
import argparse
import os
from src.utils import column_value_utils

class TestMyFunctions(unittest.TestCase):
  """
  This function will return the unique values of the target columns

  Args:
  target_name (str): The name of the target column

  returns:
  target_unique_values: List of unique values of the target columns
  """
  def setUp(self):
    self.logger = logging.getLogger()

  def test_get_target_column_unique_values(self):
    # Test for the clarity column
    unique_values = column_value_utils.get_target_column_unique_values("clarity", self.logger)
    self.assertIsInstance(unique_values, list)
    self.assertTrue(len(unique_values) > 0)

    # Test for the color column
    unique_values = column_value_utils.get_target_column_unique_values("color", self.logger)
    self.assertIsInstance(unique_values, list)
    self.assertTrue(len(unique_values) > 0)

    # Test for the cut column
    unique_values = column_value_utils.get_target_column_unique_values("cut", self.logger)
    self.assertIsInstance(unique_values, list)
    self.assertTrue(len(unique_values) > 0)

    # Test for a non-existent column
    with self.assertRaises(Exception):
        unique_values = column_value_utils.get_target_column_unique_values("non-existent-column", self.logger)

  def test_get_most_common_type(self):
    # Test for a list with one type only
    values = [1, 2, 3, 4]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, int)
    self.assertEqual(count, len(values))

    values = [1.0, 2.0, 3.0, 4.0]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, float)
    self.assertEqual(count, len(values))

    values = ['one', 'two', 'three']
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, str)
    self.assertEqual(count, len(values))

    # Test for a list with multiple types, but no clear winner
    values = [1, 2.0, 'three']
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertIsNotNone(most_common_type)
    self.assertEqual(count, 1)

    # Test for a list with multiple types and a clear winner
    values = [1, 2.0, 'three', 'four', 'five', 6.0, 7]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, str)
    self.assertEqual(count, 3)

    values = [1, 2.0, 3.0, 4.0, 'five', 6, 7]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, int)
    self.assertEqual(count, 3)

    values = [1, 2, 3, 4, 5, 6, 7]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, int)
    self.assertEqual(count, len(values))

    # Test for a list of integers
    values = [1, 2, 3, 4, 5]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, int)
    self.assertEqual(count, len(values))

    # Test for a list of floats and integers
    values = [1, 2, 3.0, 4.0, 5.0]
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, float)
    self.assertEqual(count, 3)

    # Test for a list of strings and integers
    values = [1, 2, 'three', 'four', 'five']
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertEqual(most_common_type, str)
    self.assertEqual(count, 3)

    # Test for an empty list
    values = []
    most_common_type, count = column_value_utils.get_most_common_type(values)
    self.assertIsNone(most_common_type)
    self.assertEqual(count, 0)

  def test_get_score_from_range(self):
        # Test for a list of integers
        rangeA, rangeB = 1, 10
        values = [1, 2, 3, 4, 5]
        n = len(values)
        result = column_value_utils.get_score_from_range(rangeA, rangeB, values, n)
        self.assertEqual(result, 1.0)

        # Test for a list of floats and integers
        rangeA, rangeB = 1, 10
        values = [1, 2, 3.0, 4.0, 5.0]
        n = len(values)
        result = column_value_utils.get_score_from_range(rangeA, rangeB, values, n)
        self.assertEqual(result, 1.0)

        # Test for a list of strings and integers
        rangeA, rangeB = 1, 10
        values = [1, 2, 'three', 'four', 'five']
        n = len(values)
        result = column_value_utils.get_score_from_range(rangeA, rangeB, values, n)
        self.assertEqual(result, 0.4)

        values = [1, 3, 5, 7, 9]
        rangeA = 2
        rangeB = 8
        n = 5
        self.assertEqual(column_value_utils.get_score_from_range(rangeA, rangeB, values, n), 0.6)

        values = [1.0, 2.5, 4.0, 6.5, 8.0]
        rangeA = 2
        rangeB = 6
        n = 5
        self.assertEqual(column_value_utils.get_score_from_range(rangeA, rangeB, values, n), 0.4)

        values = ['1', '2', '3', '4', '5']
        rangeA = 2
        rangeB = 4
        n = 5
        self.assertEqual(column_value_utils.get_score_from_range(rangeA, rangeB, values, n), 0.6)

        values = [None, 2, 4, None, 6, 8]
        rangeA = 3
        rangeB = 7
        n = 4
        self.assertEqual(column_value_utils.get_score_from_range(rangeA, rangeB, values, n), 0.5)

        values = [1, 2, 3, 4, 5]
        rangeA = 2.5
        rangeB = 3.5
        n = 5
        self.assertEqual(column_value_utils.get_score_from_range(rangeA, rangeB, values, n), 0.2)


  def test_convert_to_int(self):
        # Test for a list of integers and NaN values
        value = [1, 2, pd.NA, 4, 5]
        count_of_rows = len(value)
        new_list, count_of_rows = column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows)
        self.assertEqual(new_list, [1, 2, 4, 5])
        self.assertEqual(count_of_rows, 4)

        # Test for a list of floats and NaN values
        value = [1.0, 2.5, pd.NA, 4.2, 5.9]
        count_of_rows = len(value)
        new_list, count_of_rows = column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows)
        self.assertEqual(new_list, [1, 2, 4, 5])
        self.assertEqual(count_of_rows, 4)

        value = []
        count_of_rows = 0
        expected = ([], 0)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

        value = [1, 2.0, 3.1, 4.5]
        count_of_rows = 4
        expected = ([1, 2, 3, 4], 4)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

        value = [1, 2.0, None, 4.5]
        count_of_rows = 4
        expected = ([1, 2, 4], 3)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

        value = [None, None, None]
        count_of_rows = 3
        expected = ([], 0)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

        value = ['1', '2.0', '3.1', '4.5']
        count_of_rows = 4
        expected = (['1', '2.0', '3.1', '4.5'], 4)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

        value = ['1', '2.0', '3.1', '4.5', None]
        count_of_rows = 5
        expected = (['1', '2.0', '3.1', '4.5'], 4)
        self.assertEqual(column_value_utils.convert_to_int_and_update_rows_count(value, count_of_rows), expected)

  def test_cal_measurement_columns(self):
        # Test for string input data type with valid formula
        count_of_rows = 5
        column_unique_values = ['2x+3=7', '3x-1=8']
        taget_column_unique_values = []
        target_name = 'target_column_name'
        input_data_type = [str]
        n = len(column_unique_values)
        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, taget_column_unique_values, target_name, input_data_type, n)
        self.assertEqual(result, 0)

        # Test for string input data type with invalid formula
        count_of_rows = 5
        column_unique_values = ['2x+3=7', '3x-1=10x']
        taget_column_unique_values = []
        target_name = 'target_column_name'
        input_data_type = [str]
        n = len(column_unique_values)
        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, taget_column_unique_values, target_name, input_data_type, n)
        self.assertEqual(result, 0)

        # Test case for input_data_type = str, should return 1
        count_of_rows = 5
        column_unique_values = ["2x+1", "3x", "4x+5", "7x+1", "9x+6"]
        target_column_unique_values = []
        target_name = "column1"
        input_data_type = [str]
        n = len(column_unique_values)
        self.assertEqual(column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n), 1)

        # Test case for input_data_type = str, should return 0
        count_of_rows = 5
        column_unique_values = [None, "3x", "4x+5", "7x+1", "9x+6"]
        target_column_unique_values = []
        target_name = "column1"
        input_data_type = [str]
        n = len(column_unique_values)
        self.assertEqual(column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n), 0)

        # Test case for input_data_type = float, should return 0.8
        count_of_rows = 5
        column_unique_values = [1, 3, 5, 9, 12]
        target_column_unique_values = []
        target_name = "column1"
        input_data_type = [float]
        n = len(column_unique_values)
        self.assertEqual(column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n), 0.8)

        # Test case for input_data_type = float, should return 0.6
        count_of_rows = 5
        column_unique_values = [None, 3, 5, 9, 12]
        target_column_unique_values = []
        target_name = "column1"
        input_data_type = [float]
        n = len(column_unique_values)
        self.assertEqual(column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n), 0.6)

        # Test case for input_data_type = int, should return 0
        count_of_rows = 5
        column_unique_values = [1, 3, 5, 9, 12]
        target_column_unique_values = []
        target_name = "column1"
        input_data_type = [int]
        n = len(column_unique_values)
        self.assertEqual(column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n), 0)
        
        count_of_rows = 100
        column_unique_values = [1.5, 2.4, 3.1, 4.8, 5.0]
        target_column_unique_values = []
        target_name = ""
        input_data_type = [float]
        n = 100

        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n)
        assert result == 0.05, f"Expected 0.5, but got {result}"

        count_of_rows = 100
        column_unique_values = ["x + 2", "1 + x", "3 * x", "4", "5", "invalid"]
        target_column_unique_values = []
        target_name = ""
        input_data_type = [str]
        n = 100

        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n)
        assert result == 0, f"Expected 0, but got {result}"

        count_of_rows = 100
        column_unique_values = ["X + 2", "1 + X", "3 * X", "4", "5"]
        target_column_unique_values = []
        target_name = ""
        input_data_type = [str]
        n = 100

        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n)
        assert result == 0, f"Expected 1, but got {result}"

        count_of_rows = 100
        column_unique_values = ["x + 2", "1 + x", "3 * x", "4", "5"]
        target_column_unique_values = []
        target_name = ""
        input_data_type = [str]
        n = 100

        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n)
        assert result == 0, f"Expected 1, but got {result}"


        count_of_rows = 100
        column_unique_values = [1, 2, 3, 4, 5]
        target_column_unique_values = []
        target_name = ""
        input_data_type = [str]
        n = 100

        result = column_value_utils.cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_values, target_name, input_data_type, n)
        assert result == 0, f"Expected 0, but got {result}"



if __name__ == "__main__":
    unittest.main()
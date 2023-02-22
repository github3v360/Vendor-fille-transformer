import pandas as pd
import argparse
import os
from src.utils import post_processing_utils, common_utils
import unittest

class TestTransformShapeColumn(unittest.TestCase):
  def test_transform_shape_column(self):
    
    magic_numbers = common_utils.read_yaml("params.yaml")['magic_numbers']

    # Test with a shape that exists in the shape dictionary
    result = post_processing_utils.transform_shape_column("RND",magic_numbers)
    self.assertEqual(result, "Round")
    
    # Test with a shape that is close to a shape in the shape dictionary df['disc'] = df['disc'].astype(float)
    result = post_processing_utils.transform_shape_column("ROUD",magic_numbers)
    self.assertEqual(result, "Round")
    
    # Test with a shape that is not similar to any shape in the shape dictionary
    result = post_processing_utils.transform_shape_column("orange",magic_numbers)
    self.assertIsNone(result)
    
    # Test with a shape that is an exact match to a shape in the shape dictionary
    result = post_processing_utils.transform_shape_column("OVAL",magic_numbers)
    self.assertEqual(result, "Oval")
    
    # Test with a shape that is not in the shape dictionary but has a high similarity score
    result = post_processing_utils.transform_shape_column("OVEL",magic_numbers)
    self.assertEqual(result, "Oval")
    
    # Test with a shape that is not in the shape dictionary and has a low similarity score
    result = post_processing_utils.transform_shape_column("V",magic_numbers)
    self.assertIsNone(result)
    
    # Test with an empty string
    result = post_processing_utils.transform_shape_column("",magic_numbers)
    self.assertIsNone(result)
    
    # Test with None
    result = post_processing_utils.transform_shape_column(None,magic_numbers)
    self.assertIsNone(result)

class TestTransformfluorColumn(unittest.TestCase):
  def test_transform_fluor_column(self):

    magic_numbers = common_utils.read_yaml("params.yaml")['magic_numbers']

    # Test with a fluorescent that exists in the fluor dictionary
    result = post_processing_utils.transform_fluor_column("faint",magic_numbers)
    self.assertEqual(result, "FAINT")

    # Test with a fluorescent that exists in the fluor dictionary
    result = post_processing_utils.transform_fluor_column("f",magic_numbers)
    self.assertEqual(result, "FAINT")

    # Test with a fluorescent that exists in the fluor dictionary
    result = post_processing_utils.transform_fluor_column("non",magic_numbers)
    self.assertEqual(result, "NONE")

    # Test with a fluorescent that don't exists in the fluor dictionary
    result = post_processing_utils.transform_fluor_column("med-w",magic_numbers)
    self.assertEqual(result, "MEDIUM")

    # Test with a fluorescent that exists in the fluor dictionary
    result = post_processing_utils.transform_fluor_column("",magic_numbers)
    self.assertEqual(result, None)

    result = post_processing_utils.transform_fluor_column(None,magic_numbers)
    self.assertEqual(result, None)
    
class TestTransformMeasurementColumn(unittest.TestCase):

    def test_string_measurement(self):
        # Test a string measurement in the format "2 * 3 * 4"
        cur_val_l = "2 * 3 * 4"
        cur_val_d = 1.0
        expected_output = [4.0, 3.0, 2.0]
        self.assertEqual(post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d), expected_output)

    def test_list_measurement(self):
        # Test a list measurement in the format [4*1]
        cur_val_l = "4*1"
        cur_val_d = 2.0
        expected_output = [4.0, 1.0, 2.0]
        self.assertEqual(post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d), expected_output)

    def test_missing_value(self):
        # Test a missing measurement value
        cur_val_l = ""
        cur_val_d = 1.0
        expected_output = [None, None, None]
        self.assertEqual(post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d), expected_output)

    def test_invalid_value(self):
        # Test an invalid measurement value
        cur_val_l = "foo"
        cur_val_d = 1.0
        expected_output = [None, None, None]
        self.assertEqual(post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d), expected_output)

    def test_transform_measurement_column(self):
        # test case 1
        cur_val_l = "2*3*4"
        cur_val_d = 5.0
        expected_output = [4.0, 3.0, 2.0]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 1 failed: expected {expected_output}, but got {result}"
        
        # test case 2
        cur_val_l = "5*10*15"
        cur_val_d = 10.0
        expected_output = [15.0, 10.0, 5.0]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 2 failed: expected {expected_output}, but got {result}"
        
        # test case 3
        cur_val_l = ""
        cur_val_d = 5.0
        expected_output = [None, None, None]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 3 failed: expected {expected_output}, but got {result}"
        
        # test case 4
        cur_val_l = None
        cur_val_d = 5.0
        expected_output = [None, None, None]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 4 failed: expected {expected_output}, but got {result}"
        
        # test case 5
        cur_val_l = "5"
        cur_val_d = 5.0
        expected_output = [None, None, None]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 5 failed: expected {expected_output}, but got {result}"
        
        # test case 6
        cur_val_l = "3.5*2.5*2"
        cur_val_d = 5.0
        expected_output = [3.5, 2.5, 2.0]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 6 failed: expected {expected_output}, but got {result}"
        
        # test case 7
        cur_val_l = "4*1"
        cur_val_d = 3.0
        expected_output = [4.0, 1.0, 3.0]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 7 failed: expected {expected_output}, but got {result}"
        
        # test case 8
        cur_val_l = "10*20"
        cur_val_d = 30.0
        expected_output = [20.0, 10.0, 30.0]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 8 failed: expected {expected_output}, but got {result}"
        
        # test case 9
        cur_val_l = "3*5*"
        cur_val_d = 2.0
        expected_output = [None, None, None]
        result = post_processing_utils.transform_measurement_column(cur_val_l, cur_val_d)
        assert result == expected_output, f"Test case 9 failed: expected {expected_output}, but got {result}"

class TestTransformCutColumn(unittest.TestCase):

    def test_transform_cut_column(self):
        # Test standard shapes
        assert post_processing_utils.transform_cut_column("I", {"cut_similarity_transform_df_threshold": 0.5}) == "I"
        assert post_processing_utils.transform_cut_column("EX", {"cut_similarity_transform_df_threshold": 0.5}) == "EX"
        assert post_processing_utils.transform_cut_column("VG", {"cut_similarity_transform_df_threshold": 0.5}) == "VG"
        assert post_processing_utils.transform_cut_column("G", {"cut_similarity_transform_df_threshold": 0.5}) == "G"
        assert post_processing_utils.transform_cut_column("F", {"cut_similarity_transform_df_threshold": 0.5}) == "F"
        assert post_processing_utils.transform_cut_column("P", {"cut_similarity_transform_df_threshold": 0.5}) == "P"
        assert post_processing_utils.transform_cut_column("EX+", {"cut_similarity_transform_df_threshold": 0.5}) == "EX"

        # Test non-standard shapes with exact match
        assert post_processing_utils.transform_cut_column("Round", {"cut_similarity_transform_df_threshold": 0.5}) == None
        assert post_processing_utils.transform_cut_column("Princess", {"cut_similarity_transform_df_threshold": 0.5}) == None
        assert post_processing_utils.transform_cut_column("Emerald", {"cut_similarity_transform_df_threshold": 0.5}) == None

        # Test non-standard shapes with fuzzy matching
        assert post_processing_utils.transform_cut_column("RND", {"cut_similarity_transform_df_threshold": 0.5}) == None
        assert post_processing_utils.transform_cut_column("PRNC", {"cut_similarity_transform_df_threshold": 0.5}) == None
        assert post_processing_utils.transform_cut_column("EMRLD", {"cut_similarity_transform_df_threshold": 0.5}) == None
        
        # Test empty input
        assert post_processing_utils.transform_cut_column("", {"cut_similarity_transform_df_threshold": 0.5}) == None
        assert post_processing_utils.transform_cut_column(None, {"cut_similarity_transform_df_threshold": 0.5}) == None

class TestTransformDiscountColumn(unittest.TestCase):
    def test_transform_discount_column(self):
        assert post_processing_utils.transform_discount_column("10") == 10.0
        assert post_processing_utils.transform_discount_column("-10") == 10.0
        assert post_processing_utils.transform_discount_column("0") == 0.0
        assert post_processing_utils.transform_discount_column("") == 0.0
        assert post_processing_utils.transform_discount_column(None) == 0.0

class TestTransformReportNoColumn(unittest.TestCase):
    def test_transform_report_no_column(self):
        # Test Case 1 - report_no and report_no_from_link are equal
        assert post_processing_utils.transform_report_no_column("45862177986", "45862177986") == "45862177986"

        # Test Case 2 - report_no is not None and report_no_from_link is None
        assert post_processing_utils.transform_report_no_column("52364789152", None) == "52364789152"

        # Test Case 3 - report_no is None and report_no_from_link is not None
        assert post_processing_utils.transform_report_no_column(None, "4851297767") == "4851297767"

        # Test Case 4 - report_no and report_no_from_link are not equal, but report_no is not None
        assert post_processing_utils.transform_report_no_column("4851269742", "5673832784") == "4851269742"

        # Test Case 5 - report_no and report_no_from_link are not equal, and report_no is None
        assert post_processing_utils.transform_report_no_column(None, "5673832784") == "5673832784"

        # Test Case 6 - report_no and report_no_from_link are both None
        assert post_processing_utils.transform_report_no_column(None, None) == None

if __name__ == "__main__":
    unittest.main()
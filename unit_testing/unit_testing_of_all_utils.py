import pandas as pd
import argparse
import os
from src.utils.all_utils import *
import unittest

class TestStringSimilarity(unittest.TestCase):
    def test_string_similarity(self):
        self.assertAlmostEqual(string_similarity("Hello", "Hello"), 1.0)
        self.assertAlmostEqual(string_similarity("Hello", "heLLo"), 1.0)
        self.assertGreaterEqual(string_similarity("Hello", "Helo"), 0.6)
        self.assertGreaterEqual(string_similarity("Hello", "Hullo"), 0.6)
        self.assertEqual(string_similarity("Hello", "Bye"), 0.0)
        self.assertEqual(string_similarity(1, "1"), 1.0)
        self.assertEqual(string_similarity(1, "Bye"), 0.0)
        self.assertEqual(string_similarity(1.23, "1.23"), 1.0)
        self.assertGreaterEqual(string_similarity(1.2, "1.23"), 0.6)


class TestGetHighestProbColumn(unittest.TestCase):
    def test_get_highest_prob_column(self):
        self.assertEqual(get_highest_prob_column([0.7, 0.6, 0.5], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(get_highest_prob_column([0.5, 0.6, 0.7], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(get_highest_prob_column([0.6, 0.6, 0.6], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(get_highest_prob_column([0.6, 0.7, 0.6], ["col1", "col2", "col3"]), "col2")
        self.assertEqual(get_highest_prob_column([0.6, 0.6, 0.7], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(get_highest_prob_column([2.6, 0.1, 0.2], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(get_highest_prob_column([-1, 0.1, 0.2], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(get_highest_prob_column([0, 0.8, 0.5], ["col1", "col2", "col3"]), "col2")
        self.assertEqual(get_highest_prob_column([1.6, -1, -1], ["col1", "col2", "col3"]), "col1")

class TestSimilarityScoreFromColName(unittest.TestCase):
    def test_similarity_score_from_col_name(self):
        self.assertEqual(similarity_score_from_col_name("column1", ["column1", "column2", "column3"]), 1.0)
        self.assertLessEqual(similarity_score_from_col_name("shape", ["color", "carat","clarity"]), 0.2)
        self.assertGreaterEqual(similarity_score_from_col_name("col1", ["column1", "column2", "column3"]), 0.5)
        self.assertEqual(similarity_score_from_col_name("Shape", ["Shape", "tape"]), 1.0)
        self.assertGreaterEqual(similarity_score_from_col_name("column1", ["col1", "col2", "col3"]), 0.5)
        self.assertGreaterEqual(similarity_score_from_col_name("carat", ["Ct.", "shape", "color"]), 0.15)
        self.assertGreaterEqual(similarity_score_from_col_name("carat", ["weight", "clor", "cot"]), 0.3)
        self.assertGreaterEqual(similarity_score_from_col_name("color", ["colour", "cl.", "co"]), 0.5)
        self.assertGreaterEqual(similarity_score_from_col_name("shape", ["shap", "sh.", "carat"]), 0.4)

class TestGetMostCommonType(unittest.TestCase):
    def test_get_most_common_type(self):
        self.assertEqual(get_most_common_type([1, 2, 3, 4, 5]), (int, 5))
        self.assertEqual(get_most_common_type([1.0, 2.0, 3.0, 4.0, 5.0]), (float, 5))
        self.assertEqual(get_most_common_type(["a", "b", "c", "d", "e"]), (str, 5))
        self.assertEqual(get_most_common_type([1, 2.0, 3, 4.0, 5]), (int, 3))
        self.assertEqual(get_most_common_type([1.0, 2, 3.0, 4, 5.0]), (float, 3))
        self.assertEqual(get_most_common_type(["a", "b", 1, 2, 3]), (int, 3))
        self.assertEqual(get_most_common_type([1.0, 2.0, "a", "b", 3.0]), (float, 3))
        self.assertEqual(get_most_common_type(["a", "b", 1.0, "2", 3.0]), (str, 3))
        self.assertEqual(get_most_common_type([None,None,"a","b",1]), (str, 2))

class TestSimilarityScoreFromColValues(unittest.TestCase):
    def test_similarity_score_from_col_values(self):
        # The whole test is takes assumption that we have correct target values

        # The logic for traget data type with string is different where 1 indicates that most of the value matches 
        # while 0 imdicated no value matches
        self.assertEqual(similarity_score_from_col_values(["a", "b", "c", "d", "e"], ["a", "b", "c", "d", "e"],"target_column_with_str_values"), 1)
        self.assertEqual(similarity_score_from_col_values(["a", "b", "c", "d", "e"], ["f", "g", "h", "i", "j"],"target_column_with_str_values"), 0)
        self.assertEqual(similarity_score_from_col_values([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"],"target_column_with_str_values"), 1)

        # If the target data type is float or int but the input data type is str
        self.assertEqual(similarity_score_from_col_values(["1", "2", "3", "4", "5"],[1, 2, 3, 4, 5],"column_with_int_values"), 0)
        self.assertEqual(similarity_score_from_col_values(["1", "2", "3", "4", "5"],[1.1, 2.2, 3.3, 4.4, 5],"column_with_float_values"), 0)

        # If target column is carat 
        # In carat value range should be greater than 1 and less than 20
        self.assertEqual(similarity_score_from_col_values([1.1,2.1,6.8,3.1,4.2],[1.1, 2.2, 3.3, 4.4, 5],"carat"), 1)
        self.assertEqual(similarity_score_from_col_values([1.1,2.1,6.8,30,40],[1.1, 2.2, 3.3, 4.4, 5],"carat"), 0.6)

        # If target column is raprate 
        # In carat raprate range should be greater than 1000 and less than 20000
        self.assertEqual(similarity_score_from_col_values([1000.1,2000,3000,4000,5000],[2000.1,2000,3000,4000,5000],"raprate"), 0.8)
        self.assertEqual(similarity_score_from_col_values([1.1,2.4,4.2,2000.8,2.1],[2000.1,2000,3000,4000,5000],"raprate"), 0.2)

class TestGetStandardNames(unittest.TestCase):
    def test_clarity(self):
        std_names = get_standard_names("clarity")
        self.assertEqual(std_names, ["clarity", "purity"])
    
    def test_color(self):
        std_names = get_standard_names("color")
        self.assertEqual(std_names, ["color", "colour"])
        
    def test_shape(self):
        std_names = get_standard_names("shape")
        self.assertEqual(std_names, ["shape"])
        
    def test_carat(self):
        std_names = get_standard_names("carat")
        self.assertEqual(std_names, ["carat", "size", "cts", "crtwt"])
        
    def test_invalid_name(self):
        with self.assertRaises(Exception):
            get_standard_names("invalid_name")

class TestGetTargetColumnUniqueValues(unittest.TestCase):
    def test_get_target_column_unique_values(self):
        # Test for target column "clarity"
        clarity_unique_values = get_target_column_unique_values("clarity")
        self.assertEqual(len(clarity_unique_values), 12)
        self.assertIn("si1 +", clarity_unique_values)
        self.assertIn("vs1 -", clarity_unique_values)
        
        # Test for target column "carat"
        carat_unique_values = get_target_column_unique_values("carat")
        self.assertEqual(len(carat_unique_values), 5)
        self.assertEqual(float, type(carat_unique_values[0]))
        self.assertEqual(float, type(carat_unique_values[2]))
        
        # Test for target column "color"
        color_unique_values = get_target_column_unique_values("color")
        self.assertEqual(len(color_unique_values), 17)
        self.assertIn("d", color_unique_values)
        self.assertIn("g", color_unique_values)
        
        # Test for target column "shape"
        shape_unique_values = get_target_column_unique_values("shape")
        self.assertEqual(len(shape_unique_values), 148)
        self.assertIn("trapezoid", shape_unique_values)
        self.assertIn("heart", shape_unique_values)
        
        # Test for invalid target column
        with self.assertRaises(Exception):
            get_target_column_unique_values("invalid")

class TestModifySimScoreOfName(unittest.TestCase):
    def test_modify_sim_score_of_name(self):
        # Test for target name "clarity"
        target_name = "clarity"
        sim_score = 0.6
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 2,
            "carat_enhancing_factor": 1.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 0.3
        expected_need_to_continue = True
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertEqual(result, (expected_sim_score, expected_need_to_continue))

        # Test for target name "clarity" with sim_score above threshold
        target_name = "clarity"
        sim_score = 0.8
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 0.5,
            "carat_enhancing_factor": 1.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 0.8
        expected_need_to_continue = False
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertAlmostEqual(result, (expected_sim_score, expected_need_to_continue))

        # Test for target name "carat" with sim_score above threshold
        target_name = "carat"
        sim_score = 0.8
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 0.5,
            "carat_enhancing_factor": 0.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 0.4
        expected_need_to_continue = True
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertEqual(result, (expected_sim_score, expected_need_to_continue))

    def test_modify_sim_score_of_name(self):
        # Test for target name "color"
        target_name = "color"
        sim_score = 0.6
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 2,
            "carat_enhancing_factor": 1.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 1.2
        expected_need_to_continue = True
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertEqual(result, (expected_sim_score, expected_need_to_continue))

        # Test for target name "color" with sim_score above threshold
        target_name = "color"
        sim_score = 0.9
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 2,
            "carat_enhancing_factor": 1.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 0.9
        expected_need_to_continue = False
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertAlmostEqual(result, (expected_sim_score, expected_need_to_continue))

        # Test for target name "shape" 
        target_name = "shape"
        sim_score = 0.45
        magic_numbers = {
            "clarity_threshold": 0.7,
            "clarity_normalizing_factor": 2,
            "carat_enhancing_factor": 1.5,
            "color_threshold": 0.8,
            "color_normalizing_factor": 0.5,
        }
        expected_sim_score = 0.45
        expected_need_to_continue = True
        result = modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertAlmostEqual(result, (expected_sim_score, expected_need_to_continue))

        # Test for invalid target column
        with self.assertRaises(Exception):
            modify_sim_score_of_name("invalid")


class TestTransformShapeColumn(unittest.TestCase):
  def test_transform_shape_column(self):
    # Test with a shape that exists in the shape dictionary
    result = transform_shape_column("RND")
    self.assertEqual(result, "Round")
    
    # Test with a shape that is close to a shape in the shape dictionary
    result = transform_shape_column("ROUD")
    self.assertEqual(result, "Round")
    
    # Test with a shape that is not similar to any shape in the shape dictionary
    result = transform_shape_column("orange")
    self.assertIsNone(result)
    
    # Test with a shape that is an exact match to a shape in the shape dictionary
    result = transform_shape_column("OVAL")
    self.assertEqual(result, "Oval")
    
    # Test with a shape that is not in the shape dictionary but has a high similarity score
    result = transform_shape_column("OVEL")
    self.assertEqual(result, "Oval")
    
    # Test with a shape that is not in the shape dictionary and has a low similarity score
    result = transform_shape_column("V")
    self.assertIsNone(result)
    
    # Test with an empty string
    result = transform_shape_column("")
    self.assertIsNone(result)
    
    # Test with None
    result = transform_shape_column(None)
    self.assertIsNone(result)

class TestCorrectDFHeaders(unittest.TestCase):
  def test_correct_df_headers(self):

    # Test 1: Check if headers are already correct
    df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                      columns=['srno', 'color', 'cut', 'shape'])
    expected_output = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                                   columns=['srno', 'color', 'cut', 'shape'])
    corrected_df_headers = correct_df_headers(df)
    self.assertTrue(corrected_df_headers.equals(expected_output))

    # Test 2: Check if headers are incorrect and needs to be corrected
    df = pd.DataFrame([[1, 2, 3, 4],['srno', 'color', 'cut', 'shape'], [5, 6, 7, 8], [9, 10, 11, 12]],
                      columns=['unnamed 0', 'Djso', 'unnamed 1', 'unnamed 2'])
    expected_output = pd.DataFrame([[5, 6, 7, 8], [9, 10, 11, 12]],
                                   columns=['srno', 'color', 'cut', 'shape'])

    corrected_df_headers = correct_df_headers(df)
    corrected_df_headers = corrected_df_headers.reset_index(drop=True)

    self.assertTrue(all(corrected_df_headers == expected_output))
    
if __name__ == "__main__":
    unittest.main()
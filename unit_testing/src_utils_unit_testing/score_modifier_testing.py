import pandas as pd
import argparse
import os
from src.utils import score_modifier
import unittest

# class TestModifySimScoreOfName(unittest.TestCase):
    # def test_modify_sim_score_of_name(self):
    #     magic_numbers = {
    #             "clarity_normalizing_factor_for_col_name": 0.5,
    # "clarity_normalizing_factor_for_col_value": 0.5,

    # "carat_normalizing_factor_for_col_name": 0.65,
    # "carat_normalizing_factor_for_col_value": 0.35,

    # "color_normalizing_factor_for_col_name": 0.5,
    # "color_normalizing_factor_for_col_value": 0.5,

    # "shape_similarity_transform_df_threshold": 0.7,
    
    # "fluor_normalizing_factor_for_col_name": 0.5,
    # "fluor_normalizing_factor_for_col_value": 0.5,
    # "fluor_similarity_transform_df_threshold": 0.3,

    # "raprate_normalizing_factor_for_col_name": 0.5,
    # "raprate_normalizing_factor_for_col_value": 0.5,

    # "measurement_normalizing_factor_for_col_name": 0.4,
    # "measurement_normalizing_factor_for_col_value": 0.6,
    
    # "cut_normalizing_factor_for_col_name": 0.5,
    # "cut_normalizing_factor_for_col_value": 0.5,
    # "cut_similarity_transform_df_threshold": 0.7,

    # "polish_normalizing_factor_for_col_name": 0.5,
    # "polish_normalizing_factor_for_col_value": 0.5,

    # "sym_normalizing_factor_for_col_name": 0.5,
    # "sym_normalizing_factor_for_col_value": 0.5,
    
    # "table_normalizing_factor_for_col_name": 0.5,
    # "table_normalizing_factor_for_col_value": 0.5,

    # "comments_normalizing_factor_for_col_name": 0.8,
    # "comments_normalizing_factor_for_col_value": 0.2,

    # "ppc_normalizing_factor_for_col_name": 0.5,
    # "ppc_normalizing_factor_for_col_value": 0.5,

    # "disc_normalizing_factor_for_col_name": 0.6,
    # "disc_normalizing_factor_for_col_value": 0.4,

    # "amt_normalizing_factor_for_col_name": 0.5,
    # "amt_normalizing_factor_for_col_value": 0.5,

    # "raptotal_normalizing_factor_for_col_name": 0.5,
    # "raptotal_normalizing_factor_for_col_value": 0.5,

    # "stockref_normalizing_factor_for_col_name": 0.5,
    # "stockref_normalizing_factor_for_col_value": 0.5,

    # "report_normalizing_factor_for_col_name": 0.5,
    # "report_normalizing_factor_for_col_value": 0.5

    #     }
    #     result = score_modifier.modify_sim_score_of_name(0.9, 'clarity', magic_numbers)
    #     self.assertEqual(result,0.45)
    #     result = score_modifier.modify_sim_score_of_name(0.8, 'carat', magic_numbers) 
    #     self.assertEqual(result,0.52)
    #     result = score_modifier.modify_sim_score_of_name(0.95, 'polish', magic_numbers)
    #     self.assertEqual(result,0.475)
    #     result = score_modifier.modify_sim_score_of_name(1.1, 'symmetry', magic_numbers)
    #     self.assertEqual(result,0.55)
    #     result = score_modifier.modify_sim_score_of_name(1.05, 'table', magic_numbers)
    #     self.assertEqual(result,0.525)
    #     result = score_modifier.modify_sim_score_of_name(1.2, 'comments', magic_numbers)
    #     self.assertEqual(result,0.96)
    #     result = score_modifier.modify_sim_score_of_name(1.15, 'price per carat', magic_numbers)
    #     self.assertEqual(result,0.575)
    #     result = score_modifier.modify_sim_score_of_name(0.75, 'discount', magic_numbers)
    #     self.assertEqual(result,0.45)
    #     result = score_modifier.modify_sim_score_of_name(1.1, 'total', magic_numbers)
    #     self.assertEqual(result,0.55)
    #     result = score_modifier.modify_sim_score_of_name(0.95, 'rap price total', magic_numbers)
    #     self.assertEqual(result,0.475)
    #     result = score_modifier.modify_sim_score_of_name(1.1, 'Stock Ref', magic_numbers) 
    #     self.assertEqual(result,0.55)
    #     result = score_modifier.modify_sim_score_of_name(0.9, 'report_no', magic_numbers)
    #     self.assertEqual(result,0.45)

    #     # assert modify_sim_score_of_name(1.0, 'Cert', magic_numbers) == 1.0
    #     try:
    #         score_modifier.modify_sim_score_of_name(1.0, 'invalid_name', magic_numbers)
    #         assert False, "Expected an exception to be raised"
    #     except Exception as e:
    #         assert str(e) == "The function could not find this target name"

class TestMergeSimilarityScore(unittest.TestCase):

    def setUp(self):
        self.magic_numbers = {
            "clarity_normalizing_factor_for_col_name": 0.5,
            "clarity_normalizing_factor_for_col_value": 0.5,

            "carat_normalizing_factor_for_col_name": 0.65,
            "carat_normalizing_factor_for_col_value": 0.35,

            "color_normalizing_factor_for_col_name": 0.5,
            "color_normalizing_factor_for_col_value": 0.5,

            "shape_normalizing_factor_for_col_name": 0.5,
            "shape_normalizing_factor_for_col_value": 0.5,

            "shape_similarity_transform_df_threshold": 0.7,
            
            "fluor_normalizing_factor_for_col_name": 0.5,
            "fluor_normalizing_factor_for_col_value": 0.5,
            "fluor_similarity_transform_df_threshold": 0.3,

            "raprate_normalizing_factor_for_col_name": 0.5,
            "raprate_normalizing_factor_for_col_value": 0.5,

            "measurement_normalizing_factor_for_col_name": 0.4,
            "measurement_normalizing_factor_for_col_value": 0.6,
            
            "cut_normalizing_factor_for_col_name": 0.5,
            "cut_normalizing_factor_for_col_value": 0.5,
            "cut_similarity_transform_df_threshold": 0.7,

            "polish_normalizing_factor_for_col_name": 0.5,
            "polish_normalizing_factor_for_col_value": 0.5,

            "sym_normalizing_factor_for_col_name": 0.5,
            "sym_normalizing_factor_for_col_value": 0.5,
            
            "table_normalizing_factor_for_col_name": 0.5,
            "table_normalizing_factor_for_col_value": 0.5,

            "comments_normalizing_factor_for_col_name": 0.8,
            "comments_normalizing_factor_for_col_value": 0.2,

            "ppc_normalizing_factor_for_col_name": 0.5,
            "ppc_normalizing_factor_for_col_value": 0.5,

            "disc_normalizing_factor_for_col_name": 0.6,
            "disc_normalizing_factor_for_col_value": 0.4,

            "amt_normalizing_factor_for_col_name": 0.5,
            "amt_normalizing_factor_for_col_value": 0.5,

            "raptotal_normalizing_factor_for_col_name": 0.5,
            "raptotal_normalizing_factor_for_col_value": 0.5,

            "stockref_normalizing_factor_for_col_name": 0.5,
            "stockref_normalizing_factor_for_col_value": 0.5,

            "report_normalizing_factor_for_col_name": 0.5,
            "report_normalizing_factor_for_col_value": 0.5
        }

    def test_clarity_similarity_score(self):
        # Test for Clarity column
        sim_score_name = 0.5
        sim_score_val = 0.5
        target_name = 'clarity'
        expected_result = 0.5
        actual_result = score_modifier.merge_similarity_score(sim_score_name, sim_score_val, target_name, self.magic_numbers)
        self.assertEqual(expected_result, actual_result)

    def test_carat_similarity_score(self):
        # Test for Carat column
        sim_score_name = 0.65
        sim_score_val = 0.35
        target_name = 'carat'
        expected_result = 0.545
        actual_result = score_modifier.merge_similarity_score(sim_score_name, sim_score_val, target_name, self.magic_numbers)
        self.assertEqual(expected_result, actual_result)

    def test_color_similarity_score(self):
        # Test for Color column
        sim_score_name = 0.5
        sim_score_val = 0.5
        target_name = 'color'
        expected_result = 0.5
        actual_result = score_modifier.merge_similarity_score(sim_score_name, sim_score_val, target_name, self.magic_numbers)
        self.assertEqual(expected_result, actual_result)

    def test_fluor_similarity_score(self):
        # Test for Shape column
        sim_score_name = 0.5
        sim_score_val = 0.5
        target_name = 'fluorescent'
        expected_result = 0.5
        actual_result = score_modifier.merge_similarity_score(sim_score_name, sim_score_val, target_name, self.magic_numbers)
        self.assertEqual(expected_result, actual_result)

    def test_raprate_similarity_score(self):
        # Test for Shape column
        sim_score_name = 0.5
        sim_score_val = 0.5
        target_name = "raprate"
        expected_result = 0.5
        actual_result = score_modifier.merge_similarity_score(sim_score_name, sim_score_val, target_name, self.magic_numbers)
        self.assertEqual(expected_result, actual_result)

    # add more tests for the remaining columns

if __name__ == "__main__":
    unittest.main()
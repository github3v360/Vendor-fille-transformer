import pandas as pd
import argparse
import os
from src.utils import score_modifier
import unittest

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
        result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
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
        result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
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
        result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
        self.assertEqual(result, (expected_sim_score, expected_need_to_continue))

    # deftest_modify_sim_score_of_name(self):
    #     # Test for target name "color"
    #     target_name = "color"
    #     sim_score = 0.6
    #     magic_numbers = {
    #         "clarity_threshold": 0.7,
    #         "clarity_normalizing_factor": 2,
    #         "carat_enhancing_factor": 1.5,
    #         "color_threshold": 0.8,
    #         "color_normalizing_factor": 0.5,
    #     }
    #     expected_sim_score = 1.2
    #     expected_need_to_continue = True
    #     result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
    #     self.assertEqual(result, (expected_sim_score, expected_need_to_continue))

    #     # Test for target name "color" with sim_score above threshold
    #     target_name = "color"
    #     sim_score = 0.9
    #     magic_numbers = {
    #         "clarity_threshold": 0.7,
    #         "clarity_normalizing_factor": 2,
    #         "carat_enhancing_factor": 1.5,
    #         "color_threshold": 0.8,
    #         "color_normalizing_factor": 0.5,
    #     }
    #     expected_sim_score = 0.9
    #     expected_need_to_continue = False
    #     result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
    #     self.assertAlmostEqual(result, (expected_sim_score, expected_need_to_continue))

    #     # Test for target name "shape" 
    #     target_name = "shape"
    #     sim_score = 0.45
    #     magic_numbers = {
    #         "clarity_threshold": 0.7,
    #         "clarity_normalizing_factor": 2,
    #         "carat_enhancing_factor": 1.5,
    #         "color_threshold": 0.8,
    #         "color_normalizing_factor": 0.5,
    #     }
    #     expected_sim_score = 0.45
    #     expected_need_to_continue = True
    #     result = score_modifier.modify_sim_score_of_name(sim_score, target_name, magic_numbers)
    #     self.assertAlmostEqual(result, (expected_sim_score, expected_need_to_continue))
        
    #     # Test for invalid target column
    #     with self.assertRaises(Exception):
    #         score_modifier.modify_sim_score_of_name("invalid","","")

if __name__ == "__main__":
    unittest.main()
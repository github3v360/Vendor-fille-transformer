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

class TestTransformCutColumn(unittest.TestCase):
    def test_transform_cut_column(self):
    
        magic_numbers = common_utils.read_yaml("params.yaml")['magic_numbers']

        def test_transform_cut_column_none(self):
            cut_val = ""
            magic_numbers = {"cut_similarity_transform_df_threshold": 0.8}
            result = post_processing_utils.transform_cut_column(cut_val, magic_numbers)
            self.assertEqual(result, None)

        def test_transform_cut_column_exact_match(self):
            cut_val = "I"
            magic_numbers = {"cut_similarity_transform_df_threshold": 0.8}
            result = post_processing_utils.transform_cut_column(cut_val, magic_numbers)
            self.assertEqual(result, "I")

        def test_transform_cut_column_similar_match(self):
            cut_val = "in"
            magic_numbers = {"cut_similarity_transform_df_threshold": 0.8}
            result = post_processing_utils.transform_cut_column(cut_val, magic_numbers)
            self.assertEqual(result, "I")

        def test_transform_cut_column_no_match(self):
            cut_val = "abc"
            magic_numbers = {"cut_similarity_transform_df_threshold": 0.8}
            result = post_processing_utils.transform_cut_column(cut_val, magic_numbers)
            self.assertEqual(result, None)    



if __name__ == "__main__":
    unittest.main()
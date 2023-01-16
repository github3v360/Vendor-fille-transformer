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
    
    # Test with a shape that is close to a shape in the shape dictionary
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



if __name__ == "__main__":
    unittest.main()
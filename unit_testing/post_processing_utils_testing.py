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
  def test_transform_measurement_column(self):

      result = post_processing_utils.transform_measurement_column("2*3*4")
      self.assertEqual(result,[4,3,2])

      result = post_processing_utils.transform_measurement_column(" 2  *     3*    4 ")
      self.assertEqual(result,[4,3,2])

      result = post_processing_utils.transform_measurement_column("2+3+4")
      self.assertEqual(result,[4,3,2])

      result = post_processing_utils.transform_measurement_column("2*3+4")
      self.assertEqual(result,[4,3,2])

      result = post_processing_utils.transform_measurement_column("2.2*3.2*4.2")
      self.assertEqual(result,[4.2,3.2,2.2])

      result = post_processing_utils.transform_measurement_column(None)
      self.assertEqual(result,[None,None,None])

      result = post_processing_utils.transform_measurement_column("")
      self.assertEqual(result,[None,None,None])

      result = post_processing_utils.transform_measurement_column(1)
      self.assertEqual(result,[None,None,None])


    


if __name__ == "__main__":
    unittest.main()
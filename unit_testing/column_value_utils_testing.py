import pandas as pd
import argparse
import os
from src.utils import column_value_utils 
import unittest

class TestGetTargetColumnUniqueValues(unittest.TestCase):
    def get_target_column_unique_values(self):
        # Test for target column "clarity"
        clarity_unique_values = column_value_utils.get_target_column_unique_values("clarity")
        self.assertEqual(len(clarity_unique_values), 12)
        self.assertIn("si1 +", clarity_unique_values)
        self.assertIn("vs1 -", clarity_unique_values)
        
        # Test for target column "carat"
        carat_unique_values = column_value_utils.get_target_column_unique_values("carat")
        self.assertEqual(len(carat_unique_values), 5)
        self.assertEqual(float, type(carat_unique_values[0]))
        self.assertEqual(float, type(carat_unique_values[2]))
        
        # Test for target column "color"
        color_unique_values = column_value_utils.get_target_column_unique_values("color")
        self.assertEqual(len(color_unique_values), 17)
        self.assertIn("d", color_unique_values)
        self.assertIn("g", color_unique_values)
        
        # Test for target column "shape"
        shape_unique_values = column_value_utils.get_target_column_unique_values("shape")
        self.assertEqual(len(shape_unique_values), 148)
        self.assertIn("trapezoid", shape_unique_values)
        self.assertIn("heart", shape_unique_values)
        
        cut_unique_values = column_value_utils.get_target_column_unique_values("cut")
        self.assertEqual(len(cut_unique_values), 6)
        self.assertEqual("I", cut_unique_values)
        self.assertEqual("EX",cut_unique_values)

        polish_unique_values = column_value_utils.get_target_column_unique_values("polish")
        self.assertEqual(len(polish_unique_values), 9)
        self.assertEqual("I",polish_unique_values)
        self.assertEqual("EX",polish_unique_values)

        sym_unique_values = column_value_utils.get_target_column_unique_values("sym")
        self.assertEqual(len(sym_unique_values), 9)
        self.assertEqual("I",sym_unique_values)
        self.assertEqual("EX",sym_unique_values)

        table_unique_values = column_value_utils.get_target_column_unique_values("table")
        self.assertEqual(len(table_unique_values), 11)
        self.assertEqual(float, type(table_unique_values[0]))
        self.assertEqual(float, type(table_unique_values[2]))

        ppc_unique_values = column_value_utils.get_target_column_unique_values("price per carat")
        self.assertEqual(len(ppc_unique_values), 6)
        self.assertEqual(int, type(ppc_unique_values[0]))
        self.assertEqual(int, type(ppc_unique_values[2]))

        disc_unique_values = column_value_utils.get_target_column_unique_values("discount")
        self.assertEqual(len(disc_unique_values), 11)
        self.assertEqual(float, type(disc_unique_values[0]))
        self.assertEqual(float, type(disc_unique_values[2]))

        stockref_unique_values = column_value_utils.get_target_column_unique_values("Stock Ref")
        self.assertEqual(len(stockref_unique_values), 11)
        self.assertEqual("J841722022A", stockref_unique_values[0])
        self.assertEqual(str, type(stockref_unique_values[0]))
        # Test for invalid target column
        with self.assertRaises(Exception):
            column_value_utils.get_target_column_unique_values("invalid")

class TestGetMostCommonType(unittest.TestCase):
    def get_most_common_type(self):
        self.assertEqual(column_value_utils.get_most_common_type([1, 2, 3, 4, 5]), (int, 5))
        self.assertEqual(column_value_utils.get_most_common_type([1.0, 2.0, 3.0, 4.0, 5.0]), (float, 5))
        self.assertEqual(column_value_utils.get_most_common_type(["a", "b", "c", "d", "e"]), (str, 5))
        self.assertEqual(column_value_utils.get_most_common_type([1, 2.0, 3, 4.0, 5]), (int, 3))
        self.assertEqual(column_value_utils.get_most_common_type([1.0, 2, 3.0, 4, 5.0]), (float, 3))
        self.assertEqual(column_value_utils.get_most_common_type(["a", "b", 1, 2, 3]), (int, 3))
        self.assertEqual(column_value_utils.get_most_common_type([1.0, 2.0, "a", "b", 3.0]), (float, 3))
        self.assertEqual(column_value_utils.get_most_common_type(["a", "b", 1.0, "2", 3.0]), (str, 3))
        self.assertEqual(column_value_utils.get_most_common_type([None,None,"a","b",1]), (str, 2))

class TestSimilarityScoreFromColValues(unittest.TestCase):
    def similarity_score_from_col_values(self):
        # The whole test is takes assumption that we have correct target values

        # The logic for traget data type with string is different where 1 indicates that most of the value matches 
        # while 0 imdicated no value matches
        self.assertEqual(column_value_utils.similarity_score_from_col_values(["a", "b", "c", "d", "e"], ["a", "b", "c", "d", "e"],"target_column_with_str_values"), 1)
        self.assertEqual(column_value_utils.similarity_score_from_col_values(["a", "b", "c", "d", "e"], ["f", "g", "h", "i", "j"],"target_column_with_str_values"), 0)
        self.assertEqual(column_value_utils.similarity_score_from_col_values([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"],"target_column_with_str_values"), 1)

        # If the target data type is float or int but the input data type is str
        self.assertEqual(column_value_utils.similarity_score_from_col_values(["1", "2", "3", "4", "5"],[1, 2, 3, 4, 5],"column_with_int_values"), 0)
        self.assertEqual(column_value_utils.similarity_score_from_col_values(["1", "2", "3", "4", "5"],[1.1, 2.2, 3.3, 4.4, 5],"column_with_float_values"), 0)

        # If target column is carat 
        # In carat value range should be greater than 1 and less than 20
        self.assertEqual(column_value_utils.similarity_score_from_col_values([1.1,2.1,6.8,3.1,4.2],[1.1, 2.2, 3.3, 4.4, 5],"carat"), 1)
        self.assertEqual(column_value_utils.similarity_score_from_col_values([1.1,2.1,6.8,30,40],[1.1, 2.2, 3.3, 4.4, 5],"carat"), 0.6)

        # If target column is raprate 
        # In carat raprate range should be greater than 1000 and less than 20000
        self.assertEqual(column_value_utils.similarity_score_from_col_values([1000.1,2000,3000,4000,5000],[2000.1,2000,3000,4000,5000],"raprate"), 0.8)
        self.assertEqual(column_value_utils.similarity_score_from_col_values([1.1,2.4,4.2,2000.8,2.1],[2000.1,2000,3000,4000,5000],"raprate"), 0.2)

        # If target column is table
        # In carat raprate range should be greater than 50 and less than 72
        self.assertEqual(column_value_utils.similarity_score_from_col_values([50.00,57,63,72,64],[50.00,57,63,72,64],"table"), 1)
        self.assertEqual(column_value_utils.similarity_score_from_col_values([20,100,2,52,56],[50.00,57,63,72,64],"table"), 0.4)
if __name__ == "__main__":
    unittest.main()
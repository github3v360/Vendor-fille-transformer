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

if __name__ == "__main__":
    unittest.main()
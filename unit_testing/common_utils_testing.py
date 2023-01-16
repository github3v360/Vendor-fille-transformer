import pandas as pd
import argparse
import os
from src.utils import common_utils
import unittest

class TestGetHighestProbColumn(unittest.TestCase):
    def test_get_highest_prob_column(self):
        self.assertEqual(common_utils.get_highest_prob_column([0.7, 0.6, 0.5], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(common_utils.get_highest_prob_column([0.5, 0.6, 0.7], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(common_utils.get_highest_prob_column([0.6, 0.6, 0.6], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(common_utils.get_highest_prob_column([0.6, 0.7, 0.6], ["col1", "col2", "col3"]), "col2")
        self.assertEqual(common_utils.get_highest_prob_column([0.6, 0.6, 0.7], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(common_utils.get_highest_prob_column([2.6, 0.1, 0.2], ["col1", "col2", "col3"]), "col1")
        self.assertEqual(common_utils.get_highest_prob_column([-1, 0.1, 0.2], ["col1", "col2", "col3"]), "col3")
        self.assertEqual(common_utils.get_highest_prob_column([0, 0.8, 0.5], ["col1", "col2", "col3"]), "col2")
        self.assertEqual(common_utils.get_highest_prob_column([1.6, -1, -1], ["col1", "col2", "col3"]), "col1")
if __name__ == "__main__":
    unittest.main()
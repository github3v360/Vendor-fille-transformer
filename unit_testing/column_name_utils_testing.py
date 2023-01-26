import pandas as pd
import argparse
import os
from src.utils import column_name_utils 
import unittest


class TestSimilarityScoreFromColName(unittest.TestCase):
    def test_similarity_score_from_col_name(self):
        self.assertEqual(column_name_utils.similarity_score_from_col_name("column1", ["column1", "column2", "column3"]), 1.0)
        self.assertLessEqual(column_name_utils.similarity_score_from_col_name("shape", ["color", "carat","clarity"]), 0.2)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("col1", ["column1", "column2", "column3"]), 0.5)
        self.assertEqual(column_name_utils.similarity_score_from_col_name("Shape", ["Shape", "tape"]), 1.0)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("column1", ["col1", "col2", "col3"]), 0.5)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("carat", ["Ct.", "shape", "color"]), 0.15)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("carat", ["weight", "clor", "cot"]), 0.3)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("color", ["colour", "cl.", "co"]), 0.5)
        self.assertGreaterEqual(column_name_utils.similarity_score_from_col_name("shape", ["shap", "sh.", "carat"]), 0.4)

class TestGetStandardNames(unittest.TestCase):
    def test_clarity(self):
        std_names = column_name_utils.get_standard_names("clarity")
        self.assertEqual(std_names, ["clarity", "purity"])
    
    def test_color(self):
        std_names = column_name_utils.get_standard_names("color")
        self.assertEqual(std_names, ["color", "colour"])
        
    def test_shape(self):
        std_names = column_name_utils.get_standard_names("shape")
        self.assertEqual(std_names, ["shape"])
        
    def test_carat(self):
        std_names = column_name_utils.get_standard_names("carat")
        self.assertEqual(std_names, ["carat", "size", "cts", "crtwt"])

    def test_cut(self):
        std_names = column_name_utils.get_standard_names("cut")
        self.assertEqual(std_names, ["Cut", "CutGrade"])

    def test_polish(self):
        std_names = column_name_utils.get_standard_names("polish")
        self.assertEqual(std_names, ["Finish", "Pol","polish"])

    def test_sym(self):
        std_names = column_name_utils.get_standard_names("symmetry")
        self.assertEqual(std_names, ["Sym", "Symetry", "Sym-metry","symmetry"])
        
    def test_table(self):
        std_names = column_name_utils.get_standard_names("table")
        self.assertEqual(std_names, ["Table", "Table Percent", "TablePct", "TablePercent", "Tbl"])

    def test_ppc(self):
        std_names = column_name_utils.get_standard_names("price per carat")
        self.assertEqual(std_names, ["PerCarat", "PerCt", "Prc", "PriceCarat", "PriceCt", "PricePerCarat", "PricePerCt"])

    def test_discount(self):
        std_names = column_name_utils.get_standard_names("discount")
        self.assertEqual(std_names, ["RDiscPct", "RDpx", "RRapPct", "RapNet Discount Price","per","disc","disc%","RapNet Discount %"])

    def test_invalid_name(self):
        with self.assertRaises(Exception):
            column_name_utils.get_standard_names("invalid_name")

class TestStringSimilarity(unittest.TestCase):
    def test_string_similarity(self):
        self.assertAlmostEqual(column_name_utils.string_similarity("Hello", "Hello"), 1.0)
        self.assertAlmostEqual(column_name_utils.string_similarity("Hello", "heLLo"), 1.0)
        self.assertGreaterEqual(column_name_utils.string_similarity("Hello", "Helo"), 0.6)
        self.assertGreaterEqual(column_name_utils.string_similarity("Hello", "Hullo"), 0.6)
        self.assertGreaterEqual(column_name_utils.string_similarity(" ", "None"), 0.0)
        self.assertEqual(column_name_utils.string_similarity("Hello", "Bye"), 0.0)
        self.assertEqual(column_name_utils.string_similarity(1, "1"), 1.0)
        self.assertEqual(column_name_utils.string_similarity(1, "Bye"), 0.0)
        self.assertEqual(column_name_utils.string_similarity(1.23, "1.23"), 1.0)
        self.assertGreaterEqual(column_name_utils.string_similarity(1.2, "1.23"), 0.6)

if __name__ == "__main__":
    unittest.main()

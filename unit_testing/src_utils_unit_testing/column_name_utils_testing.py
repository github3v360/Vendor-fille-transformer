import pandas as pd
import argparse
import os
from src.utils import column_name_utils 
import unittest

import logging

class TestGetStandardNames(unittest.TestCase):
    
    def setUp(self):
        self.logger = logging.getLogger(__name__)
    
    def test_clarity(self):
        expected = ["clarity","purity","Clar", "Clearity"]
        result = column_name_utils.get_standard_names("clarity", self.logger)
        self.assertEqual(result, expected)
    
    def test_color(self):
        expected = ["color","colour","Colr","col"]
        result = column_name_utils.get_standard_names("color", self.logger)
        self.assertEqual(result, expected)
    
    def test_shape(self):
        expected = ["shape","shp"]
        result = column_name_utils.get_standard_names("shape", self.logger)
        self.assertEqual(result, expected)
    
    def test_carat(self):
        expected = ["Carat", "CaratSize", "CaratWeight", "Ct", "CtSize", "CtWeight", "Weight", "Sz", "cts",  "crtwt","size"]
        result = column_name_utils.get_standard_names("carat", self.logger)
        self.assertEqual(result, expected)
    
    def test_fluorescent(self):
        expected = ["fluor","flour","fluorescent","Flr", "FlrIntensity", "Fluo Intensity", "Fluor Intensity", "Fluorescence", "Fluorescence Intensity", "FluorescenceIntensity", "FluorIntensity"]
        result = column_name_utils.get_standard_names("fluorescent", self.logger)
        self.assertEqual(result, expected)
    
    def test_raprate(self):
        expected = ["Rap",'Rapprice']
        result = column_name_utils.get_standard_names("raprate", self.logger)
        self.assertEqual(result, expected)
    
    def test_length(self):
        expected = ["M1","Measurement","Diameter","length"]
        result = column_name_utils.get_standard_names("length", self.logger)
        self.assertEqual(result, expected)

    def test_depth(self):
        expected = ["M3","Measure","Diameter","depth","height"]
        result = column_name_utils.get_standard_names("depth", None)
        self.assertEqual(result, expected)
        
    def test_cut(self):
        expected = ["Cut", "CutGrade"]
        result = column_name_utils.get_standard_names("cut", None)
        self.assertEqual(result, expected)
        
    def test_polish(self):
        expected = ["Finish", "Pol","polish"]
        result = column_name_utils.get_standard_names("polish", None)
        self.assertEqual(result, expected)
        
    def test_symmetry(self):
        expected = ["Sym", "Symetry", "Sym-metry","symmetry"]
        result = column_name_utils.get_standard_names("symmetry", None)
        self.assertEqual(result, expected)
        
    def test_table(self):
        expected = ["Table", "Table Percent", "TablePct", "TablePercent", "Tbl","Table%","Table Depth"]
        result = column_name_utils.get_standard_names("table", None)
        self.assertEqual(result, expected)
        
    def test_comments(self):
        expected = ["Comments", "Remark", "Lab comment", "Cert comment", "Certificate comment", "Laboratory comment","Report Comments"]
        result = column_name_utils.get_standard_names("comments", None)
        self.assertEqual(result, expected)
        
    def test_price_per_carat(self):
        expected = ["PerCarat", "PerCt", "Prc", "PriceCarat", "PriceCt", "PricePerCarat", "PricePerCt", "Px","price/carat"]
        result = column_name_utils.get_standard_names("price per carat", None)
        self.assertEqual(result, expected)
        
    def test_discount(self):
        expected = ["disc","disc%","RapNet Discount %", "PctRapNetDiscount", "Rap netDisc", "RapnetDiscount", "RapnetDiscountPct", "RapnetDiscountPercent", "RapnetDiscPct", "RapnetDpx", "RapnetRapPct", "RDisc", "RDiscount", "RDiscountPct", "RDiscountPercent", "RDiscPct", "RDpx", "RRapPct", "RapNet Discount Price","per"]
        result = column_name_utils.get_standard_names("discount", None)
        self.assertEqual(result, expected)
        
    def test_total(self):
        expected = ["amount","total","total price"]
        result = column_name_utils.get_standard_names("total", None)
        self.assertEqual(result, expected)
        
    def test_rap_price_total(self):
        expected = ["rap total","rap value"]
        result = column_name_utils.get_standard_names("rap price total", None)
        self.assertEqual(result, expected)
        
    def test_stock_ref(self):
        expected = ["ReferenceNum", "ReferenceNumber", "Stock", "Stock Num", "Stock_no", "StockNo", "StockNum", "StockNumber", "VenderStockNumber","Refno","Packet No"]
        result = column_name_utils.get_standard_names("Stock Ref", None)
        self.assertEqual(result, expected)
    
    def test_unknown_target_name(self):
        with self.assertLogs() as cm:
            result = column_name_utils.get_standard_names("unknown", self.logger)
            self.assertEqual(result, None)
            self.assertTrue("The function could not find other satndard names for this target name" in cm.output[0])

class TestStringSimilarity(unittest.TestCase):

    def test_same_strings(self):
        self.assertEqual(column_name_utils.string_similarity("hello", "hello"), 1.0)
    
    def test_different_strings(self):
        self.assertLess(column_name_utils.string_similarity("hello", "world"), 0.5)
    
    def test_capitalization(self):
        self.assertEqual(column_name_utils.string_similarity("Hello", "hello"), 1.0)
    
    def test_numeric_input(self):
        self.assertEqual(column_name_utils.string_similarity(123, "123"), 1.0)
    
    def test_none_input(self):
        self.assertEqual(column_name_utils.string_similarity(None, "hello"), 0.0)
        self.assertEqual(column_name_utils.string_similarity("hello", None), 0.0)
    
    def test_unicode_input(self):
        self.assertEqual(column_name_utils.string_similarity("héllo", "hello"), 0.8)

class TestSimilarityfromColumnName(unittest.TestCase):

    def test_similarity_score_from_col_name(self):
        # Test case 1: Exact match
        column_name = 'clarity'
        std_names = ['clarity','purity','Clar', 'Clearity']
        assert column_name_utils.similarity_score_from_col_name(column_name, std_names) == 1
        
        # Test case 2: Partial match
        column_name = 'clrty'
        std_names = ['clarity','purity','Clar', 'Clearity']
        result = column_name_utils.similarity_score_from_col_name(column_name, std_names)
        assert  result == 0.714
        
        # Test case 3: No match
        column_name = 'weight'
        std_names = ['clarity','purity','Clar', 'Clearity']
        result = column_name_utils.similarity_score_from_col_name(column_name, std_names)
        assert  result == 0.25
        
        # Test case 4: Same strings with different cases
        column_name = 'Color'
        std_names = ['color','colour','Colr','col']
        result = column_name_utils.similarity_score_from_col_name(column_name, std_names)
        assert  result == 1
        
        # Test case 5: Similar strings
        column_name = 'lenght'
        std_names = ['M1','Measurement','Diameter','length']
        result = column_name_utils.similarity_score_from_col_name(column_name, std_names)
        assert  result == 0.667

if __name__ == '__main__':
    unittest.main()
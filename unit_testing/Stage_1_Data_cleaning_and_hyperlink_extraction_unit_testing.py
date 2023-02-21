import unittest
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
from src.Stage_1_data_cleaning_and_link_extraction import CleanDataAndExtractLink
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestStage1DataCleaningAndExtraction(unittest.TestCase):

    def setUp(self):

        '''
        We are going to use the stage_1_testing_file.xlsx file which contains different 
        types of link, empty columns and improper headers to test our Stage_1_data_cleaning_and_link_extraction.py. 
        See the file to get the proper insight
        '''
        self.ws = load_workbook('artifacts/files_for_unit_testing/stage_1_testing_file.xlsx')['Sheet1']
        self.initial_df = pd.read_excel('artifacts/files_for_unit_testing/stage_1_testing_file.xlsx')
        self.logger = None

        self.cleaner_and_link_extractor = CleanDataAndExtractLink(self.initial_df,self.ws,self.logger)
    
    def test_process(self):
        output_df, extracted_link_columns_name = self.cleaner_and_link_extractor.process()

        '''
        ============ Test 1 =================

        What we check?
        1. Here we check that many columns were dropped since they are empty
        2. We also check that how many columns were added during hyperlink extraction
        3. We also check how many rows were removed while getting the correct headers

        What can be the expected output for the above questions?
        Our input file had 8 rows and 13 columns 
        Our input file has correct header at 4 th row. Therefore first 
        three rows will be removed. The ouput will have 8-3 = 5  rows
        Our input have 1 empty column. In hyperlink extraction we wil fetch 3 columns which 
        are ['Image_link', 'Cert._link', 'report_no']. Therefore our output 
        have 13 -1 + 3 = 15 columns
        '''
        self.assertEqual(output_df.shape,(5,15))
        
        '''
        ============ Test 2 ================= 

        We wil check what are the extracted columns in hyperlink extraction 
        and we wil fetch 3 columns which 
        are ['Image_link', 'Cert._link', 'report_no']. Therefore our output 
        '''
        expected_extracted_link_columns_name =  ['Image_link', 'Cert._link', 'report_no']
        self.assertEqual(extracted_link_columns_name,expected_extracted_link_columns_name)

if __name__ == '__main__':
    unittest.main()

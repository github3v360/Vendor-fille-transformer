import unittest
import pandas as pd
import logging
from openpyxl import Workbook
from openpyxl import load_workbook
from src.utils import common_utils
from src.Stage_2_probability_calculation import DataProcessor
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# setting up the logger for test purpose
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_path = "running_logs/test.log"
formatter = logging.Formatter('Time: %(asctime)s   :    %(message)s')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class TestStage1DataCleaningAndExtraction(unittest.TestCase):

    def setUp(self):
        self.df_cleaned = pd.read_csv('artifacts/files_for_unit_testing/Stage_2_testing_file.csv')
        self.logger = logger
        self.link_columns_name = ["Image_link","Cert._link","report_no"]
        self.count_of_rows = self.df_cleaned.shape[0]
        self.Date = "19/02/2023"
        self.test_file_name = "Vendor_70"
        self.target_columns = ['clarity','carat','color','shape', "fluorescent","raprate",'cut','polish',"symmetry","table","length","width","depth",
                               "price per carat","discount","total","rap price total","comments",'report_no']
        self.prob_dict = common_utils.initialize_prob_dict(self.target_columns)
        self.magic_numbers = common_utils.get_magic_numbers()
        self.cur_df_cleaned_column_name = "carat"
        self.processor = DataProcessor(self.df_cleaned, self.logger, self.link_columns_name, self.count_of_rows, self.Date, self.test_file_name)

    def test_Probability_Based_DataExtraction(self):
        df_pre_processed, report_no_from_link, magic_numbers, prob_dict, remaining_columns_df, target_columns = self.processor.Probability_Based_DataExtraction()
        pass

    def test_get_unique_values(self):
        pass

    def test_get_current_column_values(self):

        '''
        Here we will test 
        '''
        pass
if __name__ == '__main__':
    unittest.main()

from src import Single_Sheet_extraction
import pandas as pd
import openpyxl, datetime, random
from openpyxl import load_workbook

class Entire_file_extractor:
    
    def __init__(self, file_path, debug, logger, test_file_name):
        self.file_path = file_path
        self.debug = debug
        self.logger = logger
        self.test_file_name = test_file_name

    def extract(self):
        gap = random.randint(0, 10)
        now = (datetime.datetime.now() - datetime.timedelta(days=gap)).strftime("%d/%m/%Y")

        # this is flag which will tell whether the file is excel or not
        is_excel = False

        # Load the Pandas Data Frame with all sheets
        if self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
            wb = pd.read_excel(self.file_path, None)

            # Read Data file with openpyxl
            wb_xl = load_workbook(self.file_path)

            # Fetching all sheet names
            sheet_names = list(wb.keys())

            # setting is_excel flag to True
            is_excel = True

        elif self.file_path.endswith('.csv'):

            # Reading a csv file
            wb = pd.read_csv(self.file_path)

            # Since csv files do not have multiple sheets 
            # we will assign a random name
            sheet_names = ['random_sheet']
        
        else:
            self.logger.exception("This file format is not supported")

        # Initializing Global DataFrame which will store all the processed sheet
        global_df = None

        # Iterating through all the sheet
        for sheet_name in sheet_names:

            if is_excel:

                # Fetching and storing the sheet
                df = wb[sheet_name]
                
                # Getting openpyxl current sheet
                cur_wb_xl = wb_xl[sheet_name]
            
            else:
                df = wb
                cur_wb_xl = None

            # Check if the sheet is empty
            if df.empty:
                continue

            # Data Extraction from current sheet
            extractor = Single_Sheet_extraction.ExtractFromSingleSheet(df, cur_wb_xl, self.debug, self.logger, now, self.test_file_name)
            out_df = extractor.process()

            # Concatenation of global dataframe with out_df
            if global_df is None:
                global_df = out_df
                continue

            global_df = pd.concat([global_df, out_df])

        return global_df
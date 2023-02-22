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

        # Load the Pandas Data Frame with all sheets
        wb = pd.read_excel(self.file_path, None)

        # Read Data file with openpyxl
        wb_xl = load_workbook(self.file_path)

        # Fetching all sheet names
        sheet_names = list(wb.keys())

        # Initializing Global DataFrame which will store all the processed sheet
        global_df = None

        # Iterating through all the sheet
        for sheet_name in sheet_names:
            # Fetching and storing the sheet
            df = wb[sheet_name]

            # Check if the sheet is empty
            if df.empty:
                continue

            # Data Extraction from current sheet
            extractor = Single_Sheet_extraction.ExtractFromSingleSheet(df, wb_xl[sheet_name], self.debug, self.logger, now, self.test_file_name)
            out_df = extractor.process()

            # Concatenation of global dataframe with out_df
            if global_df is None:
                global_df = out_df
                continue

            global_df = pd.concat([global_df, out_df])

        return global_df
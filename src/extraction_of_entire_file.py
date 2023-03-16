'''
This file contains class for performing post processing with column values in dataframes.
'''
import datetime
import random
import pandas as pd

from openpyxl import load_workbook
from src import single_sheet_extraction

class EntireFileExtractor:
    """
    Initially checks for the extension of file and then run the whole 
    program on each dataframe extracted.

    At the end, returns combined all the output from a single workbook.
    Args:
        file_path: Test File Path (String)
        debug: Flag Variable (int)
        logger: Logger (logger)
        test_file_name: File Name (String)
    Returns:
        global_data_frame : Processed Dataframe (Dataframe)

    """
    def __init__(self, file_path, debug, logger, test_file_name):
        self.file_path = file_path
        self.debug = debug
        self.logger = logger
        self.test_file_name = test_file_name

    def extract(self):
        """
        Extracts each sheet from workbooks and apply whole process of 
        'Single Sheet extraction' on that Dataframe.

        Concatenate all the outputs to final excel sheet
        """
        gap = random.randint(0, 10)
        now = (datetime.datetime.now() - datetime.timedelta(days=gap)).strftime("%d/%m/%Y")

        # this is flag which will tell whether the file is excel or not
        sheet_names,is_excel,work_book,work_book_xl = self.check_extension_of_sheet()
        # Initializing Global DataFrame which will store all the processed sheet
        global_data_frame = None

        # Iterating through all the sheet
        for sheet_name in sheet_names:
            if is_excel:
                # Fetching and storing the sheet
                data_frame = work_book[sheet_name]
                # Getting openpyxl current sheet
                cur_work_book_xl = work_book_xl[sheet_name]
            else:
                data_frame = work_book
                cur_work_book_xl = None
            # Check if the sheet is empty
            if data_frame.empty:
                continue

            # Data Extraction from current sheet
            extractor = single_sheet_extraction.ExtractFromSingleSheet(data_frame,
                        cur_work_book_xl, self.debug, self.logger, now, self.test_file_name)
            out_data_frame = extractor.process()

            # Concatenation of global dataframe with out_data_frame
            if global_data_frame is None:
                global_data_frame = out_data_frame
                continue

            global_data_frame = pd.concat([global_data_frame, out_data_frame])

        return global_data_frame

    def check_extension_of_sheet(self):
        """
        Checks for the type of extension of file.
        It accepts xlxs and csv extensions only.
        """
        is_excel = False

        # Load the Pandas Data Frame with all sheets
        if self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
            work_book = pd.read_excel(self.file_path, None)

            # Read Data file with openpyxl
            work_book_xl = load_workbook(self.file_path)

            # Fetching all sheet names
            sheet_names = list(work_book.keys())

            # setting is_excel flag to True
            is_excel = True

        elif self.file_path.endswith('.csv'):

            # Reading a csv file
            work_book = pd.read_csv(self.file_path)
            # Since csv files do not have multiple sheets
            # we will assign a random name
            sheet_names = ['random_sheet']

        else:
            self.logger.exception("This file format is not supported")

        return sheet_names,is_excel,work_book,work_book_xl

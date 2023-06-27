'''
This file contains class for performing post processing with column values in dataframes.
'''
import datetime
import random
import pandas as pd

from openpyxl import load_workbook
import xlrd


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
        vendor_name: File Name (String)
    Returns:
        global_data_frame : Processed Dataframe (Dataframe)

    """
    def __init__(self, file_path, debug, logger, date, vendor_name):
        self.file_path = file_path
        self.debug = debug
        self.logger = logger
        self.date = date
        self.vendor_name = vendor_name

    def extract(self):
        """
        Extracts each sheet from workbooks and apply whole process of 
        'Single Sheet extraction' on that Dataframe.

        Concatenate all the outputs to final excel sheet
        """
        print("In EXTRACT Method")
        # this is flag which will tell whether the file is excel or not
        sheet_names,is_excel,work_book,work_book_xl = self.check_extension_of_sheet()
        # Initializing Global DataFrame which will store all the processed sheet
        global_missing_data_frame = None
        global_clean_data_frame = None

        # Iterating through all the sheet
        for sheet_name in sheet_names:
            self.logger.info("New Sheet Started")
            if is_excel:
                # Fetching and storing the sheet
                data_frame = work_book[sheet_name]

                # Getting openpyxl current sheet
                cur_work_book_xl = None if work_book_xl is None else work_book_xl[sheet_name]
            else:
                data_frame = work_book
                cur_work_book_xl = None
            # Check if the sheet is empty
            if data_frame.empty:
                continue

            # Data Extraction from current sheet
            extractor = single_sheet_extraction.ExtractFromSingleSheet(data_frame,
                        cur_work_book_xl, self.debug, self.logger, self.date, self.vendor_name)
            
            df_clean, df_missing = extractor.process()
            self.logger.info("------------------------ Process Completed for this sheet ------------------------")

            # Concatenation of global dataframe with out_data_frame
            if global_clean_data_frame is None:
                flag = True
                if ~ df_clean.empty:
                    self.logger.info("------------------------ Clean Dataframe appended ------------------------")
                    global_clean_data_frame = df_clean

            if global_missing_data_frame is None:
                flag = True
                if ~ df_missing.empty:
                    self.logger.info("------------------------ Missing Dataframe appended ------------------------")
                    global_missing_data_frame = df_missing


            if (not (df_clean.empty ))and flag is False:
                global_clean_data_frame = pd.concat([global_clean_data_frame, df_clean])
                flag = False
            if (not (df_missing.empty )) and flag is False:
                global_missing_data_frame = pd.concat([global_missing_data_frame, df_missing])
                flag = False

        return global_clean_data_frame,global_missing_data_frame

    def check_extension_of_sheet(self):
        """
        Checks for the type of extension of file.
        It accepts xlxs and csv extensions only.
        """
        is_excel = False

        # Load the Pandas Data Frame with all sheets
        if self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
            work_book = pd.read_excel(self.file_path, sheet_name = None, header = None)

            # Fetching all sheet names
            sheet_names = list(work_book.keys())
            # setting is_excel flag to True
            is_excel = True

            try:
                # Read Data file with openpyxl
                work_book_xl = load_workbook(self.file_path)
            except:
                work_book_xl = None

        elif self.file_path.endswith('.csv'):

            # Reading a csv file
            work_book = pd.read_csv(self.file_path)
            # Since csv files do not have multiple sheets
            # we will assign a random name
            sheet_names = ['random_sheet']
            work_book_xl = None

        else:
            self.logger.exception("This file format is not supported")

        return sheet_names,is_excel,work_book,work_book_xl


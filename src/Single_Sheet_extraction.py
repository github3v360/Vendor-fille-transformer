import logging
import pandas as pd
import os
from src import Stage_1_data_cleaning_and_link_extraction
from src import Stage_2_probability_calculation
from src import Stage_3_post_processing

class ExtractFromSingleSheet:
    def __init__(self, df, ws, debug, logger, Date, test_file_name):
        self.df = df
        self.ws = ws
        self.debug = debug
        self.logger = logger
        self.Date = Date
        self.test_file_name = test_file_name
    
    def process(self):
        self.logger.info("-" * 75)
        
        # ======= Run Stage 1 (Which wil clean the data and extract the link) ==========
        processor = Stage_1_data_cleaning_and_link_extraction.CleanDataAndExtractLink(self.df, self.ws, self.logger)
        df_cleaned, link_columns_name = processor.process()

        # It is possible that initially sheet is not empty but
        # after cleaning sheet gets empty so we return the empty dataframe from here
        if len(df_cleaned.columns) == 0:
            return df_cleaned
        
        # ==== Stage 2 process the data (probability calculation) ======

        count_of_rows = df_cleaned.shape[0]

        processor = Stage_2_probability_calculation.DataProcessor(df_cleaned, self.logger, link_columns_name, count_of_rows, self.Date, self.test_file_name)
        df_pre_processed, report_no_from_link, magic_numbers, prob_dict, remaining_columns_df, target_columns = processor.Probability_Based_DataExtraction()
        
        #  ====== Stage 3 post-process the data =========
        processor = Stage_3_post_processing.PostProcessingData(
                             df_pre_processed, df_cleaned, report_no_from_link, magic_numbers,
                             prob_dict, link_columns_name, remaining_columns_df,
                             target_columns, self.Date, self.test_file_name,self.logger)
        
        df_processed = processor.process_data()
                
        return df_processed

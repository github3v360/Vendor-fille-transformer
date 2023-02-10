# Importing Required Libraries
import logging
import pandas as pd
import os
from src import Stage_1_data_cleaning_and_link_extraction
,Stage_2_probability_calculation, Stage_3_post_processing

def extract_from_single_sheet(df, ws, debug, logger, Date, test_file_name):

    logger.info("-" * 75)

    # ======= Run Stage 1 (Which wil clean the data and extract the link) ==========
    df_cleaned,link_columns_name = Stage_1_data_cleaning_and_link_extraction.clean_data_and_extract_link(df, ws, logger)

    # It is possible that initially sheet is not empty but
    # after cleaning sheet gets empty so we return the empty dataframe from here
    if len(df_cleaned.columns) == 0:
        return df_cleaned
    
    # ==== Stage 2 process the data (probability calculation) ======

    count_of_rows = df_cleaned.shape[0]

    df_pre_processed, report_no_from_link, magic_numbers, 
    prob_dict, remaining_columns_df, target_columns = Stage_2_probability_calculation.process_data(
                                                      df_cleaned, logger, link_columns_name,count_of_rows,
                                                      Date, test_file_name)

    #  ====== Stage 3 post-process the data =========
    df_processed = Stage_3_post_processing.post_processing_data(
                         df_pre_processed, df_cleaned, report_no_from_link, magic_numbers,
                         prob_dict, link_columns_name, remaining_columns_df,
                         target_columns, Date, test_file_name,logger)

    return df_processed
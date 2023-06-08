'''
This file contains class for applying whole logic on a single sheet of workbook
'''
# pylint: disable=too-few-public-methods
from src import Stage_1_data_cleaning_and_link_extraction
from src import Stage_2_probability_calculation
from src import Stage_3_post_processing

class ExtractFromSingleSheet:
    """
    Class calls primarily 3 different classes to process and analys whole data.
    Which includes cleaning, pre and post processing data.

    Args:
        data_frame: Unprocessed Dataframe(DataFrame)
        debug: Flag Variable (int) 
        logger: Logger (logger)
        date: Date entered by Vendor (Date)
        test_file_name: File Name (String)
        work_sheet: Current Worksheet (worksheet)
        
    Returns:
        df_processed : Processed Dataframe (Dataframe)

    """
    def __init__(self, data_frame, work_sheet, debug, logger, date, test_file_name):
        self.data_frame = data_frame
        self.work_sheet = work_sheet
        self.debug = debug
        self.logger = logger
        self.date = date
        self.test_file_name = test_file_name

    def process(self):
        """
        Process a given data frame through three stages of data cleaning and analysis.

        Returns:
            df_processed: A processed data frame after the three stages of processing.

        The three stages of processing are:
        1. Data Cleaning and Link Extraction - cleans the data and extracts links.
        2. Probability Calculation - calculates the probability of the data.
        3. Post Processing - post-processes the data after probability calculation.

        Each stage of processing is performed by a different class, 
        and the processed data frame from
        one stage is passed as input to the next stage. If the data frame 
        is empty after cleaning in the
        first stage, an empty data frame is returned.
        """
        self.logger.info("-" * 75)

        # ======= Run Stage 1 (Which wil clean the data and extract the link) ==========
        processor = Stage_1_data_cleaning_and_link_extraction.CleanDataAndExtractLink(
                    self.data_frame, self.work_sheet, self.logger)
        df_cleaned, link_columns_name = processor.process()
        # It is possible that initially sheet is not empty but
        # after cleaning sheet gets empty so we return the empty
        # dataframe from here
        if len(df_cleaned.columns) == 0:
            return df_cleaned

        # ==== Stage 2 process the data (probability calculation) ======
        count_of_rows = df_cleaned.shape[0]

        processor = Stage_2_probability_calculation.DataProcessor(
                    df_cleaned, self.logger, link_columns_name,
                    count_of_rows, self.date, self.test_file_name)
        df_pre_processed, report_no_from_link, magic_numbers, prob_dict, \
        remaining_columns_df, target_columns = processor.Probability_Based_DataExtraction()

        #  ====== Stage 3 post-process the data =========
        processor = Stage_3_post_processing.PostProcessingData(
                             df_pre_processed, df_cleaned, report_no_from_link, magic_numbers,
                             prob_dict, link_columns_name, remaining_columns_df,
                             target_columns, self.date, self.test_file_name,
                             self.logger)

        df_processed = processor.process_data()
        column_names_map = {"reportNo":"ReportNo","shape":"Shape","carat":"Carat","color":"Color","clarity":"Clarity","cut":"Cut","polish":"Polish",
        "symmetry":"Symmetry","fluorescent":"Fluorescent","rapRate":"RapRate","discount":"Discount","rapPriceTotal":"RapPriceTotal",
        "pricePerCarat":"PricePerCarat","total":"Total", "table":"Table","length":"Length","width":"Width",
        "depth":"Depth","comments":"Comments"}
        # Rename the columns using the dictionary
        df_processed.rename(columns=column_names_map, inplace=True)
        return df_processed

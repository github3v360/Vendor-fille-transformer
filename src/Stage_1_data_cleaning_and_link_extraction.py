'''
This file contains the class 'CleanDataAndExtractLink' 
which will perform all the stage 1 tasks
'''

from src.utils import data_cleaner
from src import hyperlink_extraction

class CleanDataAndExtractLink:
    '''
    This Class will do the following:
    1. Correct the headers
    2. Extract the link
    3. Extract the report number from the extracted link
    4. Clean the data (removing empty rows and columns).
    '''
    def __init__(self, dataframe, openpyxl_workbook, logger):
        '''
        Initializes the instance based on the attributes.

        Attributes:
            dataframe (pandas dataframe): Dataframe returned
                      by pandas after reading one of a file's sheets.
            
            openpyxl_workbook: openpyxl workbook of one of a file's sheets.
                               This is used to get the hyperlink since
                               pandas dataframe do not store the hypelink
            
            logger: Python's logger to log the Info, Errors and Exceptions
        '''
        self.dataframe = dataframe
        self.openpyxl_workbook = openpyxl_workbook
        self.logger = logger

    def process(self):

        """
        This function will execute all of the necessary utils functions in order to correct the 
        headers, extract the link, extract the report number from the extracted link, and
        clean the data (removing empty rows and columns).

        Returns:
            df_cleanded (pandas DataFrame): A DataFrame with the headers corrected. The
                                             extracted hyperlinks are also included in 
                                             this DataFrame.
            
            link_columns_name (List): A list of the names of the extracted links
        """

        # Correcting the DataFrame Headers
        df_corrected_headers, correct_row_idx = data_cleaner.correct_df_headers(self.dataframe)

        # Extracting the hyperlink and report number from the link
        hyperlink_extractor = hyperlink_extraction.HyperlinkExtractor(
            self.openpyxl_workbook, correct_row_idx, df_corrected_headers
        )

        df_with_links, link_columns_name = hyperlink_extractor.add_hyperlink_columns()

        # Dropping Empty Rows and columns
        df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)

        return df_cleaned, link_columns_name

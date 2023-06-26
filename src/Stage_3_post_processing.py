'''
This file contains the class 'PostProcessingData' 
which will perform all the stage 3 tasks
'''

import pandas as pd
from src import StandardValueConverterAndCalculation


class PostProcessingData:
    '''
    This Class has the following functionalities:
        1. Transform the DataFrame
        2. Add Report Number column
        3. Log the the missing target columns
        4. Log the number of rows without report number
        5. Add date column and vendor name column
        6. Add the link columns and extra columns
    '''
    def __init__(
        self,
        dataframe_pre_processed,
        dataframe_cleaned,
        report_no_from_link,
        magic_numbers,
        prob_dict,
        link_columns_name,
        remaining_columns_dataframe,
        target_columns,
        date,
        vendor_name,
        logger,
    ):
        '''
        Initializes the instance based on the attributes.

        Args:
            dataframe_pre_processed (pandas dataframe): Pre-processed dataframe
            given by stage 2

            dataframe_cleaned (pandas dataframe): cleaned dataframe given by the stage 1

            report_no_from_link (list): report number extracted from the link

            magic_number(dictionary): Dictionary cotaning the magic numbers 

            prob_dict(dictionary): A probability dictionary containing the probability 
            that a target column was chosen from the data.

            link_columns_name(list): list of links column name

            remaining_columns_dataframe(pandas dataframe): DataFrame which 
            contains all the extra (redundant) columns in the form of dictionary
            
            target_columns(list): A list of the name of all the target columns

            date: date (exact description of this date will be updated later)

            vendor_name: Name of the vendor

            logger: Python's logger to log the Info, Errors and Exceptions

        '''

        self.dataframe_pre_processed = dataframe_pre_processed
        self.dataframe_cleaned = dataframe_cleaned
        self.report_no_from_link = report_no_from_link
        self.magic_numbers = magic_numbers
        self.prob_dict = prob_dict
        self.link_columns_name = link_columns_name
        self.remaining_columns_dataframe = remaining_columns_dataframe
        self.target_columns = target_columns
        self.date = date
        self.vendor_name = vendor_name
        self.logger = logger

    def add_report_number(self, dataframe):
        """
        This function will create a new column called 'report no from link'
        to store the report number obtained from the link, as well as initialise
        the column'report no' with values. If we are unable to extract the report
        number from the sheet, None will be assigned; otherwise, the extracted
        values will be assigned.

        Args:
            dataframe (pandas dataframe): Input dataframe with report number column
        Returns:
            dataframe (pandas dataframe): Dataframe with report nnumber column added

        """
        dataframe["report_no_from_link"] = self.report_no_from_link
        dataframe["reportNo"] = dataframe["reportNo"] if "reportNo" in dataframe else None
        return dataframe

    def transform_values(self, dataframe):
        """
        This function will create object for StandardValueConverterAndCalculation class
        which will do the following -:
            1. Convert the non-standard values to standard values for shape, fluorescent
               and cut column. Eg-: "RND" to "ROUND"
            2. Extract the length, width and depth from this format "2*7*8" and then
               calculate depth% and ratio
            3. If the carat, raprate, and one of the other price-related columns are
               present, the other price-related columns will be calculated.
            4. Combine the 'report_no_from_link' and 'report_no' to get final report_no
        
        Args:
            dataframe (pandas dataframe): Input DataFrame 
        Returns:
            transformed_dataframe (pandas dataframe): Transformed DataFrame in which 
            the aforementioned transformations will take place

        """
        fetched_columns = list(dataframe.columns)
        value_transformer = StandardValueConverterAndCalculation.PostProcessing(
            fetched_columns, dataframe, self.magic_numbers, self.prob_dict, self.logger
        )
        transformed_dataframe = value_transformer.process()
        return transformed_dataframe

    def log_missing_target_columns(self, dataframe, target_columns):
        '''
        The function will log that which columns were were unable to be extracted by
        our logic.

        Args:
            dataframe (pandas dataframe): Input dataframe
            target_columns (list): A list of name of target columns
        '''
        target_columns += ["ratio", "depth %"]
        self.logger.info("-" * 75)
        self.logger.info(f"Not able to detect {set(target_columns) - set(dataframe.columns)}")

    def add_links_and_extra_columns(self, dataframe, link_columns_name):
        """
        This function will simply add link columns
        in our output dataframe

        Args:
            dataframe (pandas dataframe): Input dataframe without link columns

            links_columns_name (list): List of link columns names

        Returns:
            dataframe (pandas dataframe): DataFrame with links columns
            and extra column
        
        """
        dataframe[link_columns_name] = self.dataframe_cleaned[link_columns_name]
        dataframe = pd.concat([dataframe, self.remaining_columns_dataframe], axis=1)
        return dataframe

    def log_missing_report_no(self, dataframe):
        '''
        This function will log the number of rows without report number

        Args:
            dataframe (pandas dataframe): Input DataFrame with report_no
            column
        '''
        if "reportNo" in dataframe.columns:
            self.logger.info(
            f"The total number of columns without a report number is {dataframe['reportNo'].isna().sum()}."
            )

    def add_date_and_vendor(self, dataframe):
        """
        This function will add date and Vendor name column in the input dataframe

        Args:
            dataframe (pandas dataframe): Input DataFrame with no date and Vendor
            columns
        Returns:
            dataframe (pandas dataframe): DataFrame with date and Vendor
            columns
        """
        dataframe["Date"] = pd.Series([self.date] * len(dataframe))
        dataframe["VendorName"] = pd.Series([self.vendor_name] * len(dataframe))
        return dataframe

    def process_data(self):
        """
        This function executes all the other function of this class
        in the required sequential order

        Returns:
            dataframe_post_processed (pandas dataframe): The post processed DataFrame or 
            the final output
        """
        datframe_processed_with_report_number = self.add_report_number(self.dataframe_pre_processed)

        transformed_dataframe = self.transform_values(datframe_processed_with_report_number)

         if 'cut' not in transformed_dataframe.columns:
            # Create the 'cut' column and set its value to 'ex' for each row
            transformed_dataframe['cut'] = 'ex'

        self.log_missing_target_columns(
            transformed_dataframe, self.target_columns
        )

        transformed_dataframe_with_link_column = self.add_links_and_extra_columns(
            transformed_dataframe, self.link_columns_name
        )

        dataframe_post_processed = self.add_date_and_vendor(transformed_dataframe_with_link_column)
        
        self.log_missing_report_no(dataframe_post_processed)

        self.logger.info("-" * 75)
        self.logger.info(dataframe_post_processed.head(5))
        self.logger.info("-" * 75)
        return dataframe_post_processed

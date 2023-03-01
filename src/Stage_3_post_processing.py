import pandas as pd
from src import StandardValueConverterAndCalculation


class PostProcessingData:
    def __init__(
        self,
        df_pre_processed,
        df_cleaned,
        report_no_from_link,
        magic_numbers,
        prob_dict,
        link_columns_name,
        remaining_columns_df,
        target_columns,
        Date,
        test_file_name,
        logger,
    ):
        self.df_pre_processed = df_pre_processed
        self.df_cleaned = df_cleaned
        self.report_no_from_link = report_no_from_link
        self.magic_numbers = magic_numbers
        self.prob_dict = prob_dict
        self.link_columns_name = link_columns_name
        self.remaining_columns_df = remaining_columns_df
        self.target_columns = target_columns
        self.Date = Date
        self.test_file_name = test_file_name
        self.logger = logger

    def add_report_number(self, df):
        """
        This function will create a new column called 'report no from link'
        to store the report number obtained from the link, as well as initialise
        the column'report no' with values. If we are unable to extract the report
        number from the sheet, None will be assigned; otherwise, the extracted
        values will be assigned.
        """
        df["report_no_from_link"] = self.report_no_from_link
        df["report_no"] = df["report_no"] if "report_no" in df else None
        return df

    def transform_values(self, df):
        """
        This function will create object for StandardValueConverterAndCalculation class
        which will do the following -:
            1. Convert the non-standard values to standard values. Eg-: "RND" to "ROUND"
            2. Extract the length, width and depth from this format "2*7*8" and then
               calculate depth% and ratio
            3. Calculate the price-related columns if required amount of data is already
               available to calculate them
            4. Combine the 'report_no_from_link' and 'report_no' to get final report_no
        """
        fetched_columns = list(df.columns)
        value_transformer = StandardValueConverterAndCalculation.PostProcessing(
            fetched_columns, df, self.magic_numbers, self.prob_dict
        )
        df = value_transformer.process()
        return df

    def log_missing_target_columns(self, df, target_columns):
        target_columns += ["ratio", "depth %"]
        self.logger.info("-" * 75)
        self.logger.info(f"Not able to detect {set(target_columns) - set(df.columns)}")
        return df

    def add_links(self, df, link_columns_name, remaining_columns_df):
        """
        This function will simply add link columns
        in our output dataframe
        """
        df[link_columns_name] = self.df_cleaned[link_columns_name]
        df = pd.concat([df, self.remaining_columns_df], axis=1)
        return df

    def log_missing_report_no(self, df):
        if "report_no" in df.columns:
            self.logger.info(
                f"The total number of columns without a report number is {df['report_no'].isna().sum()}."
            )
        return df

    def add_date_and_vendor(self, df, Date, test_file_name):
        """
        This function will add Date and Vendor to the output column
        """
        df["Date"] = pd.Series([self.Date] * len(df))
        df["Vendor"] = pd.Series([self.test_file_name] * len(df))
        return df

    def process_data(self):
        """
        This function will just run all the above function to do the task
        """
        df_processed = self.add_report_number(self.df_pre_processed)
        df_processed = self.transform_values(df_processed)
        df_processed = self.log_missing_target_columns(
            df_processed, self.target_columns
        )
        df_processed = self.add_links(
            df_processed, self.link_columns_name, self.remaining_columns_df
        )
        df_processed = self.add_date_and_vendor(
            df_processed, self.Date, self.test_file_name
        )
        df_processed = self.log_missing_report_no(df_processed)

        self.logger.info("-" * 75)
        self.logger.info(df_processed.head(5))
        self.logger.info("-" * 75)
        return df_processed
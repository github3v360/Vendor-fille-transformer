'''
This file contains the class 'DataProcessor' 
which will perform all the stage 2 tasks
'''

import pandas as pd
from src.utils import (
    common_utils,
    column_name_utils,
    column_value_utils,
    score_modifier,
)

class DataProcessor:
    '''
    This class includes all of the functionality required to use the statistical model
    to extract the target columns from the data.
    '''
    def __init__(
        self, dataframe_cleaned, logger, link_columns_name, count_of_rows, date, vendor_name
    ):
        '''
        Initializes the instance based on the attributes.

        Args:
            dataframe_cleaned (pandas dataframe): cleaned dataframe given by the stage 1

            count_of_rows (int): The total number of rows present in the dataframe_cleaned

            link_columns_name(list): list of links column name

            date: date (exact description of this date will be updated later)

            vendor_name: Name of the vendor

            logger: Python's logger to log the Info, Errors and Exceptions

        '''
        self.dataframe_cleaned = dataframe_cleaned
        self.logger = logger
        self.link_columns_name = link_columns_name
        self.count_of_rows = count_of_rows
        self.date = date
        self.vendor_name = vendor_name

        self.target_columns = [
            "clarity",
            "carat",
            "color",
            "shape",
            "fluorescent",
            "raprate",
            "cut",
            "polish",
            "symmetry",
            "table",
            "length",
            "width",
            "depth",
            "price per carat",
            "discount",
            "total",
            "rap price total",
            "comments",
            "report_no",
        ]

        self.prob_dict = common_utils.initialize_prob_dict(self.target_columns)

        self.magic_numbers = common_utils.get_magic_numbers()

    def get_column_probability(
        self,
        cur_target_column,
        cur_dataframe_cleaned_column_name,
        cur_dataframe_cleaned_column_unique_values,
        cur_target_col_std_names,
        cur_target_col_unique_vals,
    ):
        """
        This function will calculate the probability of the current column
        belonging to the current (particular) target column on the basis of
        current column header name and its values 

        final_similarity_score = (sim_score_from_col_name * w1)
                                 + (sim_score_from_col_val * w2)
        where,
            sim_score_from_col_name = similarity score calculated from the column name
            sim_score_from_col_val = similarity score calculated from the column values
            w1 = weight given to the sim_score_from_col_name
            w2 = weight given to the sim_score_from_col_val
        
        Args:
            cur_target_column (string): Name of the current target column 

            cur_dataframe_cleaned_column_name (string): Name of the column for which we
            will compute the probability that it belongs to cur target column

            cur_dataframe_cleaned_column_unique_values (list): List of 
            "cur_dataframe_cleaned_column_name" unique values

            cur_target_col_std_names (list): List of all standard names of cur_target_column

            cur_target_col_unique_vals (list): List of all possible values of
            cur_target_column

        Returns:
            final_similarity_score (float): final similarity(probability) score
            of the cur_dataframe_cleaned_column_name belonging to the cur_target_column

        """
        # getting sim_score_from_col_name
        sim_score_from_cur_col_name = column_name_utils.similarity_score_from_col_name(
            cur_dataframe_cleaned_column_name, cur_target_col_std_names
        )

        # getting sim_score_from_col_val
        similarity_score_of_value = column_value_utils.similarity_score_from_col_values(
            self.count_of_rows,
            cur_dataframe_cleaned_column_unique_values,
            cur_target_col_unique_vals,
            cur_target_column,
        )

        # this will calculate final_similarity_score on the basis of
        # the formula specified in above docstring
        final_similarity_score = score_modifier.merge_similarity_score(
            sim_score_from_cur_col_name,
            similarity_score_of_value,
            cur_target_column,
            self.magic_numbers,
        )

        return final_similarity_score

    def get_remaining_column(self):
        """
        This function will get the remaining columns which were not required 
        to fetch. These remaining column will be stored in
        a single column in a key-value format

        Returns:
            remaining_columns_dataframe(pandas dataframe): DataFrame which 
            contains all the extra (redundant) columns in the form of dictionary
        """
        cols = self.dataframe_cleaned.columns
        self.remaining_columns_dataframe = pd.DataFrame()
        list_of_dicts = []
        for _, row in self.dataframe_cleaned.iterrows():
            d = {}
            for col in cols:
                if type(col) != str:
                    continue
                d[col] = row[col]
            list_of_dicts.append(d)

        self.remaining_columns_dataframe["Extra Column"] = list_of_dicts
        return self.remaining_columns_dataframe

    def get_current_column_unique_values(self, dataframe_cleaned, cur_dataframe_cleaned_column_name):
        """
        This function will used by "Iterate_And_Get_Desired_Column_By_Probability"
        function to get the values of the current column and also get the number 
        of rows (excluding None row of the current column).

        Args:
            dataframe_cleaned(pandas dataframe): cleaned dataframe given by the stage 1
            
            cur_dataframe_cleaned_column_name (string): Name of the column in dataframe_cleaned 
            for which unique values will be extracted and the number of rows for that
            column will be calculated as mentioned above.
        
        Returns:
            cur_dataframe_cleaned_column_unique_values (list): cur_dataframe_cleaned_column_name unique
            values

            cur_dataframe_cleaned_column_name (string): cur_dataframe_cleaned_column_name in lower case
        """

        cur_dataframe_cleaned_column_unique_values = list(
            self.dataframe_cleaned[cur_dataframe_cleaned_column_name].unique()
        )
        cur_dataframe_cleaned_column_unique_values = common_utils.assure_data_type(
            cur_dataframe_cleaned_column_unique_values
        )

        # Getting the total row excluding the row with None values
        total_none_values = dataframe_cleaned[cur_dataframe_cleaned_column_name].isna().sum()
        if total_none_values == 0:
            self.count_of_rows = dataframe_cleaned.shape[0]
        else:
            self.count_of_rows = dataframe_cleaned.shape[0] - total_none_values + 1

        cur_dataframe_cleaned_column_name = cur_dataframe_cleaned_column_name.lower()

        return cur_dataframe_cleaned_column_unique_values, cur_dataframe_cleaned_column_name

    def Iterate_And_Get_Desired_Column_By_Probability(self):
        '''
        This function will iterate to each column in dataframe(given by stage 1) and
        gives the probability of each column belonging to a particular target column.
        The aforementioned procedure will be done for each target column

        Returns:
            dataframe_pre_processed (pandas dataframe): Pre-processed dataframe in which
            all the target columns are fetched

            magic_number(dictionary): Dictionary cotaning the magic numbers 

            remaining_columns_dataframe(pandas dataframe): DataFrame which 
            contains all the extra (redundant) columns in the form of dictionary
        '''

        # Initializing the empty DataFrame to store output of pre-processed data
        dataframe_pre_processed = pd.DataFrame()

        # For each target column, fetch the right column and save it in dataframe_pre_processed
        for cur_target_column in self.target_columns:

            # Get a list of the column names in the dataframe_cleaned
            dataframe_cleaned_columns_name = list(self.dataframe_cleaned.columns)

            # Getting the other standard names for the current target column (cur_target_column)
            cur_target_col_std_names = column_name_utils.get_standard_names(
                cur_target_column, self.logger
            )

            # Set the probability of each column in dataframe_cleaned belonging to the current target column (cur_target_column) to -1.
            probs = [-1] * len(dataframe_cleaned_columns_name)

            # This will get the current target column (cur_target_column) unique values
            cur_target_col_unique_vals = (
                column_value_utils.get_target_column_unique_values(
                    cur_target_column, self.logger
                )
            )

            # Iteratively obtain the probability of all columns in cleaned dataframe (dataframe_cleaned) belonging to the
            # current target column (cur_target_column).
            for idx, cur_dataframe_cleaned_column_name in enumerate(dataframe_cleaned_columns_name):

                # Getting the current column of cleaned dataframe unique values
                try:
                    (
                        cur_dataframe_cleaned_column_unique_values,
                        cur_dataframe_cleaned_column_name,
                    ) = self.get_current_column_unique_values(
                        self.dataframe_cleaned, cur_dataframe_cleaned_column_name
                    )
                except:
                    continue

                # storing the final similarity score (probability)
                # of the current column in the cleaned dataframe (dataframe_cleaned)
                probs[idx] = self.get_column_probability(
                    cur_target_column,
                    cur_dataframe_cleaned_column_name,
                    cur_dataframe_cleaned_column_unique_values,
                    cur_target_col_std_names,
                    cur_target_col_unique_vals,
                )

            # Getting the column name from the cleaned_dataframe with highest probability (similarity) score
            # to current target column (cur_target_column)
            predicted_column, prob = common_utils.get_highest_prob_column(
                probs, dataframe_cleaned_columns_name
            )

            # update prob dict
            self.prob_dict[cur_target_column] = prob

            # Adding column of cleaned_dataframe with highest probability(similarity) score to dataframe_pre_processed on if the probability is more than 65%
            p = round(prob, 3)
            self.logger.info(
                f"'{cur_target_column}' is present as '{predicted_column}' with probability {round(p,3)}"
            )
            if prob > self.magic_numbers["threshold_for_selection"]:
                dataframe_pre_processed[cur_target_column] = self.dataframe_cleaned[predicted_column]

                # Dropping the column with highest probability (similarity) score from cleaned_dataframe, since we do not need to iterate over that column again
                if cur_target_column not in ["length", "width", "depth"]:
                    self.dataframe_cleaned = self.dataframe_cleaned.drop(columns=predicted_column)

        remaining_columns_dataframe = self.get_remaining_column()

        return dataframe_pre_processed, self.magic_numbers, remaining_columns_dataframe

    def Probability_Based_DataExtraction(self):
        """
        This function will run all the required function to fetch the 
        target columns from the dataframe(given by the Stage 1)

        Returns:
            dataframe_pre_processed (pandas dataframe): Pre-processed dataframe in which
            all the target columns are fetched

            report_no_from_link (list): report number extracted from the link

            magic_number(dictionary): Dictionary cotaning the magic numbers 

            prob_dict(dictionary): A probability dictionary containing the probability 
            that a target column was chosen from the data.

            remaining_columns_dataframe(pandas dataframe): DataFrame which 
            contains all the extra (redundant) columns in the form of dictionary
            
            target_columns(list): A list of the name of all the target columns
        """

        # This will store the report umber whhich were extracted from the link in stage 1
        # in to the list "self.report_no_from_link" and also upadate self.link_columns_name
        # accordingly
        (
            self.report_no_from_link,
            self.link_columns_name,
        ) = common_utils.get_report_no_extracted_from_link(
            self.dataframe_cleaned, self.logger, self.link_columns_name
        )

        (
            self.dataframe_pre_processed,
            self.magic_numbers,
            self.remaining_columns_dataframe,
        ) = self.Iterate_And_Get_Desired_Column_By_Probability()

        return (
            self.dataframe_pre_processed,
            self.report_no_from_link,
            self.magic_numbers,
            self.prob_dict,
            self.remaining_columns_dataframe,
            self.target_columns,
        )
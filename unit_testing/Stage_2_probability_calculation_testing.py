import unittest
import pandas as pd
import logging
import pandas as pd
from src.utils import (
    common_utils,
    column_name_utils,
    column_value_utils,
    score_modifier,
)
from src.Stage_2_probability_calculation import DataProcessor
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# setting up the logger for test purpose
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_path = "running_logs/test.log"
formatter = logging.Formatter("Time: %(asctime)s   :    %(message)s")
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class TestStage1DataCleaningAndExtraction(unittest.TestCase):
    def setUp(self):
        """
        we will use the Stage_2_testing_file.csv
        for all our testing
        """

        self.df_cleaned = pd.read_csv(
            "artifacts/files_for_unit_testing/Stage_2_testing_file.csv"
        )
        self.logger = logger
        self.link_columns_name = ["Image_link", "Cert._link", "report_no"]
        self.count_of_rows = self.df_cleaned.shape[0]
        self.Date = "19/02/2023"
        self.test_file_name = "Vendor_70"
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
        self.cur_df_cleaned_column_name = "carat"
        self.processor = DataProcessor(
            self.df_cleaned,
            self.logger,
            self.link_columns_name,
            self.count_of_rows,
            self.Date,
            self.test_file_name,
        )

    def test_Probability_Based_DataExtraction(self):
        (
            df_pre_processed,
            report_no_from_link,
            magic_numbers,
            prob_dict,
            remaining_columns_df,
            target_columns,
        ) = self.processor.Probability_Based_DataExtraction()
        pass

    def test_get_column_probability(self):
        """
        Here we test the final_similarity_score of current iterated
        column belonging the target columns
        """
        # We will calculate probailityof the Cla. column in self.df_cleaned
        # belonging to 'clarity'
        cur_target_column = "clarity"

        (
            cur_df_cleaned_column_unique_values,
            cur_df_cleaned_column_name,
        ) = self.processor.get_current_column_unique_values(self.df_cleaned, "Cla.")
        cur_target_col_std_names = column_name_utils.get_standard_names(
            cur_target_column, self.logger
        )
        cur_target_col_unique_vals = column_value_utils.get_target_column_unique_values(
            cur_target_column, self.logger
        )

        final_similarity_score = self.processor.get_column_probability(
            cur_target_column="clarity",
            cur_dataframe_cleaned_column_name=cur_df_cleaned_column_name,
            cur_dataframe_cleaned_column_unique_values=cur_df_cleaned_column_unique_values,
            cur_target_col_std_names=["clarity", "cls"],
            cur_target_col_unique_vals=cur_target_col_unique_vals,
        )

        self.assertEqual(final_similarity_score, 0.75)

    def test_get_current_column_unique_values(self):

        """
        Here we will test the following -:
            1. Expected values of current column
            2. cur_df_cleaned_column_name converted to lowercase or not
        """

        # For all three test we will use the 'Shape' column form 'Stage_2_testing_file.csv'

        (
            cur_df_cleaned_column_unique_values,
            cur_df_cleaned_column_name,
        ) = self.processor.get_current_column_unique_values(self.df_cleaned, "Shape")

        # Test 1
        expected_shape_values = ["BR", "ROUND", None]

        for idx, cur_val in enumerate(cur_df_cleaned_column_unique_values):

            if pd.isna(cur_val):
                cur_val = None

            self.assertEqual(cur_val, expected_shape_values[idx])

        # Test 2
        self.assertEquals(cur_df_cleaned_column_name, "shape")

    def test_Iterate_And_Get_Desired_Column_By_Probability(self):
        """
        We will test the following
            1. we will test what are the extracted columns
            2. we will test what are the extra columns we encountered
                extra columns are extracted links, Sr.No etc.
        """
        (
            df_processed,
            magic_numbers,
            remaining_columns_df,
        ) = self.processor.Iterate_And_Get_Desired_Column_By_Probability()

        # test 1
        expected_extracted_columns = [
            "clarity",
            "carat",
            "shape",
            "fluorescent",
            "raprate",
            "cut",
            "polish",
            "symmetry",
            "discount",
            "report_no",
        ]

        self.assertEqual(list(df_processed.columns), expected_extracted_columns)

        # test 2
        expected_extra_columns = [
            "Image",
            "Amount",
            "Cert.",
            "Image_link",
            "Cert._link",
        ]
        self.assertAlmostEqual(
            expected_extra_columns,
            list(remaining_columns_df["Extra Column"].iloc[0].keys()),
        )


if __name__ == "__main__":
    unittest.main()

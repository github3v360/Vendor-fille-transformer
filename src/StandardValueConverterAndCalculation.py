'''
This file contains class for performing post processing with column values in dataframes.
'''
import pickle
import os
from src.utils import post_processing_utils,common_utils,generate_report_number
import time
import math
import numpy as np

class PostProcessing:
    """
    Class performs post processing of extracted data. It starts with 'process' functions and 
    then iteratively calls other functions.
    It calculates final values for:
    1) Measurement Column
    2) All Price Columns
    3) Report No.
    4) Shape ,Fluoroscent and Cut

    Args:
        fetched_columns: Predicted Columns (list)
        df_pre_processed: Pre Processed Dataframe (DataFrame)
        magic_numbers: Required weights (dict)
        prob_dict: Predicted Probablities (dict)
        logger: Python's logger to log the Info, Errors and Exceptions
    Returns:
        df_pre_processed : Post Processed Dataframe (DataFrame)

    """
    def __init__(self, fetched_columns, df_pre_processed, magic_numbers, prob_dict, logger):
        self.fetched_columns = fetched_columns
        self.df_pre_processed = df_pre_processed
        self.magic_numbers = magic_numbers
        self.prob_dict = prob_dict
        self.logger = logger

    def cal_measurement_columns(self):
        """
        Extracts the length, width and depth from the provided string 
        in the format "2*7*8" or "7*8".
        It calculates the 'depth percentage' and 'ratio'.

        Returns:
            pre-processed DataFrame with transformed measurement columns 
            and calculated ratio and depth percentage. (Datframe)

        """
        # Corecting the length, width and depth column
        measurement_columns = ["length", "width", "depth"]

        if set(measurement_columns).issubset(set(self.fetched_columns)):
            flag = True
            try:
                _ = float(self.df_pre_processed["length"].iloc[0])
                flag = False
            except:
                pass

            if flag:
                (
                    self.df_pre_processed["length"],
                    self.df_pre_processed["width"],
                    self.df_pre_processed["depth"],
                ) = zip(
                    *self.df_pre_processed.apply(
                        lambda x: post_processing_utils.transform_measurement_column(
                            x["length"], x["depth"]
                        ),
                        axis=1,
                    )
                )
            self.df_pre_processed["length"] = self.df_pre_processed["length"].astype(
                float
            )
            self.df_pre_processed["width"] = self.df_pre_processed["width"].astype(
                float
            )
            self.df_pre_processed["depth"] = self.df_pre_processed["depth"].astype(
                float
            )

            # Calculate the ratio and depth column
            self.df_pre_processed["ratio"] = round(
                self.df_pre_processed["length"] / self.df_pre_processed["width"], 2
            )
            self.df_pre_processed["depth %"] = round(
                (self.df_pre_processed["depth"] / self.df_pre_processed["width"]) * 100,
                2,
            )
        return self.df_pre_processed

    def convert_to_integer(self,value):
        try:
            float_value = float(value)
            if math.isnan(float_value):
                return None  # Handle NaN values as needed
            else:
                return int(math.ceil(float_value))
        except (ValueError, TypeError):
            return int(value)
            
    def cal_price_columns(self):
        """
        This function will calculate the "price per carat","discount" and "total"
        only if 'carat','raprate' and one of the aforementioned column is given.
        Total Columns:
        1) Carat
        2) Raprate
        3) Price per carat
        4) Discount
        5) Total
        6) RapTotal

        Returns:
            post-processed DataFrame with additional price columns 
            
        """
        price_columns = ["carat", "raprate", "price per carat", "discount", "total"]

        if set(price_columns[:2]).issubset(set(self.fetched_columns)) and any(
            [item in self.fetched_columns for item in price_columns[2:]]
        ):
            # Now Calculating and correcting the price related column
            price_list = price_columns[2:]
            self.df_pre_processed.dropna(subset=['raprate'], inplace=True)
            self.df_pre_processed["raprate"] = self.df_pre_processed["raprate"].apply(self.convert_to_integer)
            self.df_pre_processed["carat"] = self.df_pre_processed["carat"].astype(
                float
            )
            self.df_pre_processed["rap price total"] = (
                self.df_pre_processed["raprate"] * self.df_pre_processed["carat"]
            )
            #new, converting to int
            self.df_pre_processed["rap price total"] = self.df_pre_processed["rap price total"].apply(self.convert_to_integer)

            max_prob = -1
            price_name = None

            for cur_price_name in price_list:
                try:
                    cur_prob = self.prob_dict[cur_price_name]
                except:
                    continue

                if cur_prob > max_prob:
                    max_prob = cur_prob
                    price_name = cur_price_name
            if price_name == "discount":
                self.df_pre_processed["discount"] = self.df_pre_processed[
                    "discount"
                ].apply(post_processing_utils.transform_discount_column)

                self.df_pre_processed["price per carat"] = (
                    self.df_pre_processed["raprate"] * 
                    (1 - (self.df_pre_processed["discount"] / 100)))

                self.df_pre_processed["total"] = (
                    self.df_pre_processed["price per carat"]
                    * self.df_pre_processed["carat"]
                )
            elif price_name == "price per carat":
                self.df_pre_processed["discount"] = ((
                    1
                    - (
                        self.df_pre_processed["price per carat"]
                        / self.df_pre_processed["raprate"]
                    )
                ) * 100)
                self.df_pre_processed["total"] = (
                    self.df_pre_processed["price per carat"]
                    * self.df_pre_processed["carat"]
                )
            else:
                self.df_pre_processed["price per carat"] = (
                    self.df_pre_processed["total"] / self.df_pre_processed["carat"]
                )
                self.df_pre_processed["discount"] = (
                    1
                    - (
                        self.df_pre_processed["price per carat"]
                        / self.df_pre_processed["raprate"]
                    )
                ) * 100
            self.df_pre_processed["price per carat"] = self.df_pre_processed["price per carat"].replace([np.inf, -np.inf], np.nan)
            self.df_pre_processed["total"] = self.df_pre_processed["total"].replace([np.inf, -np.inf], np.nan)
            self.df_pre_processed["rap price total"] = self.df_pre_processed["rap price total"].replace([np.inf, -np.inf], np.nan)
            self.df_pre_processed["price per carat"] = self.df_pre_processed["price per carat"].replace([np.inf, -np.inf], np.nan)


            #new, converted to int
            self.df_pre_processed["total"] = self.df_pre_processed["total"].apply(self.convert_to_integer)
            self.df_pre_processed["price per carat"] = self.df_pre_processed["price per carat"].apply(self.convert_to_integer)

        return self.df_pre_processed

    
    def process(self):
        start = time.time()
        """
        This function will tranform shape, fluorescent and cut column.
        It will transform their non-standard value to a standard value.
        It will call "cal_measurement_columns" and "cal_price_columns"
        It will combine the 'report_no_from_link' column and 'report_no' column
        to get final 'report_no' column

        Returns:
            pre-processed DataFrame with additional columns 
        """
        
        if "shape" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("shape")
            self.df_pre_processed["shape"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["shape"], self.magic_numbers,"shape", target_column_dict, None),
                axis=1,
            )
        
        if "fluorescent" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("fluorescent")
            self.df_pre_processed["fluorescent"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["fluorescent"], self.magic_numbers, "fluorescent", target_column_dict, None),
                axis=1,
            )

        self.df_pre_processed = self.cal_measurement_columns()

        if "cut" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("cut")
            self.df_pre_processed["cut"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["cut"], self.magic_numbers, "cut", target_column_dict, None),
                axis=1,
            )
        
        if "polish" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("polish")
            self.df_pre_processed["polish"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["polish"], self.magic_numbers, "polish", target_column_dict, None),
                axis=1,
            )
        
        if "symmetry" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("symmetry")
            self.df_pre_processed["symmetry"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["symmetry"], self.magic_numbers, "symmetry", target_column_dict, None),
                axis=1,
            )

        if "color" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("color")
            self.df_pre_processed["color"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["color"], self.magic_numbers, "color", target_column_dict, None),
                axis=1,
            )

        if "clarity" in self.fetched_columns:
            target_column_dict= common_utils.load_pickle_files_for_single_column("clarity")
            self.df_pre_processed["clarity"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["clarity"], self.magic_numbers, "clarity", target_column_dict, None),
                axis=1,
            )

        self.df_pre_processed = self.cal_price_columns()

        self.df_pre_processed["report_no"] = self.df_pre_processed.apply(
            lambda x: post_processing_utils.transform_report_no_column(
                x["report_no"], x["report_no_from_link"]
            ),
            axis=1,
        )
        file_destination_list = []
        test_data_dir = "artifacts/pickle_files"
        test_file_names = os.listdir(test_data_dir)
        for test_file_name in test_file_names:
            file_destination_list.append(os.path.join(test_data_dir,test_file_name))
        
        # Load shape dictionary from pickle file
        # list_of_dictionaries = common_utils.load_pickle_files(file_destination_list)
        # clarity_map=  {}
        # color_map = {}
        # cut_map = {}
        # fluorescent_map = {}
        # shape_map = {}

        # for dictionary in list_of_dictionaries:
        #     if 'color' in dictionary:
        #         color_map = dictionary['color']
        #     elif 'shape' in dictionary:
        #         shape_map = dictionary['shape']
        #     elif 'clarity' in dictionary:
        #         clarity_map = dictionary['clarity']
        #     elif 'cut' in dictionary:
        #         cut_map = dictionary['cut']
        #     elif 'fluorescent' in dictionary:
        #         fluorescent_map = dictionary['fluorescent']
        #     elif 'polish' in dictionary:
        #         polish_map = dictionary['polish']
        #     elif 'symmetry' in dictionary:
        #         symmetry_map = dictionary['symmetry']
            
        start_time_to_generate_report_no = time.time()
        required_column = ["report_no","clarity","color","fluorescent","shape","carat","cut","polish","symmetry","length","width","depth"]
        temporary_columns = []
        for col in required_column:
            if col not in self.df_pre_processed.columns:
                self.df_pre_processed.loc[:,col] = 'NOT PRESENT'
                temporary_columns.append(col)

        # self.df_pre_processed["GeneratedReportNo"] = self.df_pre_processed.apply(
        #     lambda x: post_processing_utils.generate_report_no_column(
        #         x["report_no"], x['clarity'], x['color'], x['fluorescent'], x['shape'],x['carat'],x['cut'],x['polish'],x['symmetry'],
        #         clarity_map,color_map, shape_map, cut_map, fluorescent_map,polish_map,symmetry_map
        #     ),
        #     axis=1,
        # )weight, shape, color, clarity, fluor, cut, polish, sym, mes1, mes2, mes3

        self.df_pre_processed["GeneratedReportNo"] = self.df_pre_processed.apply(
            lambda x: generate_report_number.generate_id(
                x['carat'], x['shape'], x['color'], x['clarity'],x['fluorescent'],x['cut'],x['polish'],x['symmetry'],
                x['length'],x['width'],x['depth']

            ),
            axis=1,
        )

        total_time_taken_to_generate_report_no = time.time() - start_time_to_generate_report_no

        self.logger.info(f"Time taken to generate report number {total_time_taken_to_generate_report_no}")

        temporary_columns.append("report_no_from_link")
        self.df_pre_processed.drop(columns=temporary_columns, axis=1, inplace=True)
        print("Deleted columns")
        print(temporary_columns)
        end = time.time()
        self.logger.info("Total time taken in post processing function: "+str(end-start))
        return self.df_pre_processed
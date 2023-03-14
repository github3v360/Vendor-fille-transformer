'''
This file contains class for performing post processing with column values in dataframes.
'''
from src.utils import post_processing_utils
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
    Returns:
        df_pre_processed : Post Processed Dataframe (DataFrame)

    """
    def __init__(self, fetched_columns, df_pre_processed, magic_numbers, prob_dict):
        self.fetched_columns = fetched_columns
        self.df_pre_processed = df_pre_processed
        self.magic_numbers = magic_numbers
        self.prob_dict = prob_dict

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
                _ = float(self.df_pre_processed["length"].iloc[20])
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
            self.df_pre_processed["raprate"] = self.df_pre_processed["raprate"].astype(
                float
            )
            self.df_pre_processed["carat"] = self.df_pre_processed["carat"].astype(
                float
            )
            self.df_pre_processed["rap price total"] = (
                self.df_pre_processed["raprate"] * self.df_pre_processed["carat"]
            )

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
                self.df_pre_processed["price per carat"] = self.df_pre_processed[
                    "raprate"
                ] * (1 - (self.df_pre_processed["discount"] / 100))
                self.df_pre_processed["total"] = (
                    self.df_pre_processed["price per carat"]
                    * self.df_pre_processed["carat"]
                )
            elif price_name == "price per carat":
                self.df_pre_processed["discount"] = (
                    1
                    - (
                        self.df_pre_processed["price per carat"]
                        / self.df_pre_processed["raprate"]
                    )
                ) * 100
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

        # self.df_pre_processed["rap total"] = (
        #             self.df_pre_processed["raprate"]
        #             * self.df_pre_processed["carat"]
        #         )
        return self.df_pre_processed

    def process(self):

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
            self.df_pre_processed["shape"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["shape"], self.magic_numbers, "shape"
                ),
                axis=1,
            )

        if "fluorescent" in self.fetched_columns:
            self.df_pre_processed["fluorescent"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["fluorescent"], self.magic_numbers, "fluor"
                ),
                axis=1,
            )

        self.df_pre_processed = self.cal_measurement_columns()

        if "cut" in self.fetched_columns:
            self.df_pre_processed["cut"] = self.df_pre_processed.apply(
                lambda x: post_processing_utils.transform_column(
                    x["cut"], self.magic_numbers, "cut"
                ),
                axis=1,
            )

        self.df_pre_processed = self.cal_price_columns()

        self.df_pre_processed["report_no"] = self.df_pre_processed.apply(
            lambda x: post_processing_utils.transform_report_no_column(
                x["report_no"], x["report_no_from_link"]
            ),
            axis=1,
        )
        self.df_pre_processed.drop("report_no_from_link", axis=1, inplace=True)
        return self.df_pre_processed

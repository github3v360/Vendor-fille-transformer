import pandas as pd
from src.utils import post_processing_utils


class PostProcessing:
    def __init__(self, fetched_columns, df_pre_processed, magic_numbers, prob_dict):
        self.fetched_columns = fetched_columns
        self.df_pre_processed = df_pre_processed
        self.magic_numbers = magic_numbers
        self.prob_dict = prob_dict

    def cal_measurement_columns(self):
        """
        Extract the length, width and depth from this string of this  format "2*7*8"
        and also this format "7*8" and then
        calculate depth% and ratio.
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
        only if 'carat','raprate' and one of the aforementioned column is given
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

        return self.df_pre_processed

    def process(self):

        """
        This function will tranform the shape, fluorescent and cut column
        where it will transform their non-standard value to standard values.
        It will also all the above two functions "cal_measurement_columns" 
        and "cal_price_columns"
        Finally it will combine the 'report_no_from_link' column and 'report_no' column
        to get final 'report_no' column
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

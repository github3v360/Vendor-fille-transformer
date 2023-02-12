from src.utils import data_cleaner
from src import hyperlink_extraction

class CleanDataAndExtractLink:
    def __init__(self, df, ws, logger):
        self.df = df
        self.ws = ws
        self.logger = logger

    def process(self):
        df_corrected_headers, correct_row_idx = data_cleaner.correct_df_headers(self.df)
        df_with_links, link_columns_name = hyperlink_extraction.add_hyperlink_columns(df_corrected_headers, self.ws, correct_row_idx)
        df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)

        return df_cleaned, link_columns_name
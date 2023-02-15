from src.utils import data_cleaner
from src import hyperlink_extraction

class CleanDataAndExtractLink:
    def __init__(self, df, ws, logger):
        self.df = df
        self.ws = ws
        self.logger = logger

    def process(self):

        # Correcting the DataFrame Headers
        df_corrected_headers, correct_row_idx = data_cleaner.correct_df_headers(self.df)

        # Extracting the hyperlink and report number from the link
        hyperlink_extractor = hyperlink_extraction.HyperlinkExtractor(self.ws, correct_row_idx,df_corrected_headers)
        df_with_links, link_columns_name = hyperlink_extractor.add_hyperlink_columns()

        # Dropping Empty Rows and columns
        df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)

        return df_cleaned, link_columns_name
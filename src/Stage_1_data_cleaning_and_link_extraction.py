from src.utils import data_cleaner
from src import hyperlink_extraction

# This function will be put in different file
def clean_data_and_extract_link(df, ws, logger):

    # Getting the correct headers
    df_corrected_headers, correct_row_idx = data_cleaner.correct_df_headers(df)

    # Extracting link and extractiong report number from the link
    df_with_links, link_columns_name = hyperlink_extraction.add_hyperlink_columns(df_corrected_headers, ws, correct_row_idx)

    # Dropping empty column and rows
    df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)

    return df_cleaned, link_columns_name
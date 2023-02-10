from src import post_processing_caller
import pandas as pd

def post_processing_data(df_pre_processed, df_cleaned, report_no_from_link, magic_numbers,
                         prob_dict, link_columns_name, remaining_columns_df,
                         target_columns, Date, test_file_name,logger):
    def add_report_number(df):
        df['report_no_from_link'] = report_no_from_link
        df['report_no'] = df['report_no'] if 'report_no' in df else None
        return df

    def transform_values(df):
        fetched_columns = list(df.columns)
        df = post_processing_caller.post_processing_function(fetched_columns, df, magic_numbers, prob_dict)
        return df

    def log_missing_target_columns(df, target_columns):
        target_columns += ['ratio', 'depth %']
        logger.info("-" * 75)
        logger.info(f"Not able to detect {set(target_columns) - set(df.columns)}")
        return df

    def add_links(df, link_columns_name, remaining_columns_df):
        df[link_columns_name] = df_cleaned[link_columns_name]
        df = pd.concat([df, remaining_columns_df], axis=1)
        return df

    def log_missing_report_no(df):
        if 'report_no' in df.columns:
            logger.info(f"The total number of columns without a report number is {df['report_no'].isna().sum()}.")
        return df

    def add_date_and_vendor(df, Date, test_file_name):
        df['Date'] = pd.Series([Date] * len(df))
        df['Vendor'] = pd.Series([test_file_name] * len(df))
        return df

    df_processed = add_report_number(df_pre_processed)
    df_processed = transform_values(df_processed)
    df_processed = log_missing_target_columns(df_processed, target_columns)
    df_processed = add_links(df_processed, link_columns_name, remaining_columns_df)
    df_processed = log_missing_report_no(df_processed)
    df_processed = add_date_and_vendor(df_processed, Date, test_file_name)

    logger.info("-" * 75)
    logger.info(df_processed.head(5))
    logger.info("-" * 75)
    
    return df_processed
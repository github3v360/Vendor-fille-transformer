# Importing Required Libraries
import logging
from src.utils import data_cleaner, common_utils, column_name_utils, column_value_utils, score_modifier, post_processing_utils, post_processing_caller
import pandas as pd
import os
from src import hyperlink_extraction


def extract_from_single_sheet(df,ws,debug,logger):
    
    logger.info("-" * 75)
    # ==== Stage 1 (Cleaning the Data) ====
    df_corrected_headers,correct_row_idx = data_cleaner.correct_df_headers(df)
    df_with_links, link_columns_name = hyperlink_extraction.add_hyperlink_columns(df_corrected_headers,ws,correct_row_idx)
    df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)

    # Dropping unwanted columns
    df.drop(columns=df.columns[0], axis=1,  inplace=True)

    # Finding total count of rows
    count_of_rows = df.shape[0]

    # ==== Stage 2 (Processing the Data) ====

    # Declaring the target column (required columns)
    target_columns = ['clarity','carat','color','shape',"fluorescent","raprate",'cut','polish',"symmetry","table","length","width","depth",
    "price per carat","discount","total","rap price total","comments"]

    if 'report_no' not in df_with_links.columns:
        logger.info("Report No. not found in Link")
        target_columns.append('report_no')


    # Initializing dictionary to store the probabilty of target columns
    prob_dict = dict.fromkeys(target_columns,-1)

    # reading params to get magic numbers
    params = common_utils.read_yaml("params.yaml")
    magic_numbers = params['magic_numbers']

    # Initializing the empty DataFrame to store output of pre-processed data
    df_pre_processed = pd.DataFrame()

    # For each target column, fetch the right column and save it in df_pre_processed
    for cur_target_column in target_columns:

        # Get a list of the column names in the df_cleaned 
        df_cleaned_columns_name = list(df_cleaned.columns)
        
        # Getting the other standard names for the current target column (cur_target_column)
        cur_target_col_std_names = column_name_utils.get_standard_names(cur_target_column,logger)  

        # Set the probability of each column in df_cleaned belonging to the current target column (cur_target_column) to -1.
        probs = [-1] * len(df_cleaned_columns_name)

        # This will get the current target column (cur_target_column) unique values
        cur_target_col_unique_vals = column_value_utils.get_target_column_unique_values(cur_target_column,logger)

        # Iteratively obtain the probability of all columns in cleaned df (df_cleaned) belonging to the
        # current target column (cur_target_column).
        for idx,cur_df_cleaned_column_name in enumerate(df_cleaned_columns_name):
            
            # Getting the current column of cleaned dataframe unique values
            try:
                cur_df_cleaned_column_unique_values = list(df_cleaned[cur_df_cleaned_column_name].unique())
                cur_df_cleaned_column_unique_values = common_utils.assure_data_type(cur_df_cleaned_column_unique_values)
                cur_df_cleaned_column_name = cur_df_cleaned_column_name.lower()
            except:
                continue
    
            # getting simiraity score based on name of current column in the cleaned dataframe (df_cleaned)
            sim_score_from_cur_col_name = column_name_utils.similarity_score_from_col_name(cur_df_cleaned_column_name,cur_target_col_std_names)
            
            # We will modify the simiraity score fetched from the name of current column in the cleaned dataframe (df_cleaned)
            sim_score_from_cur_col_name = score_modifier.modify_sim_score_of_name(sim_score_from_cur_col_name,cur_target_column,magic_numbers)

            # getting simiraity score based on the column values of current column in the cleaned dataframe (df_cleaned)
            similarity_score_of_value = column_value_utils.similarity_score_from_col_values(count_of_rows,cur_df_cleaned_column_unique_values,cur_target_col_unique_vals,cur_target_column)
            
            # Getting final similarity score by merging 
            # modified similarity score fetched from the name and value of current column in the cleaned dataframe (df_cleaned)
            final_similarity_score = score_modifier.merge_similarity_score(sim_score_from_cur_col_name,similarity_score_of_value,cur_target_column,magic_numbers)

            # storing the final similarity score (probability)
            # of the current column in the cleaned dataframe (df_cleaned) 
            probs[idx] = final_similarity_score

        # Getting the column name from the cleaned_df with highest probability (similarity) score
        # to current target column (cur_target_column) 
        predicted_column,prob = common_utils.get_highest_prob_column(probs, df_cleaned_columns_name)

        # update prob dict
        prob_dict[cur_target_column] = prob

        if debug:
            logger.info(predicted_column)
        
        # Adding column of cleaned_df with highest probability(similarity) score to df_pre_processed on if the probability is more than 65%
        p = round(prob,3)
        logger.info(f"'{cur_target_column}' is present as '{predicted_column}' with probability {round(p,3)}")
        if prob > magic_numbers['threshold_for_selection']:
            df_pre_processed[cur_target_column] = df_cleaned[predicted_column]

            # Dropping the column with highest probability (similarity) score from cleaned_df, since we do not need to iterate over that column again
            if cur_target_column not in ["length","width","depth"]:
                df_cleaned = df_cleaned.drop(columns=predicted_column)

    cols = df_cleaned.columns

    remaining_columns_df = pd.DataFrame()
    list_of_dicts = []
    for index, row in df_cleaned.iterrows():
        d = {}
        for col in cols:
            d[col] = row[col]
        list_of_dicts.append(d)
        
    remaining_columns_df["Extra Column"] = list_of_dicts

    # ==== Stage 3 (Post-Processing the Data) ==== 
    # To transform non-standard values to standard values
    fetched_columns = list(df_pre_processed.columns)
    df_pre_processed = post_processing_caller.post_processing_function(fetched_columns,df_pre_processed,magic_numbers,prob_dict)
    
    target_columns+=['ratio','depth %']
    
    logger.info("-" * 75)
    logger.info(f"Not able to detect {set(target_columns) - set(df_pre_processed.columns)}")
    df_processed=df_pre_processed

    # Add links
    df_processed[link_columns_name] = df_with_links[link_columns_name]
    df_processed = pd.concat([df_processed, remaining_columns_df], axis=1)

    # ==== end of all stages ====
    logger.info("-" * 75)
    logger.info(df_processed.head(5))
    logger.info("-" * 75)
    return df_processed
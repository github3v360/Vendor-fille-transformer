# Importing Required Libraries
import logging
from src.utils import data_cleaner, common_utils, column_name_utils, column_value_utils, score_modifier, post_processing_utils
import pandas as pd
import os
from src import hyperlink_extraction


def extract_from_single_sheet(df,ws,debug,logger):

    logger.info("-" * 75)
    # ==== Stage 1 (Cleaning the Data) ====
    df_corrected_headers,correct_row_idx = data_cleaner.correct_df_headers(df)
    df_with_links, link_columns_name = hyperlink_extraction.add_hyperlink_columns(df_corrected_headers,ws,correct_row_idx)
    df_cleaned = data_cleaner.drop_empty_columns_and_rows(df_with_links)
    
    # ==== Stage 2 (Processing the Data) ====

    # Declaring the target column (required columns)
    target_columns = ['clarity','carat','color','shape',"fluorescent","raprate",'cut','polish',"symmetry","table","length","width","depth",
    "price per carat","discount","total","rap price total",'Stock Ref',"comments"]

    # if 'report_no' not in df_with_links.columns:
    #     target_columns.append('report_no')

    # Initializing dictionary to store the probabilty of target columns
    prob_dict = dict.fromkeys(target_columns,-1)

    # reading params to get magic numbers
    params = common_utils.read_yaml("params.yaml")
    magic_numbers = params['magic_numbers']

    # Initializing the empty DataFrame to store output
    # of pre-processed data
    df_pre_processed = pd.DataFrame()

    # For each target column, fetch the right column and save it in df_pre_processed
    for cur_target_column in target_columns:

        # Get a list of the column names in the df_cleaned 
        df_cleaned_columns_name = list(df_cleaned.columns)
        
        # Getting the other standard names for the current target column (cur_target_column)
        cur_target_col_std_names = column_name_utils.get_standard_names(cur_target_column,logger)  

        # Set the probability of each column in df_cleaned belonging to the
        # current target column (cur_target_column) to -1.
        probs = [-1] * len(df_cleaned_columns_name)

        # This will get the current target column (cur_target_column) unique values
        cur_target_col_unique_vals = column_value_utils.get_target_column_unique_values(cur_target_column,logger)

        # Iteratively obtain the probability of all columns in cleaned df (df_cleaned) belonging to the
        # current target column (cur_target_column).
        for idx,cur_df_cleaned_column_name in enumerate(df_cleaned_columns_name):
            
            # Getting the current column of cleaned dataframe unique values
            try:
                cur_df_cleaned_column_unique_values = list(df_cleaned[cur_df_cleaned_column_name].unique())[:10]
                cur_df_cleaned_column_unique_values = common_utils.assure_data_type(cur_df_cleaned_column_unique_values)
                cur_df_cleaned_column_name = cur_df_cleaned_column_name.lower()
            except:
                continue
    
            # getting simiraity score based on name of current column in the cleaned dataframe (df_cleaned)
            sim_score_from_cur_col_name = column_name_utils.similarity_score_from_col_name(cur_df_cleaned_column_name,cur_target_col_std_names)
            
            # We will modify the simiraity score fetched from the name of current column in the cleaned dataframe (df_cleaned)
            # before calculating similarity score based on column values of current column in the cleaned dataframe (df_cleaned)
            sim_score_from_cur_col_name = score_modifier.modify_sim_score_of_name(sim_score_from_cur_col_name,cur_target_column,magic_numbers)

            # getting simiraity score based on the column values of current column in the cleaned dataframe (df_cleaned)
            similarity_score_of_value = column_value_utils.similarity_score_from_col_values(cur_df_cleaned_column_unique_values,cur_target_col_unique_vals,cur_target_column)
            
            # Getting final similarity score by merging 
            # modified similarity score fetched from the name of current column in the cleaned dataframe (df_cleaned) 
            # and simiraity score fetched from the column values of current column in the cleaned dataframe (df_cleaned)
            final_similarity_score = score_modifier.merge_similarity_score(sim_score_from_cur_col_name,similarity_score_of_value,cur_target_column,magic_numbers)

            # storing the final similarity score (probability)
            # of the current column in the cleaned dataframe (df_cleaned) 
            probs[idx] = final_similarity_score

        # Getting the column name from the cleaned_df with highest probability (similarity) score
        # to current target column (cur_target_column) 
        predicted_column,prob = common_utils.get_highest_prob_column(probs, df_cleaned_columns_name)
        # logger.info(predicted_column)
        # logger.info(round(prob,3))

        # update prob dict
        prob_dict[cur_target_column] = prob

        if debug:
            logger.info(predicted_column)
        
        # Adding column of cleaned_df with highest probability(similarity) score 
        # to df_pre_processed on if the probability is more than 65%
        p = round(prob,3)
        logger.info(f"'{cur_target_column}' is present as '{predicted_column}' with probability {round(p,3)}")
        if prob > 0.61:
            df_pre_processed[cur_target_column] = df_cleaned[predicted_column]

            # Dropping the column with highest probability (similarity) score from cleaned_df
            # since we do not need to iterate over that column again
            if cur_target_column not in ["length","width","depth"]:
                df_cleaned = df_cleaned.drop(columns=predicted_column)

    # ==== Stage 3 (Post-Processing the Data) ==== 
    # To transform non-standard values to standard values
    fetched_columns = list(df_pre_processed.columns)

    if "shape" in fetched_columns:
        df_pre_processed['shape'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_shape_column(x['shape'],magic_numbers),axis=1)
    
    if "fluorescent" in fetched_columns:
        df_pre_processed['fluorescent'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_fluor_column(x['fluorescent'],magic_numbers),axis=1)
    
    # Corecting the length, width and depth column
    measurement_columns = ["length","width","depth"]

    if set(measurement_columns).issubset(set(fetched_columns)):

        flag = True
        try:
            temp = float(df_pre_processed['length'].iloc[20])
            flag = False
        except:
            pass

        if flag:
            df_pre_processed['length'],df_pre_processed['width'],df_pre_processed['depth'] = zip(*df_pre_processed.apply(lambda x: post_processing_utils.transform_measurement_column(x['length'],x['depth']),axis=1))
        df_pre_processed['length'] = df_pre_processed['length'].astype(float)
        df_pre_processed['width'] = df_pre_processed['width'].astype(float)
        df_pre_processed['depth'] = df_pre_processed['depth'].astype(float)

        # Calculate the ratio and depth column
        df_pre_processed['ratio'] = round(df_pre_processed['length'] / df_pre_processed['width'],2)
        df_pre_processed['depth %'] = round((df_pre_processed['depth'] / df_pre_processed['width']) * 100,2)

    if "cut" in fetched_columns:
        # Correct the cut column
        df_pre_processed['cut'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_cut_column(x['cut'],magic_numbers),axis=1)

    price_columns = ["carat","raprate","price per carat","discount","total"]

    if set(price_columns[:2]).issubset(set(fetched_columns)) and any([item in fetched_columns for item in price_columns[2:]]):
        # Now Calculating and correcting the price related column
        price_list = price_columns[2:]
        df_pre_processed['raprate'] = df_pre_processed['raprate'].astype(float)
        df_pre_processed['carat'] = df_pre_processed['carat'].astype(float)
        df_pre_processed["rap price total"] = df_pre_processed['raprate'] * df_pre_processed['carat']

    
        max_prob = -1
        price_name = None

        for cur_price_name in price_list:
            try:
                cur_prob = prob_dict[cur_price_name]
            except:
                continue

            if cur_prob > max_prob:
                max_prob = cur_prob
                price_name = cur_price_name
        if price_name == "discount":
            df_pre_processed["discount"] = df_pre_processed["discount"].apply(post_processing_utils.transform_discount_column)
            df_pre_processed["price per carat"] = df_pre_processed['raprate'] * (1 - (df_pre_processed['discount']/100))
            df_pre_processed['total'] = df_pre_processed["price per carat"] * df_pre_processed['carat']
        elif price_name == "price per carat":
            df_pre_processed['discount'] =  (1 - (df_pre_processed["price per carat"] / df_pre_processed['raprate']))*100
            df_pre_processed['total'] = df_pre_processed["price per carat"] * df_pre_processed['carat']
        else:
            df_pre_processed["price per carat"] = df_pre_processed['total'] / df_pre_processed['carat']
            df_pre_processed['discount'] = (1 - (df_pre_processed["price per carat"] / df_pre_processed['raprate']))*100
    target_columns+=['ratio','depth %']
    
    logger.info("-" * 75)
    logger.info(f"Not able to detect {set(target_columns) - set(df_pre_processed.columns)}")
    df_processed=df_pre_processed

    # Add links
    df_processed[link_columns_name] = df_with_links[link_columns_name]

    # ==== end of all stages ====
    logger.info("-" * 75)
    logger.info(df_processed.head(5))
    logger.info("-" * 75)
    return df_processed
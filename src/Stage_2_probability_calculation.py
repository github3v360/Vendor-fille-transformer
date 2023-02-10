from src.utils import common_utils, column_name_utils, column_value_utils, score_modifier
import pandas as pd

def get_column_probability(df_cleaned, cur_target_column, cur_df_cleaned_column_name, cur_df_cleaned_column_unique_values,
                         cur_target_col_std_names, cur_target_col_unique_vals, logger, count_of_rows, magic_numbers):
    # getting simiraity score based on name of current column in the cleaned dataframe (df_cleaned)
    sim_score_from_cur_col_name = column_name_utils.similarity_score_from_col_name(cur_df_cleaned_column_name, cur_target_col_std_names)

    # We will modify the simiraity score fetched from the name of current column in the cleaned dataframe (df_cleaned)
    sim_score_from_cur_col_name = score_modifier.modify_sim_score_of_name(sim_score_from_cur_col_name, cur_target_column, magic_numbers)

    # getting simiraity score based on the column values of current column in the cleaned dataframe (df_cleaned)
    similarity_score_of_value = column_value_utils.similarity_score_from_col_values(count_of_rows, cur_df_cleaned_column_unique_values, cur_target_col_unique_vals, cur_target_column)

    # Getting final similarity score by merging 
    # modified similarity score fetched from the name and value of current column in the cleaned dataframe (df_cleaned)
    final_similarity_score = score_modifier.merge_similarity_score(sim_score_from_cur_col_name, similarity_score_of_value, cur_target_column, magic_numbers)

    return final_similarity_score

def process_data(df_cleaned, logger,link_columns_name,count_of_rows,Date, test_file_name):

    # Declaring the target column (required columns)
    target_columns = ['clarity','carat','color','shape', "fluorescent","raprate",'cut','polish',"symmetry","table","length","width","depth",
    "price per carat","discount","total","rap price total","comments",'report_no']

    report_no_from_link,link_columns_name = common_utils.get_report_no_extracted_from_link(df_cleaned, logger, link_columns_name)

    prob_dict = common_utils.initialize_prob_dict(target_columns)

    df_pre_processed, magic_numbers, remaining_columns_df = pre_process_data(df_cleaned, target_columns, prob_dict, logger, report_no_from_link,link_columns_name,count_of_rows,Date, test_file_name)

    return df_pre_processed, report_no_from_link, magic_numbers, prob_dict, remaining_columns_df, target_columns

def get_remaining_column(df_cleaned):
    cols = df_cleaned.columns
    remaining_columns_df = pd.DataFrame()
    list_of_dicts = []
    for _, row in df_cleaned.iterrows():
        d = {}
        for col in cols:
            if type(col) != str:
                continue
            d[col] = row[col]
        list_of_dicts.append(d)
        
    remaining_columns_df["Extra Column"] = list_of_dicts
    return remaining_columns_df

def get_unique_values(df_cleaned, cur_df_cleaned_column_name):
    try:
        cur_df_cleaned_column_unique_values = list(df_cleaned[cur_df_cleaned_column_name].unique())
        cur_df_cleaned_column_unique_values = common_utils.assure_data_type(cur_df_cleaned_column_unique_values)
        cur_df_cleaned_column_name = cur_df_cleaned_column_name.lower()
        return cur_df_cleaned_column_unique_values, cur_df_cleaned_column_name
    except:
        return None, None

def pre_process_data(df_cleaned, target_columns, prob_dict, logger, report_no_from_link, link_columns_name,count_of_rows,Date, test_file_name):
    
    magic_numbers = common_utils.get_magic_numbers()

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
            cur_df_cleaned_column_unique_values, cur_df_cleaned_column_name = get_unique_values(df_cleaned, cur_df_cleaned_column_name)

            # storing the final similarity score (probability)
            # of the current column in the cleaned dataframe (df_cleaned) 
            probs[idx] = get_column_probability(df_cleaned, cur_target_column, cur_df_cleaned_column_name, cur_df_cleaned_column_unique_values,
                         cur_target_col_std_names, cur_target_col_unique_vals, logger, count_of_rows, magic_numbers)

        # Getting the column name from the cleaned_df with highest probability (similarity) score
        # to current target column (cur_target_column) 
        predicted_column,prob = common_utils.get_highest_prob_column(probs, df_cleaned_columns_name)

        # update prob dict
        prob_dict[cur_target_column] = prob
        
        # Adding column of cleaned_df with highest probability(similarity) score to df_pre_processed on if the probability is more than 65%
        p = round(prob,3)
        logger.info(f"'{cur_target_column}' is present as '{predicted_column}' with probability {round(p,3)}")
        if prob > magic_numbers['threshold_for_selection']:
            df_pre_processed[cur_target_column] = df_cleaned[predicted_column]

            # Dropping the column with highest probability (similarity) score from cleaned_df, since we do not need to iterate over that column again
            if cur_target_column not in ["length","width","depth"]:
                df_cleaned = df_cleaned.drop(columns=predicted_column)

    remaining_columns_df = get_remaining_column(df_cleaned)

    return df_pre_processed, magic_numbers, remaining_columns_df
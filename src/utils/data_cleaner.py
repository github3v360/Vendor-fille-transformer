'''
This module contains utility functions for cleaning data as a part of pre-processing.
'''
def correct_df_headers(input_df):

    """
    This function will correct the input dataframe headers if not correct.
    Therefore this function will eliminate unwanted headers and extract the desired headers
    Args:
    input_df: Input DataFrame
    Output:
    input_df: DataFrame with correct headers
    Example -: input header = ['unnamed 0','Djso', 'unnamed 1', unnamed 2', unnamed 3']
                output header = ['Shape','Color', 'Clarity', 'Carat', 'Price']
    """

    # Possible Correct names of headers (More can be added in future)
    col_names = ['srno', 'color', 'cut', 'shape', 'clarity', 'purity',
                 'carat', 'size', 'cts', 'crtwt', 'fluor', 'flour']

    flag = False

    # Getting the current header names of the input dataframe
    cur_columns = list(input_df.columns)

    correct_row_idx = -1

    # This for loop will check if the DataFrame is already in the correct format or not
    for cur_column in cur_columns:
        if cur_column in col_names:
            flag = True
            break

    # If DataFrame is not in Correct Format
    if not flag:
        # We will check the 10 row below the current header to get the row with correct header
        for i in range(10):
            # Getting the row values of the next row
            cur_columns = list(input_df.iloc[i])
            for cur_column in cur_columns:
                # Below logic will try to match the row values with correct headers
                try:
                    cur_column = cur_column.lower()
                except:
                    continue
                if cur_column in col_names:
                    flag = True 
                    correct_row_idx = i
                    break
            
            # Update the DataFrame if we found row with correct headers
            if flag:
                input_df = input_df[i+1:]
                input_df.columns = cur_columns
                break

    input_df = input_df.reset_index(drop=True)
    return input_df, correct_row_idx

def drop_empty_columns_and_rows(input_df):
    """
    To drop columns and rows with no data
    Args:
    input_df: Input Dataframe
    Output:
    out_input_df = Output DataFrame
    """
    input_df = input_df.dropna(how="all")
    input_df = input_df.dropna(how="all",axis=1)
    return input_df

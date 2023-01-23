import pandas as pd

def correct_df_headers(df):

  """
  This function will correct the input dataframe headers if not correct.
  Therefore this function will eliminate unwanted haeders and extract the desired headers
  Args:
    df: Input DataFrame
  Output:
    df: DataFrame with correct headers
  Example -: input header = ['unnamed 0','Djso', 'unnamed 1', unnamed 2', unnamed 3']
             output header = ['Shape','Color', 'Clarity', 'Carat', 'Price']
  """

  # Possible Correct names of headers (More can be added in future)
  col_names = ['srno','color','cut','shape','clarity','purity',"carat","size" , "cts",  "crtwt","fluor","flour"]

  flag = False

  # Getting the current header names of the input dataframe
  cur_columns = list(df.columns)

  #
  correct_row_idx = -1

  # This for loop wil check if the DataFrame is already in correct format or not
  for cur_column in cur_columns:
    if cur_column in col_names:
      flag = True 
      break

  # If DataFrame is not in Correct Format
  if not flag:

    # We will check the 10 row below the current header to get the row with correct header
    for i in range(10):

      # Getting the row values of next row
      cur_columns = list(df.iloc[i])

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
        df = df[i+1:]
        df.columns = cur_columns
        break
        
  return df,correct_row_idx

def drop_empty_columns(df):
  """
  To drop columns with no data
  Args:
  df: Input Dataframe
  Output:
  out_df = Output DataFrame
  """
#   out_df = df.dropna(axis=1)
  return df.dropna()
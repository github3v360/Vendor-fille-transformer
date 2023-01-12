import pandas as pd 
import pickle
import os
import yaml 

def read_yaml(path_to_yaml: str) -> dict:
  """
  A function to read yaml file and return dictionary
  Args (str) : path to yaml file
  returns: A dictionary of the yaml file
  """
  with open(path_to_yaml) as yaml_file:
    content = yaml.safe_load(yaml_file)
    return content

def string_similarity(string1, string2):
    """Calculates the similarity between two strings using the Levenshtein distance algorithm.
    
    Args:
        string1 (str): The first string.
        string2 (str): The second string.
        
    Returns:
        float: A value between 0 and 1 representing the similarity between the two strings, with 1 being a perfect match.
    """
    # Convert to string type if the string1 and string2 is of other type
    if type(string1) != str:
      string1 = str(string1)
    
    if type(string2) != str:
      string2 = str(string2)

    # Convert the strings to lowercase
    string1 = string1.lower()
    string2 = string2.lower()
    
    # Get the length of both strings
    len1 = len(string1)
    len2 = len(string2)
    
    # Initialize a matrix to store the edit distances
    matrix = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]
    
    # Fill in the first row and column of the matrix
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    
    # Fill in the rest of the matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if string1[i - 1] == string2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    
    # Calculate the similarity score
    distance = matrix[len1][len2]
    max_len = max(len1, len2)
    return 1 - (distance / max_len)


def get_highest_prob_column(probs, cols):
    """Returns the column name with the highest probability.
    
    Args:
        probs (list): A list of probabilities, with one probability value for each column.
        cols (list): A list of column names.
        
    Returns:
        str: The column name with the highest probability.
    """
    # Zip the probabilities and column names into a list of tuples
    prob_cols = zip(probs, cols)
    
    # Sort the list of tuples in descending order of probability
    sorted_prob_cols = sorted(prob_cols, key= lambda item: item[0] ,reverse=True)
    
    # Return the column name with the highest probability
    return sorted_prob_cols[0][1]

def similarity_score_from_col_name(column_name,std_names):

    """This function calculates the similarity score between a column and a target column.
    
    Args:
        column_name (str): The column name.
        std_names (list): The list of standard names of the target column.
        
    Returns:
        str: The similarity score of the column and a target column
    """
    # if column name matches one of the standard name then we return similarity score as 1
    if column_name.lower() in std_names:
      return 1 
    
    # We calculate the string similarity of column name with standard names and return only the highest similarity 
    probs = [string_similarity(column_name,name) for name in std_names]
    return max(probs)

def get_most_common_type(values):
    """Returns the data type that occurs most frequently in a list of values, along with the count of that data type.
    
    Args:
        values (list): The list of values.
        
    Returns:
        tuple: A tuple containing the data type that occurs most frequently in the list and the count of that data type.
    """
    # Initialize a dictionary to count the occurrences of each data type
    type_counts = {
        int: 0,
        float: 0,
        str: 0,
    }
    
    # Count the occurrences of each data type
    for value in values:
        if isinstance(value, int):
            type_counts[int] += 1
        elif isinstance(value, float):
            type_counts[float] += 1
        elif isinstance(value, str):
            type_counts[str] += 1
    
    # Get the data type with the highest count
    most_common_type = max(type_counts, key=type_counts.get)
    
    # Return the data type and count as a tuple
    return (most_common_type, type_counts[most_common_type])

def similarity_score_from_col_values(column_unique_values,taget_column_unique_values):

  """
     This function calculates the similarity score between a column and a target column.
        The range of the smilarity score is not fixed in this function since it depend on the use case
    
    Args:
        column_unique_values (list): The unique values of the input column
        taget_column_unique_values (list): The unique values of the input column
        
    Returns:
        str: The similarity score of the column and a target column
    """ 
  #get the data type of column_unique_values
  input_data_type = get_most_common_type(column_unique_values)

  #get the data type of taget_column_unique_values
  target_data_type = get_most_common_type(taget_column_unique_values)

  # This will indicate that both do not have same data type
  flag = True
  if input_data_type[0] != target_data_type[0]:
    flag = False
  
  # Writing logic for string data type considering target data type will always be correct
  if target_data_type[0] == str:
 
    # If one of column_unique_values matches with any of the taget_column_unique_values then we will return 1 else 0
    for value in column_unique_values:
      if type(value) != str:
        value = str(value)
      if value.lower() in taget_column_unique_values:
        return 1

    return 0
  
  # =====Writing logic for int and float data type=====  
  if flag:
    return input_data_type[1]

  if target_data_type[0] == float:
    # input_data_type is (int) = [1,2,3] while target(float) [1.5,3.6] 
    # therefore they definitely not are same column so need to do anything if input_data_type is int

    if input_data_type[0] == int:
      return 0

    # input_data_type (str)= ['1.23','2.23','3.23'] while target [1.23,2.23,3.23]
    # therefore same column
    # input_data_type (str)= ['1','2','3'] while target [1.23,2.23,3.23]
    # therefore not same column
    total = 0
    for value in column_unique_values:
      if value is not None:
        try:
          value = float(value)
          temp = value - value//1
          if temp != 0:
            total += 1
        except:
          return 0
    return total
  
  # input data type (float)= [1.0,2.0,3.0] while target is [1,2,3] therefore same
  # but if input data type (float)= [1.23,2.48,3.22] while target is [1,2,3] therefore not same
  # input data tyoe (str) = ['1','2','3'] while target is [1,2,3] therefore same
  # input data type (str) = ['1.23','2.23','3.13'] while target is [1,2,3] therefore not same
  total = 0

  for value in column_unique_values:
      if value is not None:
        try:
          value = float(value)
          temp = value - value//1
          if temp == 0:
            total += 1
        except:
          return 0
  return total

def get_standard_names(target_name):
  ''' 
  This function will return the other standard(nick) names of the target name
  Args:
        target_name: The original name of the target column
  Returns:
  list: List of all other standard names of the target name.
  '''
  if target_name == "clarity":
   return ["clarity","purity"]
  
  elif target_name == "color":
    return ["color","colour"]
    
  elif target_name == "shape":
    return ["shape"]
    
  elif target_name == "carat":
    return ["carat","size" , "cts",  "crtwt"]
  
  elif target_name == "fluorescent":
    return ["fluor","flour","fluorescent"]

  else:
    raise Exception("The function could not find other satndard names for this target name")

def get_target_column_unique_values(target_name):
  """
  This function will return the unique values of the target columns

  Args:
  target_name (str): The name of the target column

  returns:
  target_unique_values: List of unique values of the target columns
  """

  # This Flag will become true if the data type of unique values is string
  flag = False

  if target_name == "clarity":
    clarity_file_path = os.path.join(os.path.join("artifacts","pickle_files"),"clarity_list.pkl")
    with open(clarity_file_path,'rb') as f:
      clarity_list = pickle.load(f)
    target_unique_values = clarity_list
    flag = True
  
  elif target_name == 'carat':
    
    #picked some of the random values from the Target CSV File
    target_unique_values = [3.51,3.0,3.05,3.01,3.6]
  
  elif target_name == "color":
    color_file_path = os.path.join(os.path.join("artifacts","pickle_files"),"color_list.pkl")
    with open(color_file_path,'rb') as f:
      color_list = pickle.load(f)
    target_unique_values = color_list
    flag = True
  
  elif target_name == "shape":
    shape_file_path = os.path.join(os.path.join("artifacts","pickle_files"),"shape.pkl")
    with open(shape_file_path,'rb') as f:
      shape_dict = pickle.load(f)
    target_unique_values = list(shape_dict.keys())
    flag = True
  
  elif target_name == "fluorescent":
    target_unique_values = ["faint","medium","none","f","m","n","med","non","fnt"]
    flag = True
    
  else:
    raise Exception("The function could not find this target name")
  
  if flag:
    target_unique_values = [value.lower() for value in target_unique_values]

  return target_unique_values

def modify_sim_score_of_name(sim_score, target_name,magic_numbers):
  """
  This will modify the similarity score based on magic numbers to make the statistical model more robust

  Args:
  target_name (str): The name of the target column
  sim_score(float): similarity score
  magic_numbers(dict) = magic numbers in form of dictionary

  returns:
  sim_score: The modified similarity score
  need_to_continue(bool): Stating that whether we need to calculate the similarity score from values or not
  """

  # Setting Default value of need to continue to True
  need_to_continue = True

  # For Clarity
  if target_name == "clarity":

    if sim_score > magic_numbers['clarity_threshold']:
      need_to_continue = False
    else:
      sim_score = (sim_score / magic_numbers['clarity_normalizing_factor'])
    
  # For Carat
  elif target_name == "carat":
    sim_score *= magic_numbers['carat_enhancing_factor']

  # For Color
  elif target_name == "color":

    if sim_score > magic_numbers['color_threshold']:
      need_to_continue = False
    else:
      sim_score /= magic_numbers['color_normalizing_factor']
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      pass
  
  elif target_name == "fluorescent":
    if sim_score > magic_numbers['fluor_similarity_threshold']:
      need_to_continue = True
    else:
      sim_score /= magic_numbers['fluor_normalizing_factor']
  

  else:
    raise Exception("The function could not find this target name")
  
  return sim_score, need_to_continue

def merge_similarity_score(sim_score_name,sim_score_val, target_name,magic_numbers):
  """
  This functionm will merge similarity score calculated from column name and column values

  Args:
  sim_score_name: similarity score calculated from name
  sim_score_val: similarityb score calculated from value
  target_name: The name of target column
  magic_numbers(dict) = magic numbers in form of dictionary

  returns:
  final_similarity_score
  """

  # For Clarity
  if target_name == "clarity":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['clarity_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name

  # For Carat
  elif target_name == "carat":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['carat_normalizing_factor'])
  
  # For Color
  elif target_name == "color":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['color_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      final_similarity_score = sim_score_name
  
  elif target_name == "fluorescent":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['fluor_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name
    
  else:
    raise Exception("The function could not find this target name")
  
  return final_similarity_score



def iterate_over_columns(df,target_name):
  """
  This function will iterate over all columns and return the probability of all the columns belonging to the target column
  Args:
        df (pandas dataframe): Data Frame given by the user
        target_name (str): The original name of the target column
  Returns:
  probs (list): List of the probabilty of all columns 
  """
  # reading params
  params = read_yaml("params.yaml")

  # Getting the other standard names for the target_name
  std_names = get_standard_names(target_name)

  # Get a list of the column names in the DataFrame given by the user
  columns_name = list(df.columns)

  # Initialize the probability of each column to -1
  probs = [-1] * len(columns_name)

  # This will get the target column unique values
  target_column_unique_values = get_target_column_unique_values(target_name)

  # Iterating over all the column to get similarity score
  for idx,column_name in enumerate(columns_name):

    # Getting the unique values of the current column and lowercase the column name
    try:
      column_unique_values = list(df[column_name].unique())[:10]
      column_name = column_name.lower()
    except:
      continue
    
    # getting simiraity score based on the column name 
    similarity_score_of_name = similarity_score_from_col_name(column_name,std_names)

    # if similarity score is 1 then it means we found our column and we do not need to iterate further
    if similarity_score_of_name == 1:
      probs[idx] = 1
      break
    
    # We will modify the similarity score before calculating similarity score based on column value
    similarity_score_of_name,need_to_continue = modify_sim_score_of_name(similarity_score_of_name,target_name,params['magic_numbers'])

    # if the similarity score is above threshold then we do not need to continue further
    if not need_to_continue:
      break

    # getting simiraity score based on the column values
    similarity_score_of_value = similarity_score_from_col_values(column_unique_values,target_column_unique_values)

    # Getting final similarity score by merging similarity score based on name and values
    final_similarity_score = merge_similarity_score(similarity_score_of_name,similarity_score_of_value,target_name,params['magic_numbers'])

    probs[idx] = final_similarity_score
  
  return probs,columns_name

def transform_shape_column(cur_shape):

  """
  This will transform the non-standard shape name to standard shape name
  Example -: It will transform the "RND" to "ROUND"
  """
  if cur_shape == "" or cur_shape is None:
    return None

  # Loading shape dictionary file
  shape_file_path = os.path.join(os.path.join("artifacts","pickle_files"),"shape.pkl")
  with open(shape_file_path,'rb') as f:
    shape_dict = pickle.load(f)
  
  magic_numbers = read_yaml("params.yaml")['magic_numbers']

  try:
    # Fetching the correct shape using the shape_dict
    transformed = shape_dict[cur_shape]
    return transformed

  # If we are not able to fetch the correct shape from shape_dict 
  # then we will use the similarity calculation concept
  except:
    best_key = ''
    best_sim = -1

    for shape in shape_dict.keys():
      sim = string_similarity(shape.lower(),cur_shape.lower())
      if sim > best_sim:
        best_sim = sim 
        best_key = shape
    
    # If the similarity score is higher then threshold then we return the standard shape accordingly
    if best_sim  > magic_numbers['shape_similarity_threshold']:
      return shape_dict[best_key]
    else:
      return None

def transform_fluor_column(cur_fluor):
  """
  This will transform the non-standard fluor name to standard fluor name
  Example -: It will transform the "MED" to "MEDIUM"
  """

  # Initializing our fluorescent dictionary
  fluor_key = ["faint","medium","none","f","m","n","fnt","med","non"]
  fluor_values = ["FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE"]
  fluor_dict = dict(zip(fluor_key,fluor_values))

  magic_numbers = read_yaml("params.yaml")['magic_numbers']

  try:
    # Fetching the correct fluor using the fluor_dict
    transformed = fluor_dict[cur_fluor]
    return transformed

  # If we are not able to fetch the correct fluor from fluor_dict 
  # then we will use the similarity calculation concept
  except:
    best_key = ''
    best_sim = -1

    for fluor in fluor_dict.keys():
      sim = string_similarity(fluor.lower(),cur_fluor.lower())
      if sim > best_sim:
        best_sim = sim 
        best_key = fluor
    
    # If the similarity score is higher then threshold then we return the standard fluor accordingly
    if best_sim  > magic_numbers['fluor_transfor_df_threshold']:
      return fluor_dict[best_key]
    else:
      return None

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

  # This for loop wil check if the DataFrame is already in correct format or not
  for cur_column in cur_columns:
    if cur_column in col_names:
      flag = True 
      break

  # If DataFrame is not in Correct Format
  if not flag:

    # We will check the 4 row below the current header to get the row with correct header
    for i in range(4):

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
          break

      # Update the DataFrame if we found row with correct headers
      if flag:
        df = df[i+1:]
        df.columns = cur_columns
        break
        
  return df 

def transform_df(df):
  
  """
  This is function will run whole pipeline and 
  transforms the input dataframe in to desired format. 

  Args:
    df: Input DataFrame
  Output:
    df: Transformed DataFrame
  """

  # Correcting the headers of Input DataFrame
  df = correct_df_headers(df)

  # Initializing the final DataFrame
  final_df = pd.DataFrame()
  # Listing the columns to transform in the Input DataFrame
  target_columns = ['clarity','carat','color','shape',"fluorescent"]

  for cur_column in target_columns:

    # Getting the probability of each column belonging to cur_column
    probs, columns_name = iterate_over_columns(df,cur_column)

    # Getting the column name with highest similarity to cur_column
    predicted_column = get_highest_prob_column(probs, columns_name)

    # Assigning column name with highest similarity to cur_column t0 final_df
    final_df[cur_column] = df[predicted_column]

    # Dropping the flluorescent 
    df = df.drop(columns=predicted_column)

    # This will transform the shape values in to the standard values.
    # Example "RND" ==> "Round"
    if cur_column  == 'shape':
      final_df[cur_column] = final_df[cur_column].apply(transform_shape_column)

    if cur_column == "fluorescent":
      final_df[cur_column] = final_df[cur_column].apply(transform_fluor_column)

  return final_df
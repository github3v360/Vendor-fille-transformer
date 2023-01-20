import os 
import pickle
from src.utils.column_name_utils import string_similarity
def transform_shape_column(cur_shape,magic_numbers):

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
    if best_sim  > magic_numbers['shape_similarity_transform_df_threshold']:
      return shape_dict[best_key]
    else:
      return None

def transform_fluor_column(cur_fluor,magic_numbers):
  """
  This will transform the non-standard fluor name to standard fluor name
  Example -: It will transform the "MED" to "MEDIUM"
  """

  # Initializing our fluorescent dictionary
  fluor_key = ["faint","medium","none","f","m","n","fnt","med","non"]
  fluor_values = ["FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE"]
  fluor_dict = dict(zip(fluor_key,fluor_values))

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
    if best_sim  > magic_numbers['fluor_similarity_transform_df_threshold']:
      return fluor_dict[best_key]
    else:
      return None

def transform_measurement_column(cur_val):

  """
  Args:
  cur_val: The current value during iteration of column
  """

  if cur_val is None:
    return cur_val
    
  ops_to_replace = ["+","-","x","X"]

  for cur_op in ops_to_replace:
    cur_val = cur_val.replace(cur_op,"*")

  cur_val = cur_val.split("*")
  cur_val = [float(val) for val in cur_val]
  cur_val.sort(reverse=True)
  return cur_val
  

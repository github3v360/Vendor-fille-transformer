import os,math
import pickle
from src.utils.column_name_utils import string_similarity
def transform_shape_column(cur_shape,magic_numbers):

  """
  This will transform the non-standard shape name to standard shape name
  Example -: It will transform the "RND" to "ROUND"
  """
  if cur_shape == "" or cur_shape is None or (type(cur_shape) != str):
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
  if cur_fluor == "" or cur_fluor is None or (type(cur_fluor) != str):
    return None
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

  if cur_val is None or cur_val is None or (type(cur_val) != str):
    return [1,1,1]
    
  ops_to_replace = ["+","-","x","X"]

  for cur_op in ops_to_replace:
    cur_val = cur_val.replace(cur_op,"*")

  cur_val = cur_val.split("*")
  cur_val = [float(val) for val in cur_val]
  cur_val.sort(reverse=True)
  return cur_val
  
def transform_cut_column(cut_val,magic_numbers):

  """
  This will transform the non-standard shape name to standard shape name
  Example -: It will transform the "RND" to "ROUND"
  """
  if cut_val == "" or cut_val is None:
    return None
  cut_val = str(cut_val)


  cut_key = ["I","EX","VG","G","F","P","EX+"]
  cut_values = ["I","EX","VG","G","F","P","EX"]
  cut_dict = dict(zip(cut_key,cut_values))

  try:
    # Fetching the correct shape using the shape_dict
    transformed = cut_dict[cut_val]
    return transformed

  # If we are not able to fetch the correct shape from shape_dict 
  # then we will use the similarity calculation concept
  except:
    best_key = ''
    best_sim = -1

    for cut in cut_dict.keys():
      sim = string_similarity(cut.lower(),cut_val.lower())
      if sim > best_sim:
        best_sim = sim 
        best_key = cut
    
    # If the similarity score is higher then threshold then we return the standard shape accordingly
    if best_sim  > magic_numbers['cut_similarity_transform_df_threshold']:
      return cut_dict[best_key]
    else:
      return None

def transform_discount_column(disc_val,magic_numbers,ppc_val,raprate_val):
    try:
        if int(disc_val) == 0:      
            disc_val = ((ppc_val/raprate_val) - 1)*100
        if disc_val < 0:
            disc_val*=-1
        return round(disc_val,2)
    except:
        return disc_val

def transform_total_column(tot_val,magic_numbers,ppc_val,carat_val):
    try:
        if type(tot_val) != "int" or int(tot_val) == 0:      
            trial_total = ppc_val*carat_val
            return round(trial_total,2)
        else:
            return round(tot_val,2)
    except:
        return round(tot_val,2)

def transform_rap_total_column(rap_tot_val,magic_numbers,rap_rate,carat_val):
    # print(type(rap_tot_val))
    try:
        if isinstance(rap_tot_val, str) or math.isnan(rap_tot_val) or int(rap_tot_val) == 0 or rap_tot_val != (rap_rate*carat_val):      
            trial_total = rap_rate*carat_val
            return round(trial_total,2)
        else:
            return round(rap_tot_val,2)
    except:
        # trial_total = rap_rate*carat_val
        return round(rap_tot_val,2)
    
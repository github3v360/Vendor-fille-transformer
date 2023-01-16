import os 
import pickle 

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
    target_unique_values = [1.51,2.1,3.05,4.01,5.6]
  
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
  
  elif target_name == "raprate":
    target_unique_values = [12000.00,21000.00,11000.00,18000.00,16000.12]

  elif target_name == "cut":
    target_unique_values = ["I","EX","VG","None","G","F","P"]
    flag = True

  elif target_name == "polish":
    target_unique_values = ["I","EX","VG","G","F","P","VG-EX","G-VG","F-G"]
    flag = True

  elif target_name == "symmetry":
    target_unique_values = ["I","EX","VG","G","F","P","VG-EX","G-VG","F-G"]
    flag = True
    
  else:
    raise Exception("The function could not find this target name")
  
  if flag:
    target_unique_values = [value.lower() for value in target_unique_values]

  return target_unique_values

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

def similarity_score_from_col_values(column_unique_values,taget_column_unique_values,target_name):

  """
     This function calculates the similarity score between a column and a target column.
        The range of the smilarity score is not fixed in this function since it depend on the use case
    
    Args:
        column_unique_values (list): The unique values of the input column
        taget_column_unique_values (list): The unique values of the input column
        target_name: The original name of the target column
        
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
  
  # Getting length of column_unique_values
  n = len(column_unique_values)
  
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
  if not flag:

    # input_data_type[0] == str because we are checking logic for int and float 
    # input_data_type[0] == int vecause if target values are [1.4,1.8] and input values are 
    # [1,3] it means they are definitely not falling in same category.

    if input_data_type[0] == str or input_data_type == int:
      return 0
  
  # Here now the probability is calculated on the basis of the range of value

  if target_name == 'carat':

    rangeA = 1.0
    rangeB = 20.0
  
  elif target_name == 'raprate':
    
    rangeA = 2000
    rangeB = 100000
  
  total = 0
  for value in column_unique_values:

    if type(value) != int or value is None or type(value) != float:
      try:
        value = int(value)
      except:
        continue 
    
    if value >= rangeA and value <= rangeB:
      total+=1
  
  return total / n
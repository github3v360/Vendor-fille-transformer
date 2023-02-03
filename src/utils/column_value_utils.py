import os 
import pickle 
import numpy as np
import logging


def get_target_column_unique_values(target_name,logger):
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

  # The logic for these column in entirely different from others
  # we will try to find arithmetic operators if column is string
  elif target_name in ["length","width","depth"]:
    return ["*","x","X","+","-"]

  elif target_name == "comments":
    # print(target_name)  
    target_unique_values = [",","additional"]
    flag = True
  
  elif target_name == "cut":
    target_unique_values = ["I","EX","VG","G","F","P"]
    flag = True

  elif target_name == "polish":
    target_unique_values = ["I","EX","VG","G","F","P","VG-EX","G-VG","F-G"]
    flag = True

  elif target_name == "symmetry":
    target_unique_values = ["I","EX","VG","G","F","P","VG-EX","G-VG","F-G"]
    flag = True
    
  elif target_name == "table":
    target_unique_values = [56.2,57.6,58.2,59.5,60.4,61.3,62.2,63.2,65.5,70.3,72.2]

  elif target_name == "price per carat":
    target_unique_values = [5000, 7000,8600,10000,12067,16800]

  elif target_name == "discount":
    target_unique_values = [-2,1.0,30.89,70.65,-4.00,-50.00]

  elif target_name == "total":
    target_unique_values = [5000.0, 56789.98,76452.98,54637.83]

  elif target_name == "rap price total":
    target_unique_values = [5000.0, 56789.98,76452.98,54637.83]

  elif target_name == "Stock Ref":
    target_unique_values = ["VSBDJ003","1627905","244507","J841722022A","589452","921905043","1.00W863776","2121000601"]
    
  else:
    logger.exception("The function could not find this target name")
  
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

def get_score_from_range(rangeA,rangeB,values,n):
  total = 0
  for value in values:

    if type(value) not in [int,float] or value is None:
      try:
        value = float(value)
      except:
        continue 
    
    if value >= rangeA and value <= rangeB:
      total+=1
  
  return total / n

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
  
  # Getting length of column_unique_values
  n = len(column_unique_values)

  if n==0:
      return 0

  # ===== Special Logics ===========

  if target_name in ["length","width","depth"]:

    if input_data_type[0] == str:
      get_val = None
      for val in column_unique_values:
        if val is not None and type(val) == str:
          get_val = val
          break
      if get_val is None:
        return 0
      if "*" in get_val:
        return 1
      get_val = get_val.replace("x","*")
      get_val = get_val.replace("X","*")
      try:
        _ = eval(get_val)
        return 1
      except:
        return 0
    
    elif input_data_type[0] == float:
      return get_score_from_range(1,10,column_unique_values,n)
    
    else:
      return 0

  # Writing General logic for string data type considering target data type will always be correct
  elif target_data_type[0] == str:
      
    # If one of column_unique_values matches with any of the taget_column_unique_values then we will return 1 else 0
    for value in column_unique_values:
      if type(value) != str:
        value = str(value)
      value = value.lower().strip()
      if any(value == target_value.strip() for target_value in taget_column_unique_values):
        return 1

    return 0
  
  # =====Writing General logic for int and float data type=====
  else:
  
    # Here now the probability is calculated on the basis of the range of value

    if target_name == 'carat':
      rangeA = 0.1
      rangeB = 10
  
    elif target_name == 'raprate':
      rangeA = 1000
      rangeB = 100000
      
    elif target_name == 'table':
      rangeA = 50
      rangeB = 73
    
    elif target_name == 'price per carat':
      rangeA = 5000
      rangeB = 30000

    elif target_name == 'discount':
      rangeA = -99
      rangeB = 99

      # Additional Logic for Discount
      # Discount columns are the only  ccolumns with negative number so we can take advantage of that

      for val in column_unique_values:

          if val is None:
              continue
          if type(val) not in [int,float]:
              try:
                  val =float(val)
              except:
                  continue
          if val  < 0:
              return 1000    
    
    elif target_name == 'total':
      rangeA = 10000
      rangeB = 100000

    elif target_name == 'rap price total':
      rangeA = 10000
      rangeB = 100000

    return get_score_from_range(rangeA,rangeB,column_unique_values,n)
  
     
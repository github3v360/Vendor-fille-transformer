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
    return sorted_prob_cols[0][1],sorted_prob_cols[0][0]

def assure_data_type(values):

    '''
    This column will transform the string data type to float data type if possible
    Since pandas DataFrame sometimes read dataframe column with float values and convert them in to string 
    Therefore we need to reconvert the string to float
    '''

    out_vals = values.copy()

    for idx,val in enumerate(values):

        if (val is None) or (type(val) in [int,float]):
            out_vals[idx] = val
            continue
        
        else:

            try:
                val = float(val)
            except:
                pass
            out_vals[idx] = val
    return out_vals
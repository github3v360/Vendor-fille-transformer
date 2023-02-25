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
    try:
        # Zip the probabilities and column names into a list of tuples
        prob_cols = zip(probs, cols)

        # Sort the list of tuples in descending order of probability
        sorted_prob_cols = sorted(prob_cols, key= lambda item: item[0] ,reverse=True)

        # Return the column name with the highest probability
        return sorted_prob_cols[0][1],sorted_prob_cols[0][0]
    except:
        return None,None

def assure_data_type(values):

    '''
    This column will transform the string data type to float data type if possible
    Since pandas DataFrame sometimes read dataframe column with float values and
    convert them in to string 
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

def initialize_prob_dict(target_columns):
    prob_dict = dict.fromkeys(target_columns, -1)
    return prob_dict

def get_magic_numbers():
    params = read_yaml("params.yaml")
    magic_numbers = params['magic_numbers']
    return magic_numbers

def get_report_no_extracted_from_link(df_cleaned, logger,link_columns_name):
    if 'report_no' not in df_cleaned.columns:
        logger.info("Report No. Could not be found in Link")
        report_no_from_link = None
    else:
        report_no_from_link = df_cleaned['report_no']
        df_cleaned.drop("report_no", axis=1, inplace=True)
        link_columns_name.remove('report_no')
        logger.info("Report No. discovered in the link")
    return report_no_from_link,link_columns_name
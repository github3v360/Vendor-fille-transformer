'''
This module contains utility functions for common use.
'''
import yaml
import os
import pickle

def read_yaml(path_to_yaml: str) -> dict:
    """
    A function to read yaml file and return dictionary
    Args  : path to yaml file (str)
    returns: A dictionary of the yaml file (dict)
    """
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
        return content

def get_highest_prob_column(probs, cols):
    """
    Returns the column name with the highest probability.
    
    Args:
        probs : A list of probabilities, with one probability 
                value for each column (list)
        cols : A list of column names (list)
        
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
    This function will transform the string values in 'values' list to 
    float data type if possible.
    Since pandas DataFrame sometimes reads dataframe columns with 
    float values and converts them into strings,
    we need to reconvert the strings to float data type.
    Args:
        values : A list of values to be converted to float data type (list)

    Returns:
        list: A list of values with string values converted to float 
                data type if possible.
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
    '''
    This function will intialize 
    the probability dictionary to -1
    Args:
        target_columns: The list of target column names for which the 
                    probability dictionary
                    is to be initialized (list of str)
    Returns:                
        prob_dict: A dictionary with keys as target column names 
                    and initial values as -1 (dict)
    '''
    prob_dict = dict.fromkeys(target_columns, -1)
    return prob_dict

def get_magic_numbers():
    '''
    This function will return all the magic numbers
    in the form of dictionary by reading the params.yaml file
    '''
    params = read_yaml("params.yaml")
    magic_numbers = params['magic_numbers']
    return magic_numbers

def get_report_no_extracted_from_link(df_cleaned, logger,link_columns_name):
    ''' 
    This function will store all the report number extracted from the link
    in to a list if possible
    It will also update the link_columns_name

    Args:
        df_cleaned: The cleaned dataframe where the report number 
                    is to be extracted from(data frame)
        logger: The logger object to log information messages.
        link_columns_name:A list of column names containing the links(list)
    Returns:
        report_no_from_link: A pandas Series containing the extracted 
                            report numbers (pandas Series)
        link_columns_name: An updated list of column names after removing 
                            the "report_no" column (List)

    '''
    if 'report_no' not in df_cleaned.columns:
        logger.info("Report No. not found in Link")
        report_no_from_link = None
    else:
        report_no_from_link = df_cleaned['report_no']
        df_cleaned.drop("report_no", axis=1, inplace=True)
        if "report_no" in link_columns_name:
            link_columns_name.remove('report_no')
        logger.info("Report No. discovered in the link")

    return report_no_from_link,link_columns_name

def load_pickle_files(data):
    dictionaries = []
    for file_name in data:
        try:
            with open(file_name, "rb") as f_name:
                target_unique_values = pickle.load(f_name)
                # Get unique values of target_unique_values and store them in a dictionary
                unique_values = list(set(target_unique_values.values()))
                unique_values.sort()
                unique_values.insert(0, None)
                unique_values.insert(1, 'OTHER')
                target_dict = {value: i for i, value in enumerate(unique_values, start=0)}
                dictionaries.append({os.path.basename(file_name).replace('_dict.pkl', ''): target_dict})
                # print(dictionaries)
        except FileNotFoundError:
            raise ValueError(f"File not found for target name")
    return dictionaries

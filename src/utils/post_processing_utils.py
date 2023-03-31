'''
    This module contains utility functions for post processing column data.
'''
import os
import pickle
import pandas as pd
from collections import Counter
from src.utils.column_name_utils import string_similarity

def transform_column(cur_val, magic_numbers, target_column_name):
    """
    This function is used to transform the non-standard name to the
    standard name for columns like shape, fluorescent and cut.

    Args:
        cur_val: current value (string)
        magic_numbers: dictionary of magic numbers (dict)
        target_column_name: target column name (string)

    Returns:
        transformed value (string) or None if the current value is not 
        valid or could not be transformed
    """

    if target_column_name == 'shape':
        shape_file_path = os.path.join(os.path.join("artifacts","pickle_files"),"shape.pkl")
        with open(shape_file_path,'rb') as f_name:
            target_column_dict = pickle.load(f_name)

    elif target_column_name == "fluor":
        fluor_key = ["faint","medium","none","f","m","n","fnt","med","non"]
        fluor_values = ["FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE","FAINT","MEDIUM","NONE"]
        target_column_dict = dict(zip(fluor_key,fluor_values))

    elif target_column_name == 'cut':
        cut_key = ["I","EX","VG","G","F","P","EX+"]
        cut_values = ["I","EX","VG","G","F","P","EX"]
        target_column_dict = dict(zip(cut_key,cut_values))

    elif target_column_name == "clarity":
        clar_key = ['SI1', 'VS1 -', 'SI1 -', 'SI2', 'SI2 -', 'SI2 +', 'VS1 +', 'VS2', 'VS1', 'VS2 -', 'SI1 +', 'VS2 +']
        clar_values = ['SI1', 'VS1-', 'SI1-', 'SI2', 'SI2-', 'SI2+', 'VS1+', 'VS2', 'VS1', 'VS2-', 'SI1+', 'VS2+']
        target_column_dict = dict(zip(clar_key,clar_values))

    elif target_column_name == "color":
        col_key = ['G', 'D', 'E', 'D -', 'E -', 'E +', 'G +', 'G -', 'H', 'J', 'H +', 'H -', 'I -', 'I', 'J -', 'J +', 'I +','F','F +','F -']
        col_values = ['G', 'D', 'E', 'D-', 'E-', 'E+', 'G+', 'G-', 'H', 'J', 'H+', 'H-', 'I-', 'I', 'J-', 'J+', 'I+','F','F+','F-']

        target_column_dict = dict(zip(col_key,col_values))

    if cur_val == "" or cur_val is None or (type(cur_val) != str):
        return None

    if (target_column_name == "color" or target_column_name == "clarity"):
        if (cur_val in target_column_dict.keys()):
            return target_column_dict[cur_val]
        else:
            return cur_val

    try:
        # Fetching the correct transformed value using the target_column_dict
        transformed = target_column_dict[cur_val]
        return transformed

    # If we are not able to fetch the correct transformed value from target_column_dict
    # then we will use the similarity calculation concept
    except:
        best_key = ''
        best_sim = -1

        for key in target_column_dict.keys():
            sim = string_similarity(key.lower(), cur_val.lower())
            if sim > best_sim:
                best_sim = sim
                best_key = key

        # If the similarity score is higher than threshold, then we
        # return the standard value accordingly
        if best_sim > magic_numbers['{}_similarity_transform_df_threshold'
                                    .format(target_column_name)]:
            return target_column_dict[best_key]
        else:
            return None

def transform_measurement_column(cur_val_l,cur_val_d):
    """
    This function will return length, width and depth if the 
    measurement column is in string format
    Eg -: Input: Measurement = "2 * 3 *4" 
        Output: length = 4, width = 3 and depth = 2

    If the measurement column is in this format = [4*1]
    then length = 4 , width = 1 and depth would be cur_val_d

    Args:
        cur_val_l : current row length value (String)
        cur_val_d : current row depth value (String)

    Returns:
        list: A list of 3 parameters including length width and depth (List)

    """

    if cur_val_l == "" or cur_val_l is None or (type(cur_val_l) != str):
        return [None,None,None]

    ops_to_replace = ["+","-","x","X"]

    for cur_op in ops_to_replace:
        cur_val_l = cur_val_l.replace(cur_op,"*")

    cur_val_l = cur_val_l.split("*")

    cur_val_l_len = 0
    try:
        for val in cur_val_l:
            cur_val_l[cur_val_l_len] = float(val)
            cur_val_l_len+=1
    except:
        return [None,None,None]

    cur_val_l.sort(reverse=True)

    if cur_val_l_len == 2:
        cur_val_l.append(cur_val_d)

    elif cur_val_l_len != 3:
        cur_val_l = [None,None,None]

    return cur_val_l

def transform_discount_column(disc_val):
    '''
    This function will transform discount value.
    It will convert the negative value to postive value

    Example -: -40.38 to 40.38

    Args:
        disc_val : Discount Value (int)
    Returns:
        disc_val : Transformed discount Value (int)

    '''
    try:
        disc_val = float(disc_val)
        if disc_val < 0:
            return disc_val*(-1)
        return disc_val
    except:
        return 0.0

def transform_report_no_column(report_no,report_no_from_link):

    '''
    Function checks report_no extracted from link and from sheet is same or not.
    It gives more prefernce to report_no from sheet

    Args:
        report_no : The report number extracted normally from the sheet (int or )
        report_no_from_link : The report number extracted from the link (int)

    Returns:
        return: The function will return the report number based on the comparsion
        between report_no and report_no_from_link (int)
    '''

    if report_no == report_no_from_link:
        return report_no

    if report_no is not None:
        return report_no

    if report_no_from_link is None:
        return None
    return report_no_from_link

def format_number(num):
    num = int(round(num * 100))
    num_str = str(num).zfill(4)
    return num_str

def generate_report_no_column(report_no,clarity,color,fluorescent,shape,carat,shape_keys,cut,polish,symmetry):
    shape_keys.append(None)
    
    clarity_map = { None: 0,'SI1': 1, 'SI2': 2, 'VS1': 3, 'VS2': 4}
    color_map = {None: 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'H': 5, 'I': 6, 'J': 7}
    cut_map = {None:0, 'I': 1, 'EX': 2, 'VG': 3, 'G': 4, 'F': 5, 'P': 6}
    fluorescent_map = {None: 0,'FAINT': 1, 'MEDIUM': 2, 'NONE': 3}

    shape_value_counter = Counter(f"{chr(i)}{j}" for i in range(ord('A'), ord('A')+(len(shape_keys)//10)+1) for j in range(10))
    shape_map = dict(zip(shape_keys, shape_value_counter))
    last_four = str(report_no)[-4:]

    clarity_num = str(clarity_map[clarity] ) if clarity in clarity_map else str(clarity_map[None])
    color_num = str(color_map[color]) if color in color_map else str(color_map[None])
    cut_num = str(cut_map[cut]) if cut in cut_map else str(cut_map[None])
    polish_num = str(cut_map[polish]) if polish in cut_map else str(cut_map[None])
    symmetry_num = str(cut_map[symmetry]) if symmetry in cut_map else str(cut_map[None])
    fluorescent_num = str(fluorescent_map[fluorescent]) if fluorescent in fluorescent_map else str(fluorescent_map[None])
    carat_num = str(format_number(carat))
    shape_num = str(shape_map[shape]) if shape in shape_map else str(shape_map[None])
    # Concatenate serial numbers and last four digits of previous report
    # print(clarity_num,color_num,fluorescent_num,carat_num)
    # 1.01 = 0101
    # 10.01 = 1001 
    # 1.01 , 10.1  = 101 , 101
    # 1 = 01
    # 10 = 10
    # 10 B1
    # fluro + shape + carat + color + clarity + cut + polish + symmetry + last_four(if empty put 4 0's)
    # 1 + 2 + 4 + 2 + 2 + 1 + 1 + 1 + 4 # convert to hexadecimal (convert each category to hexadecimal)(18)
    new_reportno = fluorescent_num +shape_num + carat_num + color_num +  clarity_num + cut_num + polish_num + symmetry_num +  last_four
    # print(new_reportno)
    return new_reportno
    
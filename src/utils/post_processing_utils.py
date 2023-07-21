'''
    This module contains utility functions for post processing column data.
'''
import os
import math
import pickle
import pandas as pd
from collections import Counter
from src.utils.column_name_utils import string_similarity

def transform_column(cur_val, magic_numbers, target_column_name, target_column_dict, default_value):
    """
    This function is used to transform the non-standard name to the
    standard name for columns like shape, fluorescent and cut.
    Args:
        cur_val: current value (string)
        magic_numbers: dictionary of magic numbers (dict)
        target_column_name: target column name (string)
        default_value: The Default value if not matching key is found from the dictionary
    Returns:
        transformed value (string) or None if the current value is not 
        valid or could not be transformed
    """

    # Loading dictionary for the current target column

    if cur_val == "" or cur_val == "-" or cur_val is None or (type(cur_val) != str):
        return str(default_value).lower()
    
    cur_val = cur_val.replace("+","").replace("-","").replace(" ","").lower()

    try:
        # Fetching the correct transformed value using the target_column_dict
        transformed = target_column_dict[cur_val]
        return str(transformed).lower()

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
            return str(target_column_dict[best_key])
        else:
            return str(default_value)

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

import math

def format_number(num):
    if isinstance(num, str):
        try:
            num = float(num)
        except ValueError:
            num = 0.0

    if math.isnan(num):
        num = 0

    num = int(round(num * 100))
    num_str = str(num).zfill(4)
    return num_str


# def generate_report_no_column(report_no,clarity,color,fluorescent,shape,carat,cut,polish,symmetry,clarity_map,color_map, shape_map, cut_map, fluorescent_map,polish_map,symmetry_map):
#     last_four = str(report_no)[-4:]

#     clarity_num = str(clarity_map[clarity] ) if clarity in clarity_map else str(clarity_map[None])
#     color_num = str(color_map[color]) if color in color_map else str(color_map[None])
#     cut_num = str(cut_map[cut]) if cut in cut_map else str(cut_map[None])
#     polish_num = str(polish_map[polish]) if polish in cut_map else str(cut_map[None])
#     symmetry_num = str(symmetry_map[symmetry]) if symmetry in cut_map else str(cut_map[None])
#     fluorescent_num = str(fluorescent_map[fluorescent]) if fluorescent in fluorescent_map else str(fluorescent_map[None])
#     carat_num = str(format_number(carat))
#     shape_num = str(shape_map[shape]) if shape in shape_map else str(shape_map[None])
    
#     new_reportno = fluorescent_num +shape_num + carat_num + color_num +  clarity_num + cut_num + polish_num + symmetry_num +  last_four
#     # print(new_reportno)
#     return new_reportno
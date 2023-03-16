'''
This module contains utility functions for working with column values in dataframes.
'''
import pickle
import pandas as pd

def get_target_column_unique_values(target_name, logger):
    """
    This function will return the unique values of the target columns

    Args:
    target_name : The name of the target column (String)

    returns:
    target_unique_values: List of unique values of the target columns (List)
    """

    target_dict = {
        "clarity": ("artifacts/pickle_files/clarity_list.pkl", True),
        "carat": ([1.51, 2.1, 3.05, 4.01, 5.6], False),
        "color": ("artifacts/pickle_files/color_list.pkl", True),
        "shape": ("artifacts/pickle_files/shape.pkl", True),
        "fluorescent": (
            ["faint", "medium", "none", "f", "m", "n", "med", "non", "fnt"],
            True,
        ),
        "raprate": ([12000.00, 21000.00, 11000.00, 18000.00, 16000.12], False),
        "length": (["*", "x", "X", "+", "-"], False),
        "width": (["*", "x", "X", "+", "-"], False),
        "depth": (["*", "x", "X", "+", "-"], False),
        "comments": ([",", "additional"], True),
        "cut": (["I", "EX", "VG", "G", "F", "P", "EX+", "EX +"], True),
        "polish": (["I", "EX", "VG", "G", "F", "P", "VG-EX", "G-VG", "F-G"], True),
        "symmetry": (["I", "EX", "VG", "G", "F", "P", "VG-EX", "G-VG", "F-G"], True),
        "table": (
            [56.2, 57.6, 58.2, 59.5, 60.4, 61.3, 62.2, 63.2, 65.5, 70.3, 72.2],
            False,
        ),
        "price per carat": ([5000, 7000, 8600, 10000, 12067, 16800], False),
        "discount": ([-2, 1.0, 30.89, 70.65, -4.00, -50.00], False),
        "total": ([5000.0, 56789.98, 76452.98, 54637.83], False),
        "rap price total": ([5000.0, 56789.98, 76452.98, 54637.83], False),
        "Stock Ref": (
            [
                "VSBDJ003",
                "1627905",
                "244507",
                "J841722022A",
                "589452",
                "921905043",
                "1.00W863776",
                "2121000601",
            ],
            True,
        ),
        "report_no": (
            [5673832784, 4851297767, 4851269742, 52364789152, 45862177986, 45841253698],
            False,
        ),
    }

    try:
        value, flag = target_dict[target_name]
        if isinstance(value, str):
            try:
                with open(value, "rb") as f_name:
                    target_unique_values = pickle.load(f_name)
            except FileNotFoundError:
                raise ValueError(f"File not found for target name: {target_name}")
        else:
            target_unique_values = value
        if flag:
            target_unique_values = [value.lower() for value in target_unique_values]
        return target_unique_values
    except KeyError:
        raise ValueError(f"Target name not found: {target_name}")


def get_most_common_type(values):
    """
    Returns the data type that occurs most frequently in a list of values,
    along with the count of that data type.
    
    Args:
        values : The list of values (List)
        
    Returns:
        tuple: A tuple containing the data type that occurs most frequently 
        in the list and the count of that data type.
        most_common_type: type (int,float,str)
        type_counts[most_common_type] : count of most common type (int)
    """
    # Initialize a dictionary to count the occurrences of each data type

    if len(values) == 0:
        return (None, 0)
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

def get_score_from_range(range_a, range_b, values, num_rows):
    """
    Calculates the score by counting the number of values in the `values` list that
    fall within the range [range_a, range_b] and returning the average count.

    Args:
        range_a : The lower bound of the range ([int, float])
        range_b : The upper bound of the range ([int, float])
        values : A list of numeric values (List[int, float])
        num_rows : The number of rows in the dataset (int)

    Returns:
        float: The average count of values in `values` that fall within the range [range_a, range_b].
    """
    total = 0
    for value in values:
        if type(value) not in [int, float] or value is None:
            try:
                value = float(value)
            except Exception:
                continue 

        if range_a <= value <= range_b:
            total += 1

    return total / num_rows


def convert_to_int_and_update_rows_count(value, count_of_rows):
    """
    Convert values in the list to integers if possible and update the 
    count_of_rows if any None value is encountered.

    Args:
        value: A list of values to be converted to integers (List)
        count_of_rows: An integer representing the total number of rows (int)

    Returns:
        A tuple containing the new list with converted values and the 
        updated count_of_rows after accounting for any None values. 
        new_list: (List)
        count_of_rows: (int)

    """
    new_list = []
    for i in value:
        if pd.isna(i):
            count_of_rows -= 1
        else:
            if isinstance(i, float):
                try:
                    i = int(i)
                except Exception:
                    pass
            new_list.append(i)
    return new_list, count_of_rows

def cal_measurement_columns(count_of_rows, column_unique_values, target_column_unique_value,
                            target_name, input_data_type, num_rows):
    """
    This function will calculate the probability that a column belongs to
    measurement columns (length, width, and depth).

    Measurement columns can either contain this type of string "2*3*4"
    or it will simply contain values "2.8".

    Args:
    - count_of_rows : the number of rows in the column (int)
    - column_unique_values : the list of unique values in the column (List[Union[int, float, str]])
    - target_column_unique_value : the list of unique values in the target column
     (List[Union[int, float, str]])
    - target_name : the name of the target column (str)
    - input_data_type : the data type of the input column (Type)
    - num_rows : the total number of rows in the dataset (int)

    Returns:
    - float: the probability that the column belongs to measurement columns
    """
    # if input data type is string
    if input_data_type[0] == str:
        # Initialize the experiment value to None
        get_val = None

        # Iterate over all the values until we get
        # a value which is not None and has data type of string
        for val in column_unique_values:
            if val is not None and type(val) == str:
                get_val = val
                break

        # If we don't get any value which is not None and has data type
        # of string we return probability as 0
        if get_val is None:
            return 0

        # If there is "*" in get_val we will return the probability as one
        # since measurement column is the only column which will contain "*"
        if "*" in get_val:
            return 1

        # Below lines of code will replace "x" and "X" to "*"
        # Then it will check that after replacing it is a
        # mathematical expression like this "2*5*8" or not
        # if yes return 1 else 0
        get_val = get_val.replace("x", "*")
        get_val = get_val.replace("X", "*")

        try:
            _ = eval(get_val)
            return 1
        except Exception:
            return 0

    # if input data type is float
    elif input_data_type[0] == float:
        return get_score_from_range(1, 10, column_unique_values, num_rows)

    else:
        return 0

def similarity_score_from_col_values(count_of_rows,column_unique_values,
                                target_column_unique_value,target_name):
    """
    This function calculates the similarity score between a column and a target column.
    The range of the similarity score is not fixed in this function since it depends on 
    the use case.
    Args:
        count_of_rows : The number of rows in the column (int)
        column_unique_values : The unique values of the input column (List[Union[int, float, str]])
        target_column_unique_value : The unique values of the target column (List[str])
        target_name: The original name of the target column  (String)
    Returns:
        str: The similarity score of the column and the target column (float)
    """ 

    # get the data type of column_unique_values
    input_data_type = get_most_common_type(column_unique_values)

    # get the data type of target_column_unique_value
    target_data_type = get_most_common_type(target_column_unique_value)

    # Getting length of column_unique_values
    len_column_unique_value = len(column_unique_values)

    if len_column_unique_value==0:
        return 0

    # ===== Special Logics for specific columns ===========

    if target_name in ["length","width","depth"]:
        return cal_measurement_columns(count_of_rows,column_unique_values,
                target_column_unique_value,target_name,input_data_type,len_column_unique_value)
    
    elif target_name == 'report_no':
        updated_unique_values_list,count = convert_to_int_and_update_rows_count(
                                            column_unique_values,count_of_rows)

        last_unique_value = updated_unique_values_list[-1]

        if (not pd.isna(last_unique_value)) and str(last_unique_value).isalnum() and len(
                                            str(last_unique_value)) >= 10:
            unique_values_count = len(updated_unique_values_list)
            if unique_values_count == count:
                return 10
        else:
            return 0

    # Writing General logic for string data type considering target data type will always be correct
    elif target_data_type[0] == str:
    
        # If one of column_unique_values matches with any of the target_column_unique_value
        #  then we will return 1 else 0
        for value in column_unique_values:
            if type(value) != str:
                value = str(value)
            value = value.lower().strip()
            if any(value == target_value.strip() for target_value in target_column_unique_value):
                return 1

        return 0

    # =====Writing General logic for int and float data type=====
    else:

        # Here now the probability is calculated on the basis of the range of value
        # Define the target_name to range mapping
        target_range_map = {
            'carat': (0.1, 10),
            'raprate': (1000, 100000),
            'table': (50, 73),
            'price per carat': (5000, 30000),
            'discount': (-99, 99),
            'total': (10000, 100000),
            'rap price total': (10000, 100000)
        }

        # Check if target_name exists in the mapping
        if target_name in target_range_map:
            # Get the range for target_name
            range_a, range_b = target_range_map[target_name]

            # Specific Logic for Discount
            # Discount columns are the only columns with negative numbers
            if target_name == 'discount':
                for val in column_unique_values:
                    if val is None:
                        continue
                    if type(val) not in [int, float]:
                        try:
                            val = float(val)
                        except Exception:
                            continue
                    if val < 0:
                        return 1000

            return get_score_from_range(range_a, range_b, column_unique_values, 
            len_column_unique_value)

'''
This file calculates difference of files
'''
import csv

def csv_diff_of_each_cell(file1, file2):
    """
    This function takes in two CSV files and returns the difference between them.

    Args:
    file1 (str): The path to the first CSV file.
    file2 (str): The path to the second CSV file.

    Returns:
    list: A list of tuples, where each tuple represents a cell 
          that is different between the two files.
          The tuple contains the row index, column index, 
          and the values from both files respectively.
    """
    # Load the CSV files into lists
    with open(file1, 'r') as f:
        csv1 = [row for row in csv.reader(f)]
    with open(file2, 'r') as f:
        csv2 = [row for row in csv.reader(f)]

    # Find the differences between the two CSV files
    diff_file = []
    for i in range(min(len(csv1), len(csv2))):
        for j in range(min(len(csv1[i]), len(csv2[i]))):
            if csv1[i][j] != csv2[i][j]:
                diff_file.append((i, j, csv1[i][j], csv2[i][j]))

    return diff_file


def file_diff_of_each_line(file1, file2):
    """
    This function takes in two file paths and returns the difference between them.

    Args:
    file1 (str): The path to the first file.
    file2 (str): The path to the second file.

    Returns:
    list: A list of strings, where each string represents a 
            line that is different between the two files.
    """
    # Load the contents of the files into lists
    with open(file1, 'r') as f:
        lines1 = f.readlines()
    with open(file2, 'r') as f:
        lines2 = f.readlines()

    # Find the differences between the two files
    diff_files = []
    i = 0
    while i < len(lines1) or i < len(lines2):
        if i >= len(lines1) or i >= len(lines2):
            diff_files.append(lines1[i] if i < len(lines1) else lines2[i])
        elif lines1[i] != lines2[i]:
            diff_files.append(f"< {lines1[i].strip()}\n> {lines2[i].strip()}\n")
        i += 1

    return diff_files


if __name__ == "__main__":
    diff = csv_diff_of_each_cell(r"artifacts\output_generated\Master_File copy.csv",r"C:\Users\hp\OneDrive\Desktop\D360\Vendor-fille-transformer\artifacts\output_generated\Master_File.csv")
    for row, col, val1, val2 in diff:
        print(f"Row {row+1}, Column {col+1}: {val1} -> {val2}")
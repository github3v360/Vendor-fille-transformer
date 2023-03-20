import os
import warnings

# This line will suppress all DeprecationWarning messages
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_file_paths(directory):
    """
    This function takes in a directory path and returns a list of all file paths in that directory
    and its subdirectories.

    Args:
    directory (str): The path to the directory.

    Returns:
    list: A list of strings, where each string represents a file path.
    """
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

all_unit_test_file_path = get_file_paths("unit_testing")
all_unit_test_file_path.remove("unit_testing/run_all_unit_tests.py")

flag = False
file_names_with_error = []

for current_unit_test_file_path in all_unit_test_file_path:
    print("="*5,current_unit_test_file_path.split("/")[-1][:-3],"="*5)
    # Replace "file.py" with the path of the file that you want to run
    exit_code = os.system(f"python {current_unit_test_file_path}")
    
    if exit_code == 0:
        print("All test cases for this file passed successfully")
    else:
        print("Either some test cases did not pass or some error occured while runnning this file")
        flag = True
        file_names_with_error.append(current_unit_test_file_path.split("/")[-1])
    print()
    print()

if flag:
    print("====== List of files which did not run successfuly are written below ======")
    for file_name in file_names_with_error:print(file_name)
else:
    print("All the files shown no error")

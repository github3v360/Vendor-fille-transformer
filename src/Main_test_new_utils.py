import yaml
import pandas as pd
import argparse
from src import test_new_utils
import os
import time

def main():

    test_data_dir = "artifacts/test_data"
    test_file_names = os.listdir(test_data_dir)

    for test_file_name in test_file_names:
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        out_df = test_new_utils.test_stage(file_path)
        end = time.time()
        print()
        print(f'==== Total time taken {end - start} ====')
    

if __name__ == '__main__' :
    main()
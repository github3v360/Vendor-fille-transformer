import yaml
import pandas as pd
import argparse
from src.utils.all_utils import *
import os
import time

def main():

    test_data_dir = "artifacts/test_data"
    test_file_names = os.listdir(test_data_dir)

    for test_file_name in test_file_names:
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        df = pd.read_excel(file_path)
        out_df = transform_df(df)
        end = time.time()
        print(out_df.head())
        print()
        print(f'==== Total time taken {end - start} ====')
        print("HIIIIII")
    

if __name__ == '__main__' :
    main()
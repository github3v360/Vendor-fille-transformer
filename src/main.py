import yaml
import pandas as pd
import argparse
from src.utils.all_utils import *
import os
import time

def main(file_path):
    print("hello")
    start = time.time()
    df = pd.read_excel(file_path)
    out_df = transform_df(df)
    end = time.time()
    print(out_df.head())
    print()
    print(f'==== Total time taken {end - start} ====')
    

if __name__ == '__main__' :

    args = argparse.ArgumentParser()
    default_path = os.path.join(os.path.join("artifacts","test_data"),"JBBROTHER.xlsx")
    args.add_argument("--file_path","-f",default=default_path)
    parsed_args = args.parse_args()
    main(parsed_args.file_path)
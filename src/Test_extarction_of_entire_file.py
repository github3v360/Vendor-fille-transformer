import yaml
import pandas as pd
import argparse
from src import Extraction_of_entire_file
import os
import time

def main():

    test_data_dir = "artifacts/new_test_data"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/output_generated"

    for test_file_name in test_file_names:
        # if  test_file_name != "3.15.2022.xlsx":
        #     continue
        file_path = os.path.join(test_data_dir,test_file_name)
        # file_path = os.path.join(test_data_dir,"FINESTAR.xlsx")
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        try:
            out_df = Extraction_of_entire_file.extract_entire_file(file_path,True)
            print(out_df.head(2))
        except:
            print(f"Logic Failed for {test_file_name} file")
        end = time.time()
        print()
        print(f'==== Total time taken {end - start} ====')
        out_file_name = test_file_name[:test_file_name.index(".x")] + "_output" +".csv"
        out_file_path = os.path.join(out_dir,out_file_name)
        out_df.to_csv(out_file_path)
    

if __name__ == '__main__' :
    main()
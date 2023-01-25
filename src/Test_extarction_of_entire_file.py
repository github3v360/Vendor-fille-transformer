import yaml
import pandas as pd
import argparse
from src import Extraction_of_entire_file
import os
import time
import shutil

def main():

    test_data_dir = "artifacts/new_test_data"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/output_generated"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)


    for test_file_name in test_file_names:
        # if  test_file_name != "Copy of DOSSIER RD IF VS2.xlsx":
        #     continue
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        try:
            out_df = Extraction_of_entire_file.extract_entire_file(file_path,False)
            print(out_df.head(2))
        except:
            print(f"Logic Failed for {test_file_name} file")
            continue
        print(out_df.head(2))
        end = time.time()
        print()
        print(f'==== Total time taken {end - start} ====')
        out_file_name = test_file_name[:test_file_name.index(".x")] + "_output" +".csv"
        out_file_path = os.path.join(out_dir,out_file_name)
        out_df.to_csv(out_file_path)
    
if __name__ == '__main__' :
    main()
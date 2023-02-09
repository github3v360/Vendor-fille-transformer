import os, shutil
import pandas as pd
import logging

def merge_based_on_date(logger):

    test_data_dir = "artifacts/merge_output_generated"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/merge_date_output_generated"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    for test_file_name in test_file_names:
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        try:
            df = pd.read_csv(file_path)
            print(df)
        except:
            logger.exception()

def merge_according_to_preference():
    print()
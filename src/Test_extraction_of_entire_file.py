import yaml
import pandas as pd
import argparse
from src import Extraction_of_entire_file
import os
import time
import shutil
import logging

logger = logging.getLogger(__name__)
# log1 = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = logging.Formatter('Time: %(asctime)s   :    %(message)s')

file_handler = logging.FileHandler('test.log')
# file_handler_1 = logging.FileHandler('test.log')

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
# file_handler_1.setLevel(logging.INFO)


logger.addHandler(file_handler)
# log1.addHandler(file_handler)
def main():

    test_data_dir = "artifacts/new_test_data"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/output_generated"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)


    for test_file_name in test_file_names:
        # if  test_file_name != "3.15.2022.xlsx":
        #     continue
        logger.info(test_file_name)
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        try:
            out_df = Extraction_of_entire_file.extract_entire_file(file_path,False)
            print(out_df.head(2))
        except:
            logger.exception('Failed Due to: ')
            logger.info(f"Logic Failed for {test_file_name} file")
            logger.info("-" *50)
            # print(f"Logic Failed for {test_file_name} file")
            continue
        end = time.time()
        print()
        print(f'==== Total time taken {end - start} ====')
        out_file_name = test_file_name[:test_file_name.index(".x")] + "_output" +".csv"
        out_file_path = os.path.join(out_dir,out_file_name)
        out_df.to_csv(out_file_path)
    
if __name__ == '__main__' :
    main()
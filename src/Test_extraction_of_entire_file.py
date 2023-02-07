import yaml
import pandas as pd
import argparse
from src import Extraction_of_entire_file
import os
import time
import shutil
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_path = "running_logs/test.log"

formatter = logging.Formatter('Time: %(asctime)s   :    %(message)s')

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
def main():

    test_data_dir = "artifacts/new_test_data_2"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/output_generated"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)


    for test_file_name in test_file_names:
        # if test_file_name != "KAPU BR.xlsx":
        #     continue
        logger.info(test_file_name)
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        try:
            out_df = Extraction_of_entire_file.extract_entire_file(file_path,False,logger)
        except:
            logger.exception('Failed Due to: ')
            logger.info(f"Logic Failed for {test_file_name} file")
            logger.info("-" *50)
            continue
        end = time.time()
        print()
        logger.info(f"'Total time taken : ' {end - start}")
        out_file_name = test_file_name[:test_file_name.index(".x")] + "_output" +".csv"
        out_file_path = os.path.join(out_dir,out_file_name)
        out_df.to_csv(out_file_path)

    logger.info('Process Completed')
    
if __name__ == '__main__' :
    main()
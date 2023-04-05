import yaml
import pandas as pd
import argparse
from src import extraction_of_entire_file
import os
import time
import shutil
import logging
from src import utils 
from utils import merge_files

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_path = "running_logs/test.log"

formatter = logging.Formatter('Time: %(asctime)s   :    %(message)s')

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
def main():

    test_data_dir = "artifacts/test_files"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts/output_generated"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    dummy_df = pd.DataFrame(columns=['clarity','carat','color','shape',"fluorescent","raprate",'cut','polish',"symmetry","table","length","width","depth",
    "price per carat","discount","total","rap price total","comments","report_no"])

    for test_file_name in test_file_names:
        if test_file_name not in ["continue.xlsx"]:
            continue
        logger.info(test_file_name)
        file_path = os.path.join(test_data_dir,test_file_name)
        print(f"====File name : {test_file_name} ======")
        start = time.time()
        try:
            vendor_name = test_file_name[:-5]
            extractor = extraction_of_entire_file.EntireFileExtractor(file_path,False,logger,"2/02/2002",vendor_name)
            out_df = extractor.extract()
            dummy_df = pd.concat([out_df,dummy_df])
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
        out_df.to_csv(out_file_path,index=False)

    out_file_name = "Master_File" +".csv"
    out_file_path = os.path.join(out_dir,out_file_name)
    dummy_df.to_csv(out_file_path,index=False)

    # ans = input("Do you want to merge based on date: (Y/N)?")
    # if ans == 'Y':
    #     merge_files.merge_based_on_date(logger)
    # logger.info('Process Completed')

    logger.info('Process Completed')
    
if __name__ == '__main__' :
    main()
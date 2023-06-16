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

def main():

    test_data_dir = "artifacts/output_generated"
    test_file_names = os.listdir(test_data_dir)
    out_dir = "artifacts"

    list_df =  []
    for test_file_name in test_file_names:
        if test_file_name in ["ParishiDiamond-atlantic1-15-06-2023 (2)_output.csv","Shairu Gems Inventory 15.06.23 (3)_output.csv",
        "Glowstar FY_output.csv","ParishiDiamond-atlantic1-15-06-2023 (3)_output.csv","ParishiDiamond-atlantic1-15-06-2023 (4)_output.csv",
        ]:
            continue
        print(test_file_name)
        file_path = os.path.join(test_data_dir,test_file_name)

        out_df = pd.read_csv(file_path)

        list_df.append(out_df)

    final_df = merge_dataframes(list_df)
    out_file_name = "Merged_Vendor_File" +".csv"
    out_file_path = os.path.join(out_dir,out_file_name)
    final_df.to_csv(out_file_path,index=False)

def merge_dataframes(df_list):
    # Concatenate the dataframes in the list
    df_concatenated = pd.concat(df_list)

    # Drop any duplicate rows based on all columns
    df_no_duplicates = df_concatenated.drop_duplicates()

    counter = dict()

    for idx,val in enumerate(df_no_duplicates["generated_report_no"]):
        counter[val] = idx

    df_final = df_no_duplicates.iloc[list(counter.values())]
    df_final.reset_index(drop=True,inplace=True)
    
    return df_final

if __name__ == '__main__' :
    main()
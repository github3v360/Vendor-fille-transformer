from src import Single_Sheet_extraction
import pandas as pd
import openpyxl 

def extract_entire_file(file_path,debug):

    # ==== (Reading the file // Fetching the file) ====

    # Load the Pandas Data Frame with all sheets
    wb = pd.read_excel(file_path,None)

    # Fetching all sheet names
    sheet_names = list(wb.keys())

    # Initializing Global DataFrame which will store all the processed sheet
    global_df = None

    # Iterating through all the sheet
    for sheet_name in sheet_names:

        # Fetching and storing the sheet
        df = wb[sheet_name]
        
        # Check if the sheet is empty
        if df.empty:
            continue

        # Data Extraction from current sheet
        out_df = Single_Sheet_extraction.extract_from_single_sheet(df,debug)

        # Concatenation of global dataframe with out_df
        if global_df is None:
            global_df = out_df
            continue

        global_df = pd.concat([global_df,out_df])
    
    return global_df
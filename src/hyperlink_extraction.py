from openpyxl import load_workbook
import openpyxl
import os
import pandas as pd
import re

def Find(string):
 
    # Use a regular expression pattern to match URLs
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    links = re.findall(pattern, string)
    
    # Return the first link if any are found, or None if not
    return links[0] if links else None

def add_hyperlink_columns(df,ws,correct_row_idx):

    columns_name = list(df.columns)
    
    cols_link = []

    for cur_col in range(1,len(columns_name)+1):

        sample_cell = ws.cell(row = 12, column = cur_col)
        
        if sample_cell.value is not None:
            cur_link = sample_cell.hyperlink

            if cur_link is not None:
                if cur_link.target is not None:
                    cols_link.append((columns_name[cur_col-1],cur_col))

            else:
                if type(sample_cell.value) == str:
                    if Find(sample_cell.value) is not None:
                        cols_link.append((columns_name[cur_col-1],cur_col))
    
    df_link = pd.DataFrame()

    total_link_columns = len(cols_link)

    if total_link_columns == 0:
        return df,[]

    for j in range(len(cols_link)):
        df_link[df.columns[cols_link[j][1]-1] + "_link"] = [None]*len(df)

    t = 0

    for i in range(correct_row_idx+3,ws.max_row+1):
        
        for j in range(len(cols_link)):

            cur_cell = ws.cell(row=i,column=cols_link[j][1])
            
            # If completely empty simply return None
            if cur_cell.value is None and cur_cell.hyperlink is None:
                df_link[df.columns[cols_link[j][1]-1] + "_link"].iloc[t] = None
                continue

            # If hyperlink is not None
            cur_hyperlink_value = cur_cell.hyperlink

            if cur_hyperlink_value is not None:
                
                # If hyperlink is not given
                if cur_hyperlink_value.target is not None:
                    df_link[df.columns[cols_link[j][1]-1] + "_link"].iloc[t] = cur_hyperlink_value.target
                    continue

            # If hyperlink is None or hyperlink.target is None
            else:
                df_link[df.columns[cols_link[j][1]-1] + "_link"].iloc[t] = Find(cur_cell.value)
            
        t+=1
    df = pd.concat([df,df_link],axis=1)
    return df,list(df_link.columns)
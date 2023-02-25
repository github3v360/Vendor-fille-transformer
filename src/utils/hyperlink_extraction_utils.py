from openpyxl import load_workbook
import openpyxl
import os
import pandas as pd
import re
import urllib.parse

def Find(string):

    ''' 
    This function will fetch the url from the
    string if possible
    '''
 
    # Use a regular expression pattern to match URLs
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    links = re.findall(pattern, string)
    
    # Return the first link if any are found, or None if not
    return links[0] if links else None

def extract_report_number(url):

    '''
    This function will extract the report number from 
    the url
    '''

    if type(url) != str:
        try:
            url = str(url)
        except:
            return None

    parsed_url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed_url.query)
    if 'reportno' in query:
        report_no = query['reportno'][0]
        return report_no
    else:
        match = re.search(r"([\w\.]+)\.pdf$", parsed_url.path)
        if match:
            report_no = match.group(1)
            return report_no
        else:
            match = re.search(r"/diamond-detail/([\w\d]+)", parsed_url.path)
            if match:
                report_no = match.group(1)
                return report_no
            else:
                return None

def get_hyperlink_columns(df, ws, columns_name):
    '''
    This function will find name and index of all the 
    columns which contains the hyperlink
    '''

    cols_link = []
    
    for cur_col in range(1,len(columns_name)+1):
        sample_cell = ws.cell(row = 6, column = cur_col)
        
        if sample_cell.value is not None:
            cur_link = sample_cell.hyperlink

            if cur_link is not None and cur_link.target is not None:
                cols_link.append((columns_name[cur_col-1],cur_col))
            elif type(sample_cell.value) == str and Find(sample_cell.value) is not None:
                cols_link.append((columns_name[cur_col-1],cur_col))
    
    return cols_link
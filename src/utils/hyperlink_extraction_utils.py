'''
This module contains utility functions for hyperlink related extractions.
'''
import re
import urllib.parse

def find(string):
    '''     
    This function fetches a URL from a string if one is present.
    Args:
        string : The string to search for a URL (str)

    Returns:
        str or None: The first URL found in the string, or None if no URLs are found.
    '''

    # Use a regular expression pattern to match URLs
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    links = re.findall(pattern, string)

    # Return the first link if any are found, or None if not
    return links[0] if links else None

def extract_report_number(url):
    '''
    This function extracts the report number from the given url using
    regular expressions and url parsing.

    Args:
        url: A string representing the URL (str)

    Returns:
        str: Report number if it exists in the URL, otherwise None.
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

def get_hyperlink_columns(input_df, worksheet, columns_name):
    
    '''
    This function finds the name and index of all the columns which 
    contain a hyperlink

    Args:
        input_df: Input DataFrame
        worksheet: Openpyxl Worksheet object
        columns_name: List of column names (List)

    Returns:
        cols_link: List of Tuples containing name and index of all the 
        columns which contain a hyperlink (List(tuple))
    '''

    cols_link = []

    for cur_col in range(1,len(columns_name)+1):
        sample_cell = worksheet.cell(row = 6, column = cur_col)

        if sample_cell.value is not None:
            cur_link = sample_cell.hyperlink

            if cur_link is not None and cur_link.target is not None:
                cols_link.append((columns_name[cur_col-1],cur_col))
            elif type(sample_cell.value) == str and find(sample_cell.value) is not None:
                cols_link.append((columns_name[cur_col-1],cur_col))

    return cols_link

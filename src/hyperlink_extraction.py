'''
This file contains class for processing columns with links.
'''
import pandas as pd
from src.utils import hyperlink_extraction_utils

class HyperlinkExtractor:
    """
    Args:
        self : An instance of a class. This method requires the following attributes to be 
                set on the class instance (object)
        work_sheet : The worksheet from which the hyperlink and report numbers should be 
                extracted.(openpyxl Worksheet)
        correct_row_idx : The index of the row from which data extraction should start.(int)
        data_frame : The input Pandas DataFrame.(DataFrame)
        columns_name : List of all cleaned column names (List)
        cols_link : A list of tuples containing the column index and name of the columns 
                containing hyperlinks.(List)
        total_link_columns : Count of columns having links (int)
        data_frame_link : Store values from columns having links (DataFrame)
        new_columns : List of new columns which is to be added (List)
    """
    def __init__(self, work_sheet, correct_row_idx, data_frame):
        self.work_sheet = work_sheet
        self.correct_row_idx = correct_row_idx
        self.data_frame = data_frame
        self.columns_name = list(data_frame.columns)
        self.cols_link = None
        self.total_link_columns = 0
        self.data_frame_link = pd.DataFrame()
        self.new_columns = []

    def add_hyperlink_columns(self):
        """
        Adds hyperlink columns to a Pandas DataFrame based on the given columns name and worksheet.

        Inputs:
            self (object): An instance of a class.
            No direct inputs are required for this method. However, it 
            requires the following attributes to be set on the class instance:

            - data_frame : The input Pandas DataFrame.(DataFrame)
            - work_sheet : From which the hyperlink columns should be extracted.(Worksheet)
            - columns_name : Column names for which hyperlink columns should be extracted.(list)
            
        Outputs:
            data_frame : A Pandas DataFrame with hyperlink columns added.(DataFrame)
            new_columns : A list of the names of the newly added columns.(list)

        The add_hyperlink_columns method extracts hyperlinks and report numbers from a worksheet 
        and adds them as new columns to a Pandas DataFrame.

        """
        if self.work_sheet is None:
            return self.data_frame,self.new_columns
        self.cols_link = hyperlink_extraction_utils.get_hyperlink_columns(
            self.data_frame, self.work_sheet, self.columns_name)
        self.total_link_columns = len(self.cols_link)
        if self.total_link_columns == 0:
            return self.data_frame, []
        for j, _ in enumerate(self.cols_link):
            self.data_frame_link[self.data_frame.columns[self.cols_link[j][1]-1] + "_link"] = \
                [None]*len(self.data_frame)


        self.data_frame_link['report_no'] = [None]*len(self.data_frame)
        self.data_frame_link = self.iteratively_extract_link_and_report_number(0)
        self.data_frame_link.dropna(axis=1, how='all', inplace=True)
        self.data_frame = pd.concat([self.data_frame, self.data_frame_link], axis=1)
        self.new_columns = list(self.data_frame_link.columns)
        return self.data_frame, self.new_columns

    def iteratively_extract_link_and_report_number(self, current):
        """
        Extracts hyperlink and report number for each row in a Pandas DataFrame 
        based on the given worksheet and columns.

        Inputs:
            self : An instance of a class.(object)
            current : The index of the current row being processed.(int)
            
        Outputs:
            data_frame_link : A Pandas DataFrame with hyperlink and report number 
            extracted for each row.(DataFrame)

        The iteratively_extract_link_and_report_number method extracts 
        hyperlinks and report numbers for each row in a
        dataframe based on the given worksheet and columns.
        """
        for i in range(self.correct_row_idx+3, self.work_sheet.max_row+1):
            for j, _ in enumerate(self.cols_link):
                try:
                    cur_cell = self.work_sheet.cell(row=i, column=self.cols_link[j][1])
                    extracted_link = self.extract_link_from_current_cell(cur_cell)
                    self.data_frame_link[self.data_frame.columns[self.cols_link[j][1]-1] + "_link"].iloc[current] = \
                        extracted_link
                    self.extract_report_number_from_cur_cell(current,extracted_link)
                except:
                    continue
            current += 1
        return self.data_frame_link

    def extract_link_from_current_cell(self, cur_cell):
        """
        Extracts a hyperlink from the given cell and returns the hyperlink target.

        Inputs:
            self (object): An instance of a class.
            cur_cell (openpyxl Cell): The cell from which to extract the hyperlink.
            
        Outputs:
            link (str or None): The target of the hyperlink if it exists, otherwise None.

        The extract_link_from_current_cell method extracts a hyperlink target from the given 
        cell in an openpyxl worksheet. If the cell has no hyperlink, the method searches for 
        a hyperlink in the cell's value using the hyperlink_extraction_utils.find function. 
        If no hyperlink is found, the method returns None.

        """
        if cur_cell.value is None and cur_cell.hyperlink is None:
            return None
        cur_hyperlink_value = cur_cell.hyperlink
        if cur_hyperlink_value is not None and cur_hyperlink_value.target is not None:
            return cur_hyperlink_value.target
        return hyperlink_extraction_utils.find(cur_cell.value)

    def extract_report_number_from_cur_cell(self,current,extracted_link):
        """
        The extract_report_number_from_cur_cell method extracts a report number 
        from the given hyperlink and sets the report number value to a specified 
        index of the data_frame_link Pandas DataFrame. 
        If the report number has already been extracted for the given index, 
        the method does nothing.

        Args:

            self (object): An instance of a class.
            current (int): The index of the row in the Pandas DataFrame 
                            where the report number will be added.
            extracted_link (str): The hyperlink from which the report 
                            number will be extracted.

        """
        if self.data_frame_link['report_no'].iloc[current] is None:
            self.data_frame_link['report_no'].iloc[current] = \
            hyperlink_extraction_utils.extract_report_number(extracted_link)

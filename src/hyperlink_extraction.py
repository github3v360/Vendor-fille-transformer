'''
This file contains class for performing post processing with column values in dataframes.
'''
import pandas as pd
from src.utils import hyperlink_extraction_utils

class HyperlinkExtractor:
    """
    Doc
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
        Doc
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
        Doc
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
        Doc
        """
        if cur_cell.value is None and cur_cell.hyperlink is None:
            return None
        cur_hyperlink_value = cur_cell.hyperlink
        if cur_hyperlink_value is not None and cur_hyperlink_value.target is not None:
            return cur_hyperlink_value.target
        return hyperlink_extraction_utils.find(cur_cell.value)

    def extract_report_number_from_cur_cell(self,current,extracted_link):
        """
        Doc
        """
        if self.data_frame_link['report_no'].iloc[current] is None:
            self.data_frame_link['report_no'].iloc[current] = \
            hyperlink_extraction_utils.extract_report_number(extracted_link)

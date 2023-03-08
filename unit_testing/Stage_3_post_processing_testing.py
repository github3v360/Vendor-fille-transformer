import unittest
import pandas as pd
from src.Stage_3_post_processing import PostProcessingData
import numpy as np

class TestPostProcessingData(unittest.TestCase):
    
    def setUp(self):

        # Here we taking Stage_3_post_processing_testing_file.csv as our test file
        self.df_pre_processed = pd.read_csv('artifacts/files_for_unit_testing/stage_3_post_processing_testing_file.csv')

        self.df_cleaned = pd.DataFrame()

        self.report_no_from_link = [6193596691,1419976351,7398125633,1423295944,6412976238]

        self.magic_numbers = {'shape_similarity_transform_df_threshold': 0.7,'fluor_similarity_transform_df_threshold': 0.3,'cut_similarity_transform_df_threshold': 0.7}

        self.prob_dict = {'price per carat': 0.6843187374972216, 'discount': 400.3, 'total': 0.40850515463917525}

        self.link_columns_name = []

        self.remaining_columns_df = pd.DataFrame({'redundant_column_1': [1,2,3,4,5], 'redundant_column_2': [6,7,8,9,10]})
        self.target_columns = ['col1', 'col2']
        self.date = '2022-01-01'
        self.test_file_name = 'test_file.csv'
        self.logger = None

        self.pp_data = PostProcessingData(self.df_pre_processed, self.df_cleaned, self.report_no_from_link,
                                          self.magic_numbers, self.prob_dict, self.link_columns_name,
                                          self.remaining_columns_df, self.target_columns, self.date,
                                          self.test_file_name, self.logger)
    
    def test_add_report_no(self):

        '''
        Tests

        1. In this test, column with name 'report_no' is initialized to None
           if report number not fetched from stage 2. Since our sample self.df_pre_processed doesn't
           have report number therefore 'report_no' will be initalized to None

        2. Also another column will be made which names 'report_no_from_link' which will contain
            report number extracted from link during stage1 
        '''
        out_df = self.pp_data.add_report_number(self.df_pre_processed)
        
        # test 1
        expected_report_no = [None]*5
        self.assertEqual(list(out_df['report_no']),expected_report_no)

        # test 2
        self.assertEqual( list(out_df['report_no_from_link']) , self.report_no_from_link)

    def test_add_date_and_vendor(self):

        '''
        This will test whether the date and vendor is added in our dataframe or not
        '''
        out_df = self.pp_data.add_date_and_vendor(self.df_pre_processed)

        expected_date_series = [self.date]*5
        expected_vendor_series = [self.test_file_name]*5

        # Testing date and vendor
        self.assertEqual( list(out_df['date']) , expected_date_series )
        self.assertEqual( list(out_df['Vendor']) ,  expected_vendor_series)
    
    def test_transform_values(self):

        ''' 
        Tests

        1. All the values of shape column will be transformed to standard value. 'BR' will
           be converted to 'round'
        
        2. All the values of fluorescent column will be transformed to standard value. 'M' will
           be converted to 'Medium'

        3. All the values of cut column will be transformed to standard value. 'EX+' will
           be converted to 'EX'
        
        4. (i) length, width and depth will be extracted from the string. 
           Example-: string='6.58 x 6.59 x 4.07'. length=6.59 ,width=6.58 and depth=4.07
           
           (ii) The other possible string format is "6.58 x 6.59". here we will be able to fetch
                the length and width but won't be able to extract the depth
            
           (iii) if string is empty
        
        5. Ratio and depth% will be calculated from the length, width and depth

        6. Discount will be converted from "-40.38" to "40.38"

        7. All three "price per carat","discount" and "total" will be calculated 
           if "carat", "raprate" and one of the above is given. Else all three will be None
        
        '''
        out_df = self.pp_data.add_report_number(self.df_pre_processed)
        out_df = self.pp_data.transform_values(out_df)

        # test 1 -: initially the first row of shape had 'BR' in our df_pre_processed we expect it to get 
        # converted to 'Round'
        expected_transformed_shape_value_1st_row = "Round"
        self.assertEqual(out_df['shape'].iloc[0],expected_transformed_shape_value_1st_row)

        # test 2  -: initially the first row of flourescent had 'M' in our df_pre_processed we
        # expect it to get  converted to 'MEDIUM'

        expected_transformed_fluorescent_value_1st_row = "MEDIUM"
        self.assertEqual(out_df['fluorescent'].iloc[0],expected_transformed_fluorescent_value_1st_row)

        # test 3  -: initially the first row of cut had 'EX+' in our df_pre_processed we
        # expect it to get  converted to 'EX'
        
        expected_transformed_cut_value_1st_row = "EX"
        self.assertEqual(out_df['cut'].iloc[0],expected_transformed_cut_value_1st_row)

        # test 4 

        # part (i) here we need to fetch out the length, width and depth from 1st row whose format
        # is "3.2 x 4.2 x 5.2"
        expected_transformed_lwd_values_1st_row = [6.59,6.58,4.07]
        self.assertEqual(list(out_df[['length','width','depth']].iloc[0]),expected_transformed_lwd_values_1st_row)

        # part (ii) here we need to fetch out the length and width from last row whose format
        # is "3.2 x 4.2". Depth will be given separately. See the file to see values properly
        expected_transformed_lwd_values_last_row = [6.41,6.37,4.07]
        self.assertEqual(list(out_df[['length','width','depth']].iloc[-1]),expected_transformed_lwd_values_last_row)

        # part (iii) string is empty. 3rd row follows the condition
        expected_transformed_lwd_values_3rd_row = [None,None,None]
        output_lwd_3rd_rpw = list(out_df[['length','width','depth']].iloc[2])

        for idx,out in enumerate(output_lwd_3rd_rpw):
            # here we converting None of other type to python default None
            if pd.isna(out):out = None
            self.assertEqual(out,expected_transformed_lwd_values_3rd_row[idx])



        # test 5
        # first row: length=6.59 width=6.58 and depth=4.07
        # 'ratio' = round(6.59/6.58,2) 'depth %' = round((4.07/6.58)*100,2)
        expected_ratio_1st_row = round(6.59/6.58,2)
        expected_depth_percent_1st_row = round((4.07/6.58)*100,2)

        self.assertEqual(list(out_df[['ratio','depth %']].iloc[0]),[expected_ratio_1st_row,expected_depth_percent_1st_row])

        # test 6
        # we expect that discount will be converted from "-40.38" to "40.38"

        expected_discount_1st_row = 40.38
        self.assertEqual(list(out_df[['discount']].iloc[0]),[expected_discount_1st_row])

        # test 7
        #5425.42     40.38  5859.4536   9100.0   1.08
        #NaN     24.48        NaN      NaN   1.01
        # print(out_df[["price per carat","discount","total","raprate","carat"]])

        # part (i): one of "price per carat","discount" and "total" is given. "raprate" and "carat"
        # is given. We will be able to calculate all five of them. First row follow these above condition

        expected_ppc_1st_row = 5425.42
        expected_discount_1st_row = 40.38
        expected_total_1st_row = 5859.4536 
        expected_results = [expected_ppc_1st_row,expected_discount_1st_row,expected_total_1st_row]

        output = list(out_df[["price per carat","discount","total"]].iloc[0])

        for idx,out in enumerate(output):
            self.assertAlmostEqual(round(out),round(expected_results[idx]))

        # part (ii): "raprate" or "carat" is not given.
        #  We will not be able to calculate all five price related values. last row follow the above condition

        expected_ppc_3rd_row = None
        expected_discount_3rd_row = 24.48
        expected_total_3rd_row = None
        expected_results = [expected_ppc_3rd_row,expected_discount_3rd_row,expected_total_3rd_row]

        output = list(out_df[["price per carat","discount","total"]].iloc[-1])

        for idx,out in enumerate(output):
            if idx==0 or idx==2:
                # here we converting None of other type to python default None
                if pd.isna(out):out = None
            self.assertEqual(out,expected_results[idx])

if __name__ == '__main__':
    unittest.main()
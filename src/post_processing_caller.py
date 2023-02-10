from src.utils import post_processing_utils
import pandas as pd


def post_processing_function(fetched_columns,df_pre_processed,magic_numbers,prob_dict):

    if "shape" in fetched_columns:
        df_pre_processed['shape'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_shape_column(x['shape'],magic_numbers),axis=1)
    
    if "fluorescent" in fetched_columns:
        df_pre_processed['fluorescent'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_fluor_column(x['fluorescent'],magic_numbers),axis=1)
    
    # Corecting the length, width and depth column
    measurement_columns = ["length","width","depth"]

    if set(measurement_columns).issubset(set(fetched_columns)):

        flag = True
        try:
            _ = float(df_pre_processed['length'].iloc[20])
            flag = False
        except:
            pass

        if flag:
            df_pre_processed['length'],df_pre_processed['width'],df_pre_processed['depth'] = zip(*df_pre_processed.apply(lambda x: post_processing_utils.transform_measurement_column(x['length'],x['depth']),axis=1))
        df_pre_processed['length'] = df_pre_processed['length'].astype(float)
        df_pre_processed['width'] = df_pre_processed['width'].astype(float)
        df_pre_processed['depth'] = df_pre_processed['depth'].astype(float)

        # Calculate the ratio and depth column
        df_pre_processed['ratio'] = round(df_pre_processed['length'] / df_pre_processed['width'],2)
        df_pre_processed['depth %'] = round((df_pre_processed['depth'] / df_pre_processed['width']) * 100,2)

    if "cut" in fetched_columns:
        # Correct the cut column
        df_pre_processed['cut'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_cut_column(x['cut'],magic_numbers),axis=1)

    price_columns = ["carat","raprate","price per carat","discount","total"]

    if set(price_columns[:2]).issubset(set(fetched_columns)) and any([item in fetched_columns for item in price_columns[2:]]):
        # Now Calculating and correcting the price related column
        price_list = price_columns[2:]
        df_pre_processed['raprate'] = df_pre_processed['raprate'].astype(float)
        df_pre_processed['carat'] = df_pre_processed['carat'].astype(float)
        df_pre_processed["rap price total"] = df_pre_processed['raprate'] * df_pre_processed['carat']

    
        max_prob = -1
        price_name = None

        for cur_price_name in price_list:
            try:
                cur_prob = prob_dict[cur_price_name]
            except:
                continue

            if cur_prob > max_prob:
                max_prob = cur_prob
                price_name = cur_price_name
        if price_name == "discount":
            df_pre_processed["discount"] = df_pre_processed["discount"].apply(post_processing_utils.transform_discount_column)
            df_pre_processed["price per carat"] = df_pre_processed['raprate'] * (1 - (df_pre_processed['discount']/100))
            df_pre_processed['total'] = df_pre_processed["price per carat"] * df_pre_processed['carat']
        elif price_name == "price per carat":
            df_pre_processed['discount'] =  (1 - (df_pre_processed["price per carat"] / df_pre_processed['raprate']))*100
            df_pre_processed['total'] = df_pre_processed["price per carat"] * df_pre_processed['carat']
        else:
            df_pre_processed["price per carat"] = df_pre_processed['total'] / df_pre_processed['carat']
            df_pre_processed['discount'] = (1 - (df_pre_processed["price per carat"] / df_pre_processed['raprate']))*100
    
    df_pre_processed['report_no'] = df_pre_processed.apply(lambda x: post_processing_utils.transform_report_no_column(x['report_no'],x['report_no_from_link']),axis=1)
    df_pre_processed.drop('report_no_from_link',axis=1,inplace=True)
    return df_pre_processed
    
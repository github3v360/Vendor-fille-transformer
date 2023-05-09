# Importing Required Libraries
import pandas as pd
from src import extraction_of_entire_file
import logging
import io
import tempfile
import os
from google.cloud import storage
import json
# Bucket Realted parameters and functions

tempdir = tempfile.gettempdir()
tempdir = tempfile.mkdtemp()

client = storage.Client(project="friendlychat-bb9ff")

actual_weight_dict = {}
actual_shape_dict = {'OTHER': 'OTHER','ROUND':'RD', 'RD':'RD', 'R':'RD', 'BR':'RD', 'RB':'RD',
          'ROUND BRILLIANT':'RD','ROUNDBRILLIANT':'RD', 'BRILLIANT':'RD',
          'BRILLIANT CUT':'RD', 'BRILLIANTCUT':'RD', 
          'OVAL':'OV',  'OV':'OV', 'OC':'OV',  'OVEL':'OV', 'OL':'OV', 
          'EMERALD':'EM', 'EM':'EM', 'EMRD':'EM', 'EC':'EM', 
          'CUSHION MODIFIED':'CU', 'CMB':'CU','CM':'CU', 'CS':'CU', 'CUSHIONMODIFIED':'CU',
          'CUSHION':'CU', 'CUS':'CU','CU':'CU', 'CMB-N': 'CU', 'CUSHIONB':'CU',
          'CUSHIONSQ':'CU', 'CUSHIONLN':'CU','CUSHIONBRSQ':'CU', 'CUSHIONBRLN': 'CU',
          'PRINCESS':'PR','PR':'PR','PC':'PR',
          'PEAR':'PS','PAER':'PS', 'PER':'PS', 'PS':'PS', 'PE':'PS',
          'RADIANT':'RA', 'RAD':'RA', 'RA':'RA', 'RA-N': 'RA', 'SQRADIANT': 'RA','LRADIANT': 'RA',    
          'MARQUISE':'MQ', 'MR':'MQ', 'MQ':'MQ', 'MAR':'MQ', 
          'ASHCHER':'AS', 'AS':'AS', 'ASSCHER': 'AS',
          'HEART':'HS','HRT':'HS', 'LOVE':'HS', 'HS':'HS', 'HR':'HS', 'HC':'HS','HE':'HS',
          'TRIANGLE':'TR', 'TRI': 'TR', 'TR':'TR'}

# Shape Count 10 
shape_list = ['RD', 'OV', 'EM', 'CU', 'PR', 'PS', 'RA', 'MQ', 'AS', 'HS']
rare_shape_list = ['TR']

def getActualShape(input_shape):
    if type(input_shape) == str:
        try: 
            return actual_shape_dict[input_shape.replace(' ', '').upper()]
        except KeyError:
            return input_shape
    else: 
        return input_shape


actual_color_dict = {'OTHER': 'OTHER','D':'D', 'E':'E', 'F':'F',
                     'G':'G', 'H':'H', 'I':'I',
                     'J':'J', 'K':'K', 'L':'L', 
                     'M':'M', 'N':'N', 'O':'O', 
                     'P':'P', 'Q':'Q','R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V',
                     'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z',
                     'FANCY': 'FANCY'}
# Color Count 23
color_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
rare_color_list = ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def getActualColor(input_color):
    if type(input_color) == str:
        try: 
            return actual_color_dict[input_color.replace(' ', '').upper()]
        except KeyError:
            return input_color
    else: 
        return input_color


actual_fluor_dict = {
    'OTHER': 'OTHER','NONE':'N', 'NON':'N', 'N':'N', 'NO':'N', 'NAN':'N', 'NIL':'N','FLO':'N',
    'FAINT':'F','FNT':'F', 'FL1':'F', 'F': 'F', 'FA': 'F','NEGLIGIBLE':'F',
    'MEDIUM':'M','MED':'M', 'M':'M', 'MEDIUMYELLOW': 'M', 'MD-BL':'M', 'FL2':'M',
    'STRONG':'S', 'STG':'S', 'S':'S', 'ST':'S', 'STRONGYELLOW':'S', 'ST-BL':'S','FL3':'S', 
    'VERY STRONG':'VS', 'VST':'VS', 'VSTG':'VS', 'VS':'VS', 'VERYSTRONG':'VS', 'VERYSTRONGBL': 'VS', 'FL4':'VS','VST-BL':'VS', 
    'SL':'SL', 'SLIGHT':'SL', 'SLI':'SL',
    'VERY SLIGHT':'VSL', 'VSLG':'VSL', 'VSLT':'VSL'
    }
# Fluor Count 5
fluor_list = ['N', 'F', 'M', 'S', 'VS'] 
rare_fluor_list = []

def getActualFlour(input_flour): 
    if type(input_flour) == str:
        try: 
            return actual_fluor_dict[input_flour.replace(' ', '').upper()]
        except KeyError:
            return input_flour
    else: 
        return input_flour

actual_clarity_dict = {
    'OTHER': 'OTHER','FL':'FL', 'IF':'IF', 'VVS1':'VVS1', 'VVS2':'VVS2', 'VS1':'VS1',
    'VS2':'VS2', 'SI1':'SI1', 'SI2':'SI2','SI3':'SI3', 'I1':'I1', 'I2':'I2', 'I3':'I3',
     'P1':'P1', 'P2':'P2', 'P3':'P3', 'LC' : 'LC', 'LOUPECLEAN':'CLEAN'
    }
# Clarity Count 12
clarity_list = ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1', 'I2', 'I3']
rare_clarity_list = ['PK']

def getActualClarity(input_clarity, default_value): 
    if type(input_clarity) == str:
        try: 
            return actual_clarity_dict[input_clarity.replace(' ', '').upper()]
        except KeyError:
            return default_value
    else: 
        return default_value

def getBNCLarity(actual_clarity) :
    if actual_clarity == 'FL':
        return 'IF'
    if actual_clarity in ['I1', 'I2', 'I3']:
        return 'SI2'
    return actual_clarity

#converting I to X
actual_cut_dict = {'OTHER': 'OTHER','EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P','I':'X','IDEAL':'X','ID':'X'}
# Cut Count 5
cut_list = ['X', 'VG', 'G']
rare_cut_list = ['F', 'P']

def getActualCut(input_cut, default_value, shape):
    if not shape == "RD":
        return default_value # Default is VG for all the shapes  
    if type(input_cut) == str:
        try: 
            return actual_cut_dict[input_cut.replace(' ', '').upper()]
        except KeyError:
            return default_value
    else: 
        return default_value

actual_polish_dict = {'OTHER': 'OTHER','EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                      'FAIR TO GOOD':'F-G', 'GOOD TO VERY GOOD':'G-VG','VERY GOOD TO EXCELLENT':'VG-EX',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P','I':'X','IDEAL':'X','ID':'X'}
# Polish Count 5
polish_list = ['X', 'VG', 'G']
rare_polish_list = ['F', 'P']
def getActualPolish(input_polish, default_value): 
    if type(input_polish) == str:
        try: 
            return actual_polish_dict[input_polish.replace(' ', '').upper()]
        except KeyError:
            return default_value
    else: 
        return default_value

actual_sym_dict = {'OTHER': 'OTHER','EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                      'FAIR TO GOOD':'F-G', 'GOOD TO VERY GOOD':'G-VG','VERY GOOD TO EXCELLENT':'VG-EX',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P','I':'X','IDEAL':'X','ID':'X'}
# Symmetry Count 5
sym_list = ['X', 'VG', 'G']
rare_sym_list = ['F', 'P']

def getActualSym(input_sym, default_value): 
    if type(input_sym) == str:
        try: 
            return actual_sym_dict[input_sym.replace(' ', '').upper()]
        except KeyError:
            return default_value
    else: 
        return default_value

# Weight Count 28
weight_list = [0.23, 0.29, 0.37, 0.45, 0.49, 0.54, 0.59, 0.69, 0.74, 0.79, 0.89, 0.94,
               0.99, 1.04, 1.09, 1.19, 1.29, 1.39, 1.49, 1.69, 1.79, 1.99, 2.19, 2.39,
               2.69, 2.99, 3.99, 5.00, 45.00]
rare_weight_list = [10.00, 15.00, 20.00, 25.00, 30.00, 40.00, 50.00]

""" Weight for given stone will be represented by upper end of the range. 
    If the weight of diamond is '0.25', then it will be in the range '0.30'
    For diamond with weight '0.10', it will be under '0.23'
"""
def get_d360_weight(input_weight_str):
    if type(input_weight_str) == int or type(input_weight_str) == float:
      input_weight = input_weight_str
    else:
      input_weight = float(input_weight_str)
    for weight_temp in weight_list: 
      if input_weight < (weight_temp + 0.001):
        return str(weight_temp)
    return input_weight_str


def dict_key(weight, shape, color, clarity, fluor, cut, polish, sym): #WSCCFCPS
    return ','.join([get_d360_weight(weight), shape, color, clarity, fluor, cut, polish, sym]).upper()

def user_value_dict_key(weight, shape, color, clarity, fluor, cut, polish, sym) :
    if shape == None:
        shape = "other"
    if color == None:
        color = "other"
    if clarity == None:
        clarity = "other"
    if polish == None:
        polish = "other"
    if sym == None:
        sym = "other"    
    weight = weight
    shape = actual_shape_dict[shape.upper()]
    color = actual_color_dict[color.upper()]
    clarity = actual_clarity_dict[clarity.upper()]
    fluor = actual_fluor_dict[fluor.upper()]
    cut = actual_cut_dict[cut.upper()]
    polish = actual_polish_dict[polish.upper()]
    sym = actual_sym_dict[sym.upper()]
    return dict_key(weight, shape, color, clarity, fluor, cut, polish, sym)

def outsideBnColorRange(color):
    return color in [ 'L', 'M', 'N', 'O', 'M', 'N', 'O',
               'P', 'Q', 'P', 'Q']
def dataframe_to_dictionary(request):
    request_json = request.get_json()
    json_data = request_json['data']
    date = request.args.get('date')
    vendor_name = request.args.get('vendor_name')
    converted_df = convert_to_common_format(date,vendor_name,json_data)
    dictionary_with_counts = create_count_dictionary(converted_df)
    print("Dump geneerated")
    return json.dumps(dictionary_with_counts)

def create_count_dictionary(out_df):
    my_dict = {}
    for index, row in out_df.iterrows():
        value = user_value_dict_key(row['carat'],row['shape'], row['color'], row['clarity'], row['fluorescent'], row['cut'], row['polish'], row['symmetry'])
        if value in my_dict:
            my_dict[value] += 1
        else:
            my_dict[value] = 1
    print(my_dict)
    print("Dictionary Generated")
    return my_dict

def convert_to_common_format(date,vendor_name,json_data):
    print("In commomn format function")
    df = pd.read_json(json_data)

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "save.xlsx")

    df.to_excel(file_path)
    log_buffer = io.StringIO()
    logging.basicConfig(level=logging.INFO, stream=log_buffer)

    extractor = extraction_of_entire_file.EntireFileExtractor(file_path,False,logging,date,vendor_name)
    out_df = extractor.extract()
    out_df=out_df.reset_index()
    print("Converted to common format")
    return out_df
        
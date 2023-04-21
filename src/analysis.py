import pandas as pd
import pickle
class Analysis_of_files:
    def __init__(self, file_name):
        self.filename = file_name
        self.actual_shape_dict = {'ROUND':'RD', 'RD':'RD', 'R':'RD', 'BR':'RD', 'RB':'RD',
            'ROUND BRILLIANT':'RD','ROUNDBRILLIANT':'RD', 'BRILLIANT':'RD',
            'BRILLIANT CUT':'RD', 'BRILLIANTCUT':'RD', 
            'OVAL':'OV',  'OV':'OV', 'OC':'OV',  'OVEL':'OV', 'OL':'OV', 
            'EMERALD':'EM', 'EM':'EM', 'EMRD':'EM', 'EC':'EM', 
            'CUSHION MODIFIED':'CU', 'CMB':'CU','CM':'CU', 'CS':'CU', 'CUSHIONMODIFIED':'CU',
            'CUSHION':'CU', 'CUS':'CU','CU':'CU',
            'PRINCESS':'PR','PR':'PR','PC':'PR',
            'PEAR':'PS','PAER':'PS', 'PER':'PS', 'PS':'PS',
            'RADIANT':'RA', 'RAD':'RA', 'RA':'RA',          
            'MARQUISE':'MQ', 'MR':'MQ', 'MQ':'MQ', 'MAR':'MQ',
            'ASHCHER':'AS', 'AS':'AS', 'ASSCHER': 'AS',
            'HEART':'HS','HRT':'HS', 'LOVE':'HS', 'HS':'HS', 'HR':'HS', 'HC':'HS',
            'TRIANGLE':'TR', 'TRI': 'TR', 'TR':'TR'}
        self.actual_weight_dict = {}
        self.actual_color_dict = {'D':'D', 'E':'E', 'F':'F', 'D-':'D', 'E-':'E', 'F-':'F','D+':'D', 'E+':'E', 'F+':'F',
                        'G':'G', 'H':'H', 'I':'I', 'G-':'G', 'H-':'H', 'I-':'I', 'G+':'G', 'H+':'H', 'I+':'I',
                        'J':'J', 'K':'K', 'L':'L', 'J-':'J', 'K-':'K', 'L-':'L', 'J+':'J', 'K+':'K', 'L+':'L',
                        'M':'M', 'N':'N', 'O':'O', 'M-':'M', 'N-':'N', 'O-':'O', 'M+':'M', 'N+':'N', 'O+':'O',
                        'P':'P', 'Q':'Q', 'P-':'P', 'Q-':'Q', 'Q+':'Q', 'P+':'P',
                        'Q':'Q', 'R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V',
                        'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z'}
        self.shape_list = ['RD', 'OV', 'EM', 'CU', 'PR', 'PS', 'RA', 'MQ', 'AS', 'HS']
        self.rare_shape_list = ['TR']
        self.color_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        self.rare_color_list = ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.actual_fluor_dict = {
        'NONE':'N', 'NON':'N', 'N':'N', 'NO':'N', 'NAN':'N',
        'FAINT':'F','FNT':'F', 'FAINT':'F', 'F': 'F',
        'MEDIUM':'M','MED':'M', 'M':'M', 'MEDIUMYELLOW': 'M',
        'STRONG':'S', 'STG':'S', 'S':'S', 'ST':'S', 'STRONGYELLOW':'S',
        'VERY STRONG':'VS', 'VST':'VS', 'VSTG':'VS', 'VS':'VS', 'VERYSTRONG':'VS', 'VERYSTRONGBL': 'VS',
        }
        # Fluor Count 5
        self.fluor_list = ['N', 'F', 'M', 'S', 'VS'] 
        self.rare_fluor_list = []
        self.actual_clarity_dict = {
        'FL':'FL', 'IF':'IF', 'VVS1':'VVS1', 'VVS2':'VVS2', 'VS1':'VS1',
        'FL-':'IF', 'IF-':'IF', 'VVS1-':'VVS1', 'VVS2-':'VVS2', 'VS1-':'VS1',
        'FL+':'IF', 'IF+':'IF', 'VVS1+':'VVS1', 'VVS2+':'VVS2', 'VS1+':'VS1',
        'VS2':'VS2', 'SI1':'SI1', 'SI2':'SI2', 'I1':'', 'I2':'', 'I3':'I3',
        'VS2-':'VS2', 'SI1-':'SI1', 'SI2-':'SI2', 'I1-':'I1', 'I2-':'I2', 'I3-':'I3',
        'VS2+':'VS2', 'SI1+':'SI1', 'SI2+':'SI2', 'I1+':'I1', 'I2+':'I2', 'I3+':'I3'}
        # Clarity Count 12
        self.clarity_list = ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1', 'I2', 'I3']
        self.rare_clarity_list = ['PK']
        self.actual_cut_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                    'EX-':'X', 'VG-':'VG', 'G-': 'G',
                    'EX+':'X', 'VG+':'VG', 'G+': 'G',
                    'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                    'F':'F','FAIR':'F','P':'P','POOR':'P',}
        # Cut Count 5
        self.cut_list = ['X', 'VG', 'G']
        self.rare_cut_list = ['F', 'P']
        self.actual_polish_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                    'EX-':'X', 'VG-':'VG', 'G-': 'G',
                    'EX+':'X', 'VG+':'VG', 'G+': 'G',
                    'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                    'F':'F','FAIR':'F','P':'P','POOR':'P',}
        # Polish Count 5
        self.polish_list = ['X', 'VG', 'G']
        self.rare_polish_list = ['F', 'P']
        self.actual_sym_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                    'EX-':'X', 'VG-':'VG', 'G-': 'G',
                    'EX+':'X', 'VG+':'VG', 'G+': 'G',
                    'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                    'F':'F','FAIR':'F','P':'P','POOR':'P',}
        # Symmetry Count 5
        self.sym_list = ['X', 'VG', 'G']
        self.rare_sym_list = ['F', 'P']
        # Weight Count 28
        #weight_list = [0.23, 0.30, 0.38, 0.46, 0.50, 0.55, 0.60, 0.70, 0.75, 0.80, 0.90, 0.95,
        #               1.00, 1.05, 1.10, 1.20, 1.30, 1.40, 1.50, 1.70, 1.80, 2.00, 2.20, 2.40,
        #               2.70, 3.00, 4.00, 5.00, 45.00]
        self.weight_list = [0.23, 0.29, 0.37, 0.45, 0.49, 0.54, 0.59, 0.69, 0.74, 0.79, 0.89, 0.94,
                    0.99, 1.04, 1.09, 1.19, 1.29, 1.39, 1.49, 1.69, 1.79, 1.99, 2.19, 2.39,
                    2.69, 2.99, 3.99, 5.00, 45.00]
        self.rare_weight_list = [10.00, 15.00, 20.00, 25.00, 30.00, 40.00, 50.00]
        self.dict_for_counts = {}

    def getActualShape(self,input_shape):
        if type(input_shape) == str:
            try: 
                return self.actual_shape_dict[input_shape.replace(' ', '').upper()]
            except KeyError:
                return input_shape
        else: 
            return input_shape

    def getActualColor(self,input_color):
        if type(input_color) == str:
            try: 
                return self.actual_color_dict[input_color.replace(' ', '').upper()]
            except KeyError:
                return input_color
        else: 
            return input_color

    def getActualFlour(self,input_flour): 
        if type(input_flour) == str:
            try: 
                return self.actual_fluor_dict[input_flour.replace(' ', '').upper()]
            except KeyError:
                return input_flour
        else: 
            return input_flour

    

    def getActualClarity(self,input_clarity, default_value): 
        if type(input_clarity) == str:
            try: 
                return self.actual_clarity_dict[input_clarity.replace(' ', '').upper()]
            except KeyError:
                return default_value
        else: 
            return default_value


    def getBNCLarity(self,actual_clarity) :
        if actual_clarity == 'FL':
            return 'IF'
        if actual_clarity in ['I1', 'I2', 'I3']:
            return 'SI2'
        return actual_clarity


    def getActualCut(self,input_cut, default_value, shape):
        if not shape == "RD":
            return default_value # Default is VG for all the shapes  
        if type(input_cut) == str:
            try: 
                return self.actual_cut_dict[input_cut.replace(' ', '').upper()]
            except KeyError:
                return default_value
        else: 
            return default_value

    
    def getActualPolish(self,input_polish, default_value): 
        if type(input_polish) == str:
            try: 
                return self.actual_polish_dict[input_polish.replace(' ', '').upper()]
            except KeyError:
                return default_value
        else: 
            return default_value

    def getActualSym(self,input_sym, default_value): 
        if type(input_sym) == str:
            try: 
                return self.actual_sym_dict[input_sym.replace(' ', '').upper()]
            except KeyError:
                return default_value
        else: 
            return default_value

    

    """ Weight for given stone will be represented by upper end of the range. 
        If the weight of diamond is '0.25', then it will be in the range '0.30'
        For diamond with weight '0.10', it will be under '0.23'
    """
    def get_d360_weight(self,input_weight_str):
        if type(input_weight_str) == int or type(input_weight_str) == float:
            input_weight = input_weight_str
        else:
            input_weight = float(input_weight_str)
        for weight_temp in self.weight_list: 
            if input_weight < (weight_temp + 0.001):
                return str(weight_temp)

    # It will generate key by joining all properties by ',' and return it.
    def dict_key(self,weight, shape, color, clarity, fluor, cut, polish, sym): #WSCCFCPS
        return ','.join([self.get_d360_weight(weight), shape, color, clarity, fluor, cut, polish, sym]).replace(' ', '').upper()


    def user_value_dict_key(self,weight, shape, color, clarity, fluor, cut, polish, sym) :
        weight = weight
        shape = self.actual_shape_dict[shape.replace(' ', '').upper()]
        color = self.actual_color_dict[color.replace(' ', '').upper()]
        clarity = self.actual_clarity_dict[clarity.replace(' ', '').upper()]
        fluor = self.actual_fluor_dict[fluor.replace(' ', '').upper()]
        cut = self.actual_cut_dict[cut.replace(' ', '').upper()]
        polish = self.actual_polish_dict[polish.replace(' ', '').upper()]
        sym = self.actual_sym_dict[sym.replace(' ', '').upper()]
        return self.dict_key(weight, shape, color, clarity, fluor, cut, polish, sym)

    def create_dictionary(self):
        for weight in self.weight_list: 
            for shape in self.shape_list: 
                for color in self.color_list:
                    for clarity in self.clarity_list:
                        for fluor in self.fluor_list: 
                            for cut in self.cut_list:
                                for polish in self.polish_list:
                                    for sym in self.sym_list:
                                        self.dict_for_counts[self.dict_key(str(weight), shape, color, clarity, fluor, cut, polish, sym)] = 0 
    def run_on_user_file(self):
        try:
            with open(self.filename, "rb") as f_name:
                self.create_dictionary()
                df = pd.read_csv(f_name)
                # print(len(self.dict_for_counts))
                # print(self.dict_for_counts['0.54,EM,D,IF,N,VG,X,VG'])
                print("Found File")    
        except FileNotFoundError:
            raise ValueError(f"File not found for target name")

    def store_dictionary_to_pickle(self):
        pickle_file = "/home/github3_v360/Vendor-fille-transformer/artifacts/pickle_files/dictionary_count.pickle"
        with open(pickle_file, "wb") as file:
            pickle.dump(self.dict_for_counts, file)
        print("Dictionary stored in pickle file:", pickle_file)

def main():
    p = Analysis_of_files("/home/github3_v360/Vendor-fille-transformer/artifacts/test_files/DHARAM.xlsx")
    p.create_dictionary()
    p.store_dictionary_to_pickle()

if __name__ == "__main__":
    main()

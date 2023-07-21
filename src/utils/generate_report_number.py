actual_weight_dict = {}
actual_shape_dict = {'ROUND':'RD',
          'ROUNDBRILLIANT':'RD', 'BRILLIANT':'RD',
          'BRILLIANTCUT':'RD',
          'OVAL':'OV',  'OV':'OV', 'OC':'OV',  'OVEL':'OV', 'OL':'OV',
          'EMERALD':'EM', 'EM':'EM', 'EMRD':'EM', 'EC':'EM',
          'CUSHIONMODIFIED':'CU', 'CMB':'CU','CM':'CU', 'CS':'CU',
          'CUSHION':'CU', 'CUS':'CU','CU':'CU','CUSHION-MOD':'CU',
          'PRINCESS':'PR','PR':'PR','PC':'PR',
          'PEAR':'PS','PAER':'PS', 'PER':'PS', 'PS':'PS',
          'RADIANT':'RA', 'RAD':'RA', 'RA':'RA',
          'MARQUISE':'MQ', 'MR':'MQ', 'MQ':'MQ', 'MAR':'MQ',
          'ASHCHER':'AS', 'AS':'AS', 'ASSCHER': 'AS',
          'HEART':'HS','HRT':'HS', 'LOVE':'HS', 'HS':'HS', 'HR':'HS', 'HC':'HS',
          'TRIANGLE':'TR', 'TRI': 'TR', 'TR':'TR','NONE':'OTHER',  
          'TRAPEZOID':'OTHER', 
            'LOZENGE':'OTHER', 'BRIOLETTE':'OTHER', 'SQUAREEMERALD':'OTHER',
            'CUSHIONSQ':'OTHER', 'EUROPEANCUT':'OTHER', 'BAGUETTE':'OTHER',
            'SHIELD':'OTHER', 'TAPEREDBULLET':'OTHER', 'SQUARERADIANT':'OTHER',
            'OLDMINER':'OTHER', 'TRILLIANT':'OTHER', 'HALFMOON':'OTHER', 'EPAULETTE':'OTHER',
            'CUSHIONBRSQ':'OTHER', 'TAPEREDBAGUETTE':'OTHER',  'HEXAGONAL':'OTHER', 'CUSHIONB':'OTHER',
            'CUSHIONBRILLIANT':'OTHER', 'CALF':'OTHER', 'BULLETS':'OTHER', 'MARQ':'OTHER', 'KITE':'OTHER', 'PENTAGONAL':'OTHER',
            'CUSHIONBRLN':'OTHER', 'OTHER':'OTHER', 'CUSHIONRADIANT':'OTHER', 'OCTAGONAL':'OTHER', 'SQUARE':'OTHER', 'STAR':'OTHER',
            'ROSE':'OTHER', 'FLANDERS':'OTHER', 'CUSHIONLN':'OTHER','NOTPRESENT':'NOT PRESENT'}

actual_color_dict = {'D':'D', 'E':'E', 'F':'F', 'D-':'D', 'E-':'E', 'F-':'F','D+':'D', 'E+':'E', 'F+':'F',
                     'G':'G', 'H':'H', 'I':'I', 'G-':'G', 'H-':'H', 'I-':'I', 'G+':'G', 'H+':'H', 'I+':'I',
                     'J':'J', 'K':'K', 'L':'L', 'J-':'J', 'K-':'K', 'L-':'L', 'J+':'J', 'K+':'K', 'L+':'L',
                     'M':'M', 'N':'N', 'O':'O', 'M-':'M', 'N-':'N', 'O-':'O', 'M+':'M', 'N+':'N', 'O+':'O',
                     'P':'P', 'P-':'P', 'Q-':'Q', 'Q+':'Q', 'P+':'P',
                     'Q':'Q', 'R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V','NONE':'NONE',
                     'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z','OTHER':'OTHER','NOTPRESENT':'NOT PRESENT'}

actual_fluor_dict = {
    'NONE':'N', 'NON':'N', 'N':'N', 'NO':'N', 'NAN':'N',
    'FAINT':'F','FNT':'F', 'F': 'F',
    'MEDIUM':'M','MED':'M', 'M':'M', 'MEDIUMYELLOW': 'M',
    'STRONG':'S', 'STG':'S', 'S':'S', 'ST':'S', 'STRONGYELLOW':'S',
    'VERY STRONG':'VS', 'VST':'VS', 'VSTG':'VS', 'VS':'VS', 'VERYSTRONG':'VS', 'VERYSTRONGBL': 'VS','OTHER':'OTHER','NOTPRESENT':'NOT PRESENT'
    }


actual_clarity_dict = {
    'FL':'FL', 'IF':'IF', 'VVS1':'VVS1', 'VVS2':'VVS2', 'VS1':'VS1',
    'FL-':'IF', 'IF-':'IF', 'VVS1-':'VVS1', 'VVS2-':'VVS2', 'VS1-':'VS1',
    'FL+':'IF', 'IF+':'IF', 'VVS1+':'VVS1', 'VVS2+':'VVS2', 'VS1+':'VS1',
    'VS2':'VS2', 'SI1':'SI1', 'SI2':'SI2', 'I1':'I1', 'I2':'I2', 'I3':'I3',
    'VS2-':'VS2', 'SI1-':'SI1', 'SI2-':'SI2', 'I1-':'I1', 'I2-':'I2', 'I3-':'I3',
    'VS2+':'VS2', 'SI1+':'SI1', 'SI2+':'SI2', 'I1+':'I1', 'I2+':'I2', 'I3+':'I3','NONE':'NONE',
    'P1': 'P1', 'P2': 'P2','P3': 'P3', 'LC': 'LC','SI3':'SI3','SI3+':'SI3','SI3-':'SI3','OTHER':'OTHER','NOTPRESENT':'NOT PRESENT'}

actual_cut_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G', 'NONE':'NONE' ,
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G','FAIRTOGOOD': 'G','G-VG':'VG','F-G':'G',
                   'F':'F','FAIR':'F','P':'OTHER','POOR':'OTHER','3EX':'X','I':'X','IDEAL':'X','ID':'X','NOTPRESENT':'NOT PRESENT'}

actual_polish_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G','NONE':'NONE',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'OTHER','POOR':'OTHER','FAIRTOGOOD': 'G','G-VG':'VG','F-G':'G',
                   'I':'X','IDEAL':'X','ID':'X','NOTPRESENT':'NOT PRESENT'}

actual_sym_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G','NONE':'NONE',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'OTHER','POOR':'OTHER','FAIRTOGOOD': 'G','G-VG':'VG','F-G':'G',
                   'I':'X','IDEAL':'X','ID':'X','NOTPRESENT':'NOT PRESENT'}

shape_id_dict = {'RD': 0,
                 'OV': 1,
                 'EM': 2,
                 'CU': 3,
                 'PR': 4,
                 'PS': 5,
                 'RA': 6,
                 'MQ': 7,
                 'AS': 8,
                 'HS': 9,
                 'OTHER': 10,
                 'NOT PRESENT':11}

# Color Count 11
color_id_dict = {'D': 0,
                 'E': 1,
                 'F': 2,
                 'G': 3,
                 'H': 4,
                 'I': 5,
                 'J': 6,
                 'K': 7,
                 'L': 8,
                 'M': 9,
                 'OTHER': 10,
                 'NOT PRESENT':11,
                 'NONE':12}

# Fluor Count 5
fluor_id_dict  = {'N': 0,
              'F': 1,
              'M': 2,
              'S': 3,
              'VS': 4,
              'NOT PRESENT':5}


# Clarity Count 11
clarity_id_dict = {'FL': 0,
                   'IF': 1,
                   'VVS1': 2,
                   'VVS2': 3,
                   'VS1': 4,
                   'VS2': 5,
                   'SI1': 6,
                   'SI2': 7,
                   'I1': 8,
                   'I2': 9,
                   'I3': 10,
                   'SI3':11,
                   'P1':12,
                   'P2':13,
                   'P3':14,
                   'NOT PRESENT':15,
                   'NONE':16}

# Cut, Polish, Sym Count 3
cps_id_dict = {'X': 0,
               'VG': 1,
               'G': 2,
               'F':3,
               'OTHER':4,
               'NONE':5,
               'NOT PRESENT':6
               }

def actual_measurement_dict(mes1, mes2, mes3,weight):
    if mes1 == 'NOT PRESENT':
        mes1 = 0.01

    if mes2 == 'NOT PRESENT':
        mes2 =0.01

    if mes3 == 'NOT PRESENT':
        mes3 = 0.01

    if weight == 'NOT PRESENT':
        weight = 99.99
        #NEEDS TO BE CHANGED
    return mes1, mes2, mes3,weight
def decimal_to_base36(decimal_number):
    base36_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if decimal_number == 0:
        return '0'
    base36_number = ''
    while decimal_number > 0:
        decimal_number, remainder = divmod(decimal_number, 36)
        base36_digit = base36_digits[remainder]
        base36_number = base36_digit + base36_number
    return base36_number

def generate_id(weight, shape, color, clarity, fluor, cut, polish, sym, mes1, mes2, mes3):
  shape_id = shape_id_dict[actual_shape_dict[shape.replace(' ', '').upper()]]
  color_id = color_id_dict[actual_color_dict[color.replace(' ', '').upper()]]
  clarity_id = clarity_id_dict[actual_clarity_dict[clarity.replace(' ', '').upper()]]
  fluor_id = fluor_id_dict[actual_fluor_dict[fluor.replace(' ', '').upper()]]
  cut_id = cps_id_dict[actual_cut_dict[cut.replace(' ', '').upper()]]
  polish_id = cps_id_dict[actual_polish_dict[polish.replace(' ', '').upper()]]
  sym_id = cps_id_dict[actual_sym_dict[sym.replace(' ', '').upper()]]
  mes1, mes2, mes3,weight = actual_measurement_dict(mes1, mes2, mes3,weight)

  gen_rep_id = int(weight * 100) # Converting decimal to 4 digit interger
  gen_rep_id = (gen_rep_id * len(shape_id_dict)) + shape_id
  gen_rep_id = (gen_rep_id * len(color_id_dict)) + color_id
  gen_rep_id = (gen_rep_id * len(clarity_id_dict)) + clarity_id
  gen_rep_id = (gen_rep_id * len(fluor_id_dict)) + fluor_id
  gen_rep_id = (gen_rep_id * len(cps_id_dict)) + cut_id
  gen_rep_id = (gen_rep_id * len(cps_id_dict)) + polish_id
  gen_rep_id = (gen_rep_id * len(cps_id_dict)) + sym_id
  gen_rep_id = (gen_rep_id * 1000) + int(mes1 * 100) # Cannot handle more than 10 cm lenth
  gen_rep_id = (gen_rep_id * 1000) + int(mes2 * 100) # Cannot handle more than 10 cm lenth
  gen_rep_id = (gen_rep_id * 1000) + int(mes3 * 100) # Cannot handle more than 10 cm lenth
  alpa_num_id = decimal_to_base36(gen_rep_id)
  return alpa_num_id
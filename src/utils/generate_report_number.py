actual_weight_dict = {}
actual_shape_dict = {'ROUND':'RD',
          'ROUND BRILLIANT':'RD', 'BRILLIANT':'RD',
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
          'TRIANGLE':'TR', 'TRI': 'TR', 'TR':'TR',
          'TRAPEZOID':'TZ', 'RADIANT':'RAD', 'ASHCHER':'ASC',
     'LOZENGE':'LZ', 'HEART':'HT', 'BRIOLETTE':'BRT', 'SQUARE EMERALD':'SE',
     'CUSHIONSQ':'CS', 'EMERALD':'EM', 'EUROPEANCUT':'EC', 'BAGUETTE':'BG', 'TRIANGLE':'TR',
     'CUSHION':'CUS', 'OVAL':'OV', 'SHIELD':'SH', 'TAPERED BULLET':'TB', 'SQUARE RADIANT':'SR',
     'OLDMINER':'OM', 'TRILLIANT':'TL', 'PEAR':'PR', 'HALF MOON':'HM', 'EPAULETTE':'EP', 'PRINCESS':'PRN',
     'CUSHIONBRSQ':'CSBQ', 'TAPERED BAGUETTE':'TBG', 'CUSHION-MOD':'CM', 'HEXAGONAL':'HX', 'CUSHIONB':'CSB',
     'CUSHION BRILLIANT':'CB', 'CALF':'CF', 'BULLETS':'BLT', 'MARQ':'MRQ', 'KITE':'KT', 'PENTAGONAL':'PNT',
     'CUSHIONBRLN':'CSBL', 'OTHER':'OTHER', 'CUSHION RADIANT':'CR', 'OCTAGONAL':'OCT', 'SQUARE':'SQR', 'STAR':'STR',
     'ROSE':'RS', 'FLANDERS':'FLD', 'CUSHIONLN':'CSL'}

actual_color_dict = {'D':'D', 'E':'E', 'F':'F', 'D-':'D', 'E-':'E', 'F-':'F','D+':'D', 'E+':'E', 'F+':'F',
                     'G':'G', 'H':'H', 'I':'I', 'G-':'G', 'H-':'H', 'I-':'I', 'G+':'G', 'H+':'H', 'I+':'I',
                     'J':'J', 'K':'K', 'L':'L', 'J-':'J', 'K-':'K', 'L-':'L', 'J+':'J', 'K+':'K', 'L+':'L',
                     'M':'M', 'N':'N', 'O':'O', 'M-':'M', 'N-':'N', 'O-':'O', 'M+':'M', 'N+':'N', 'O+':'O',
                     'P':'P', 'Q':'Q', 'P-':'P', 'Q-':'Q', 'Q+':'Q', 'P+':'P',
                     'Q':'Q', 'R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V',
                     'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z'}

actual_fluor_dict = {
    'NONE':'N', 'NON':'N', 'N':'N', 'NO':'N', 'NAN':'N',
    'FAINT':'F','FNT':'F', 'FAINT':'F', 'F': 'F',
    'MEDIUM':'M','MED':'M', 'M':'M', 'MEDIUMYELLOW': 'M',
    'STRONG':'S', 'STG':'S', 'S':'S', 'ST':'S', 'STRONGYELLOW':'S',
    'VERY STRONG':'VS', 'VST':'VS', 'VSTG':'VS', 'VS':'VS', 'VERYSTRONG':'VS', 'VERYSTRONGBL': 'VS',
    }


actual_clarity_dict = {
    'FL':'FL', 'IF':'IF', 'VVS1':'VVS1', 'VVS2':'VVS2', 'VS1':'VS1',
    'FL-':'IF', 'IF-':'IF', 'VVS1-':'VVS1', 'VVS2-':'VVS2', 'VS1-':'VS1',
    'FL+':'IF', 'IF+':'IF', 'VVS1+':'VVS1', 'VVS2+':'VVS2', 'VS1+':'VS1',
    'VS2':'VS2', 'SI1':'SI1', 'SI2':'SI2', 'I1':'', 'I2':'', 'I3':'I3',
    'VS2-':'VS2', 'SI1-':'SI1', 'SI2-':'SI2', 'I1-':'I1', 'I2-':'I2', 'I3-':'I3',
    'VS2+':'VS2', 'SI1+':'SI1', 'SI2+':'SI2', 'I1+':'I1', 'I2+':'I2', 'I3+':'I3'}


actual_cut_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P','3EX':'X',}

actual_polish_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P','FAIR TO GOOD': 'FG','G-VG':'GVG','F-G':'FG'}

actual_sym_dict = {'EX':'X', 'VG':'VG', 'G': 'G', 'X':'X',
                   'EX-':'X', 'VG-':'VG', 'G-': 'G',
                   'EX+':'X', 'VG+':'VG', 'G+': 'G',
                   'EXCELLENT':'X', 'VERY GOOD': 'VG', 'VERYGOOD': 'VG', 'GOOD': 'G',
                   'F':'F','FAIR':'F','P':'P','POOR':'P',}

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
                 'OTHER': 10}

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
                 'OTHER': 10}

# Fluor Count 5
fluor_id_dict  = {'N': 0,
              'F': 1,
              'M': 2,
              'S': 3,
              'VS': 4,}


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
                   'I3': 10,}

# Cut, Polish, Sym Count 3
cps_id_dict = {'X': 0,
               'VG': 1,
               'G': 2}

def generate_id(weight, shape, color, clarity, fluor, cut, polish, sym, mes1, mes2, mes3):
  shape_id = shape_id_dict[actual_shape_dict[shape.replace(' ', '').upper()]]
  color_id = color_id_dict[actual_color_dict[color.replace(' ', '').upper()]]
  clarity_id = clarity_id_dict[actual_clarity_dict[clarity.replace(' ', '').upper()]]
  fluor_id = fluor_id_dict[actual_fluor_dict[fluor.replace(' ', '').upper()]]
  cut_id = cps_id_dict[actual_cut_dict[cut.replace(' ', '').upper()]]
  polish_id = cps_id_dict[actual_polish_dict[polish.replace(' ', '').upper()]]
  sym_id = cps_id_dict[actual_sym_dict[sym.replace(' ', '').upper()]]

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
def get_standard_names(target_name):
  ''' 
  This function will return the other standard(nick) names of the target name
  Args:
        target_name: The original name of the target column
  Returns:
  list: List of all other standard names of the target name.
  '''
  if target_name == "clarity":
   return ["clarity","purity"]
  
  elif target_name == "color":
    return ["color","colour"]
    
  elif target_name == "shape":
    return ["shape"]
    
  elif target_name == "carat":
    return ["carat","size" , "cts",  "crtwt"]
  
  elif target_name == "fluorescent":
    return ["fluor","flour","fluorescent"]
  
  elif target_name == "raprate":
    return ["AskingPrice", "Rap",'Rapprice']
  
  elif target_name == "length":
    return ["M1","Measurement","Diameter","length"]

  elif target_name == "width":
    return ["M2","Measurement","Diameter","width"]

  elif target_name == "depth":
    return ["M3","Measurement","Diameter","depth"]
  
  elif target_name == "cut":      
    return ["Cut", "CutGrade"]

  elif target_name == "polish":
    return ["Finish", "Pol","polish"]  

  elif target_name == "symmetry":
    return ["Sym", "Symetry", "Sym-metry","symmetry"]

  elif target_name == "table":
    return ["Table", "Table Percent", "TablePct", "TablePercent", "Tbl","Table%"]
    
  elif target_name == "comments":
    return ["Comments", "Remark", "Lab comment", "Cert comment", "Certificate comment", "Laboratory comment","Report Comments"]
   
  elif target_name == "price per carat":
    return ["AskingPrice", "PerCarat", "PerCt", "Prc", "Price", "PriceCarat", "PriceCt", "PricePerCarat", "PricePerCt", "Px","price/carat","RapNet Price"]

  elif target_name == "discount":
    return ["disc","disc%","RapNet Discount %", "PctRapNetDiscount", "Rap netDisc", "RapnetDiscount", "RapnetDiscountPct", "RapnetDiscountPercent", "RapnetDiscPct", "RapnetDpx", "RapnetRapPct", "RDisc", "RDiscount", "RDiscountPct", "RDiscountPercent", "RDiscPct", "RDpx", "RRapPct", "RapNet Discount Price"]
  
  elif target_name == "total":
    return ["amount","total","total price"]
  
  elif target_name == "rap price total":
    return ["rap total","rap value"]
      
  else:
    raise Exception("The function could not find other satndard names for this target name")

def string_similarity(string1, string2):
    """Calculates the similarity between two strings using the Levenshtein distance algorithm.
    
    Args:
        string1 (str): The first string.
        string2 (str): The second string.
        
    Returns:
        float: A value between 0 and 1 representing the similarity between the two strings, with 1 being a perfect match.
    """
    # Convert to string type if the string1 and string2 is of other type
    if type(string1) != str:
      string1 = str(string1)
    
    if type(string2) != str:
      string2 = str(string2)

    # Convert the strings to lowercase
    string1 = string1.lower()
    string2 = string2.lower()
    
    # Get the length of both strings
    len1 = len(string1)
    len2 = len(string2)
    
    # Initialize a matrix to store the edit distances
    matrix = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]
    
    # Fill in the first row and column of the matrix
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    
    # Fill in the rest of the matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if string1[i - 1] == string2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    
    # Calculate the similarity score
    distance = matrix[len1][len2]
    max_len = max(len1, len2)
    return 1 - (distance / max_len)

def similarity_score_from_col_name(column_name,std_names):

    """This function calculates the similarity score between a column and a target column.
    
    Args:
        column_name (str): The column name.
        std_names (list): The list of standard names of the target column.
        
    Returns:
        str: The similarity score of the column and a target column
    """
    # if column name matches one of the standard name then we return similarity score as 1
    if column_name.lower() in std_names:
      return 1 
    
    # We calculate the string similarity of column name with standard names and return only the highest similarity 
    probs = [string_similarity(column_name,name) for name in std_names]
    return max(probs)
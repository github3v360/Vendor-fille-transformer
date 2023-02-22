def modify_sim_score_of_name(sim_score, target_name,magic_numbers):
  """
  This will modify the similarity score based on magic numbers to make the statistical model more robust

  Args:
  target_name (str): The name of the target column
  sim_score(float): similarity score
  magic_numbers(dict) = magic numbers in form of dictionary

  returns:
  sim_score: The modified similarity score
  need_to_continue(bool): Stating that whether we need to calculate the similarity score from values or not
  """
  
  # For Clarity
  if target_name == "clarity":
      sim_score = (sim_score * magic_numbers['clarity_normalizing_factor_for_col_name'])
    
  # For Carat
  elif target_name == "carat":
    sim_score *= magic_numbers['carat_normalizing_factor_for_col_name']

  # For Color
  elif target_name == "color":
      sim_score *= magic_numbers['color_normalizing_factor_for_col_name']
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      pass
  
  # For fluorescent
  elif target_name == "fluorescent":
      sim_score *= magic_numbers['fluor_normalizing_factor_for_col_name']
  
  # For raprate
  elif target_name == "raprate":
      sim_score *= magic_numbers['raprate_normalizing_factor_for_col_name']
  
  elif target_name in ["length","width","depth"]:
    sim_score = sim_score * magic_numbers['measurement_normalizing_factor_for_col_name']
  
  #For Cut
  elif target_name == "cut":
      sim_score *= magic_numbers['cut_normalizing_factor_for_col_name']
  
  #For Polish
  elif target_name == "polish":
      sim_score *= magic_numbers['polish_normalizing_factor_for_col_name']


  #For Symmetry
  elif target_name == "symmetry":
      sim_score *= magic_numbers['sym_normalizing_factor_for_col_name']
    
  # For table
  elif target_name == "table":
      sim_score *= magic_numbers['table_normalizing_factor_for_col_name']

  elif target_name == "comments":
      sim_score *= magic_numbers['comments_normalizing_factor_for_col_name']

  elif target_name == "price per carat":
      sim_score *= magic_numbers['ppc_normalizing_factor_for_col_name']

  elif target_name == "discount":
      sim_score *= magic_numbers['disc_normalizing_factor_for_col_name']

  elif target_name == "total":
      sim_score *= magic_numbers['amt_normalizing_factor_for_col_name']

  elif target_name == "rap price total":
      sim_score *= magic_numbers['raptotal_normalizing_factor_for_col_name']

  elif target_name == "Stock Ref":
      sim_score *= magic_numbers['stockref_normalizing_factor_for_col_name']

  elif target_name == "report_no":
      sim_score *= magic_numbers['report_normalizing_factor_for_col_name']
      
  # elif target_name == "Cert":
  #     sim_score *= magic_numbers['cert_normalizing_factor_for_col_name']

  else:
    raise Exception("The function could not find this target name")
  
  return round(sim_score,3)

def merge_similarity_score(sim_score_name,sim_score_val, target_name,magic_numbers):
  """
  This functionm will merge similarity score calculated from column name and column values

  Args:
  sim_score_name: Modified similarity score calculated from name
  sim_score_val: similarityb score calculated from value
  target_name: The name of target column
  magic_numbers(dict) = magic numbers in form of dictionary

  returns:
  final_similarity_score
  """

  # For Clarity
  if target_name == "clarity":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['clarity_normalizing_factor_for_col_value']

  # For Carat
  elif target_name == "carat":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['carat_normalizing_factor_for_col_value'])
  
  # For Color
  elif target_name == "color":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['color_normalizing_factor_for_col_value']
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      final_similarity_score = sim_score_name
  
  # Fluorescent
  elif target_name == "fluorescent":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['fluor_normalizing_factor_for_col_value']
  
  # Raprate
  elif target_name == "raprate":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['raprate_normalizing_factor_for_col_value'])
  
  elif target_name in ["length","width","depth"]:
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['measurement_normalizing_factor_for_col_value'])
  
  #Cut 
  elif target_name == "cut":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['cut_normalizing_factor_for_col_value']
            
  #Polish      
  elif target_name == "polish":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['polish_normalizing_factor_for_col_value']

  #symmetry          
  elif target_name == "symmetry":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['sym_normalizing_factor_for_col_value']
    
  elif target_name == "table":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['table_normalizing_factor_for_col_value'])
    
  elif target_name == "comments":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['comments_normalizing_factor_for_col_value']

  elif target_name == "price per carat":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['ppc_normalizing_factor_for_col_value']

  elif target_name == "discount":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['disc_normalizing_factor_for_col_value']
  
  elif target_name == "total":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['amt_normalizing_factor_for_col_value']
  
  elif target_name == "rap price total":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['raptotal_normalizing_factor_for_col_value']

  elif target_name == "Stock Ref":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['stockref_normalizing_factor_for_col_value']

  elif target_name == "report_no":
    final_similarity_score = sim_score_name + sim_score_val * magic_numbers['report_normalizing_factor_for_col_value']

#   elif target_name == "Cert":
#     final_similarity_score = sim_score_name + sim_score_val * magic_numbers['cert_normalizing_factor_for_col_value']

  else:
    raise Exception("The function could not find this target name")
  
  return round(final_similarity_score,3)
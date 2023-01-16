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

  # Setting Default value of need to continue to True
  need_to_continue = True

  # For Clarity
  if target_name == "clarity":

    if sim_score > magic_numbers['clarity_threshold']:
      need_to_continue = False
    else:
      sim_score = (sim_score / magic_numbers['clarity_normalizing_factor'])
    
  # For Carat
  elif target_name == "carat":
    sim_score *= magic_numbers['carat_enhancing_factor']

  # For Color
  elif target_name == "color":

    if sim_score > magic_numbers['color_threshold']:
      need_to_continue = False
    else:
      sim_score /= magic_numbers['color_normalizing_factor']
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      pass
  
  # For fluorescent
  elif target_name == "fluorescent":
    if sim_score > magic_numbers['fluor_similarity_threshold']:
      need_to_continue = True
    else:
      sim_score /= magic_numbers['fluor_normalizing_factor']
  
  # For raprate
  elif target_name == "raprate":
    if sim_score >= magic_numbers['raprate_threshold_factor']:
      need_to_continue = False
    else:
      sim_score *= magic_numbers['raprate_enhanching_factor']
  
  #For Cut
  elif target_name == "cut":

    if sim_score_val ==  1:
        final_similarity_score = sim_score_name + magic_numbers['cut_enhancing_factor']
    
    else:
        final_similarity_score = sim_score_name
      
  #For Polish
  elif target_name == "polish":

    if sim_score_val ==  1:
        final_similarity_score = sim_score_name + magic_numbers['polish_enhancing_factor']

    else:
        final_similarity_score = sim_score_name

  #For Symmetry
  elif target_name == "symmetry":

    if sim_score_val ==  1:
        final_similarity_score = sim_score_name + magic_numbers['sym_enhancing_factor']
    
    else:
        final_similarity_score = sim_score_name

  else:
    raise Exception("The function could not find this target name")
  
  return sim_score, need_to_continue

def merge_similarity_score(sim_score_name,sim_score_val, target_name,magic_numbers):
  """
  This functionm will merge similarity score calculated from column name and column values

  Args:
  sim_score_name: similarity score calculated from name
  sim_score_val: similarityb score calculated from value
  target_name: The name of target column
  magic_numbers(dict) = magic numbers in form of dictionary

  returns:
  final_similarity_score
  """

  # For Clarity
  if target_name == "clarity":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['clarity_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name

  # For Carat
  elif target_name == "carat":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['carat_normalizing_factor'])
  
  # For Color
  elif target_name == "color":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['color_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name
  
  # For shape (Modification Remaining and will be done in future)
  elif target_name == "shape":
      final_similarity_score = sim_score_name
  
  # Fluorescent
  elif target_name == "fluorescent":

    if sim_score_val ==  1:
      final_similarity_score = sim_score_name + magic_numbers['fluor_enhancing_factor']
    
    else:
      final_similarity_score = sim_score_name
  
  # Raprate
  elif target_name == "raprate":
    final_similarity_score = sim_score_name + (sim_score_val*magic_numbers['raprate_enhanching_factor'])
    
  #Cut 
  elif target_name == "cut":

        if sim_score_val ==  1:
            final_similarity_score = sim_score_name + magic_numbers['cut_enhancing_factor']
        
        else:
            final_similarity_score = sim_score_name
            
  #Polish      
   elif target_name == "polish":

        if sim_score_val ==  1:
            final_similarity_score = sim_score_name + magic_numbers['polish_enhancing_factor']

        else:
            final_similarity_score = sim_score_name

  #symmetry          
   elif target_name == "symmetry":

        if sim_score_val ==  1:
            final_similarity_score = sim_score_name + magic_numbers['sym_enhancing_factor']
        
        else:
            final_similarity_score = sim_score_name
    
  else:
    raise Exception("The function could not find this target name")
  
  return final_similarity_score
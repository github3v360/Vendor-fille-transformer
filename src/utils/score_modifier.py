def modify_sim_score_of_name(sim_score, target_name, magic_numbers):
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
    normalizing_factors = {
        "clarity": "clarity_normalizing_factor_for_col_name",
        "carat": "carat_normalizing_factor_for_col_name",
        "color": "color_normalizing_factor_for_col_name",
        "shape": "shape_normalizing_factor_for_col_name",
        "fluorescent": "fluor_normalizing_factor_for_col_name",
        "raprate": "raprate_normalizing_factor_for_col_name",
        "length": "measurement_normalizing_factor_for_col_name",
        "width": "measurement_normalizing_factor_for_col_name",
        "depth": "measurement_normalizing_factor_for_col_name",
        "cut": "cut_normalizing_factor_for_col_name",
        "polish": "polish_normalizing_factor_for_col_name",
        "symmetry": "sym_normalizing_factor_for_col_name",
        "table": "table_normalizing_factor_for_col_name",
        "comments": "comments_normalizing_factor_for_col_name",
        "price per carat": "ppc_normalizing_factor_for_col_name",
        "discount": "disc_normalizing_factor_for_col_name",
        "total": "amt_normalizing_factor_for_col_name",
        "rap price total": "raptotal_normalizing_factor_for_col_name",
        "Stock Ref": "stockref_normalizing_factor_for_col_name",
        "report_no": "report_normalizing_factor_for_col_name"
    }

    normalizing_factor = normalizing_factors.get(target_name)
    if normalizing_factor is None:
        raise Exception("The function could not find this target name")

    return round(sim_score * magic_numbers[normalizing_factor], 3)

def merge_similarity_score(sim_score_name, sim_score_val, target_name, magic_numbers):
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
    normalizing_factors = {
        "clarity": "clarity_normalizing_factor_for_col_value",
        "carat": "carat_normalizing_factor_for_col_value",
        "color": "color_normalizing_factor_for_col_value",
        "shape": "shape_normalizing_factor_for_col_value",
        "fluorescent": "fluor_normalizing_factor_for_col_value",
        "raprate": "raprate_normalizing_factor_for_col_value",
        "length": "measurement_normalizing_factor_for_col_value",
        "width": "measurement_normalizing_factor_for_col_value",
        "depth": "measurement_normalizing_factor_for_col_value",
        "cut": "cut_normalizing_factor_for_col_value",
        "polish": "polish_normalizing_factor_for_col_value",
        "symmetry": "sym_normalizing_factor_for_col_value",
        "table": "table_normalizing_factor_for_col_value",
        "comments": "comments_normalizing_factor_for_col_value",
        "price per carat": "ppc_normalizing_factor_for_col_value",
        "discount": "disc_normalizing_factor_for_col_value",
        "total": "amt_normalizing_factor_for_col_value",
        "rap price total": "raptotal_normalizing_factor_for_col_value",
        "Stock Ref": "stockref_normalizing_factor_for_col_value",
        "report_no": "report_normalizing_factor_for_col_value"
    }
    if target_name not in normalizing_factors:
        raise Exception("The function could not find this target name")
    normalizing_factor = magic_numbers.get(normalizing_factors[target_name])
    final_similarity_score = sim_score_name + sim_score_val * (normalizing_factor or 1)
    return round(final_similarity_score, 3)
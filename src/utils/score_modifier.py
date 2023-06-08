"""
This module contains utility functions for merging scores calculated from name and value.
"""

def merge_similarity_score(sim_score_name, sim_score_val, target_name, magic_numbers):
    """
    This function will merge similarity score calculated from column name and column values

    final_similarity_score = ( normalizing_factors_for_col_name * sim_score_name ) +
                             ( normalizing_factors_for_col_value * sim_score_value )

    Args:
        sim_score_name: similarity score calculated from name (float)
        sim_score_val: similarityb score calculated from value (float)
        target_name: The name of target column (String)
        magic_numbers: magic numbers in form of dictionary (dict)

    returns:
        final_similarity_score (float)
    """
    normalizing_factors_for_col_name = {
        "clarity": "clarity_normalizing_factor_for_col_name",
        "carat": "carat_normalizing_factor_for_col_name",
        "color": "color_normalizing_factor_for_col_name",
        "shape": "shape_normalizing_factor_for_col_name",
        "fluorescent": "fluor_normalizing_factor_for_col_name",
        "rapRate": "raprate_normalizing_factor_for_col_name",
        "length": "measurement_normalizing_factor_for_col_name",
        "width": "measurement_normalizing_factor_for_col_name",
        "depth": "measurement_normalizing_factor_for_col_name",
        "cut": "cut_normalizing_factor_for_col_name",
        "polish": "polish_normalizing_factor_for_col_name",
        "symmetry": "sym_normalizing_factor_for_col_name",
        "table": "table_normalizing_factor_for_col_name",
        "comments": "comments_normalizing_factor_for_col_name",
        "pricePerCarat": "ppc_normalizing_factor_for_col_name",
        "discount": "disc_normalizing_factor_for_col_name",
        "total": "amt_normalizing_factor_for_col_name",
        "rapPriceTotal": "raptotal_normalizing_factor_for_col_name",
        "stockRef": "stockref_normalizing_factor_for_col_name",
        "reportNo": "report_normalizing_factor_for_col_name"
    }

    normalizing_factors_for_col_value = {
        "clarity": "clarity_normalizing_factor_for_col_value",
        "carat": "carat_normalizing_factor_for_col_value",
        "color": "color_normalizing_factor_for_col_value",
        "shape": "shape_normalizing_factor_for_col_value",
        "fluorescent": "fluor_normalizing_factor_for_col_value",
        "rapRate": "raprate_normalizing_factor_for_col_value",
        "length": "measurement_normalizing_factor_for_col_value",
        "width": "measurement_normalizing_factor_for_col_value",
        "depth": "measurement_normalizing_factor_for_col_value",
        "cut": "cut_normalizing_factor_for_col_value",
        "polish": "polish_normalizing_factor_for_col_value",
        "symmetry": "sym_normalizing_factor_for_col_value",
        "table": "table_normalizing_factor_for_col_value",
        "comments": "comments_normalizing_factor_for_col_value",
        "pricePerCarat": "ppc_normalizing_factor_for_col_value",
        "discount": "disc_normalizing_factor_for_col_value",
        "total": "amt_normalizing_factor_for_col_value",
        "rapPriceTotal": "raptotal_normalizing_factor_for_col_value",
        "stockRef": "stockref_normalizing_factor_for_col_value",
        "reportNo": "report_normalizing_factor_for_col_value"
    }

    if target_name not in normalizing_factors_for_col_name:
        raise Exception("The function could not find this target name")

    weight_by_name = magic_numbers.get(normalizing_factors_for_col_name[target_name])
    weight_by_value = magic_numbers.get(normalizing_factors_for_col_value[target_name])

    final_similarity_score = (weight_by_name * sim_score_name) + (sim_score_val * weight_by_value)
    return round(final_similarity_score, 3)

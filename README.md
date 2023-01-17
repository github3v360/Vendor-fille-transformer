# Vendor-fille-transformer
A pipeline to transform the unstructured vendor file in to the desired format

# How to run this repository

## First Clone this repository

### Then run following commands

```
pip install -r equirements_for_local_machine.txt
python src/test_pipeline.py
```
### If you need to run your own file then run the following command
```
python src/main.py -f=your_file_path
```

# Similarity(Probability) Score Calculation Logic

### Let's take example of clarity 

sim_score_from_col_name = similarity score calculated from the column name

sim_score_from_col_val = similarity score calculated from the column name

clarity_normalizing_factor_for_col_name = weightage given to the "sim_score_from_col_name"

clarity_normalizing_factor_for_col_value = weightage given to the "sim_score_from_col_val"


Final_similarity_score = (sim_score_from_col_name*clarity_normalizing_factor_for_col_name) + 
                         (sim_score_from_col_val * clarity_normalizing_factor_for_col_value)
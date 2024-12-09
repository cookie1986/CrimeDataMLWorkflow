import os
import json
import pandas as pd
from src.data_processing import process_dataset, standardise_class_labels
from src.text_processing import process_texts_in_batches
from config.settings import settings


def main_pipeline(input_file, output_file, retain_original=False, rename_cols=True, y_name=None):
    # load and process the data
    cache_file = 'data/processed_data.csv'
    if not os.path.exists(cache_file):    
        data = process_dataset(
            input_file=input_file,
            output_file=output_file,
            retain_original=retain_original,
            rename_cols=rename_cols,
            y_name=y_name
        )  
        # process and clean the text data
        data['x1'] = process_texts_in_batches(data['x1'].tolist())
    else:
        data = pd.read_csv(cache_file)

    # standardise Y values
    with open(settings.REMAPPED_Y_VALS_JSON_FILE_PATH, 'r') as file:
        new_Y = json.load(file)
    updated_class_labels = standardise_class_labels(
        text_list = data["Y"].tolist(),
        mapping = new_Y
        )
    data["Y"] = updated_class_labels

    # save the final output for checking
    data.to_csv(cache_file,index=False)

    return data


if __name__ == "__main__":
    processed_data = main_pipeline(
        input_file='data/data.csv',
        output_file='data/processed_data.csv',
        retain_original=False,
        rename_cols=True,
        y_name='VIC OFFENDER RELATIONSHIP',
    )
    print(f"Processed DataFrame of type: {type(processed_data)}")
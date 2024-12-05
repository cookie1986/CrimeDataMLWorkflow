from src.data_processing import process_dataset
from src.text_processing import process_texts_in_batches


def main_pipeline(input_file, output_file, retain_original=False, rename_cols=True, y_name=None):
    # load and process the data    
    data = process_dataset(
        input_file=input_file,
        output_file=output_file,
        retain_original=retain_original,
        rename_cols=rename_cols,
        y_name=y_name
    )
    
    # process and clean the text data
    data['x1'] = process_texts_in_batches(data['x1'].tolist())

    # save the final output for checking
    data.to_csv('data/processed_data.csv',index=False)

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
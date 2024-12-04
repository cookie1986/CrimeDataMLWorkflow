from src.data_processing import process_dataset

process_dataset(
    input_file='data/data.csv',
    output_file='data/data.csv',
    retain_original=True,
    rename_cols=True,
    y_name='VIC OFFENDER RELATIONSHIP'
)
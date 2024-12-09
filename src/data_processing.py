import os
import pandas as pd
from config.settings import settings


def process_dataset(
        input_file: str,
        output_file: str,
        y_name: str,
        rename_cols: bool = True,
        retain_original: bool = False
):
    """
    Process the dataset by filtering columns, renaming them, removing blank rows and duplicates, and optionally retaining a copy of the original file.

    Args:
        input_file (str): Path to the input dataset.
        output_file (str): Path to save the processed dataset.
        rename_cols (bool): Whether to rename columns with a standard naming convention.
        retain_original (bool): Whether to retain the original dataset.

    Raises: 
        ValueError: If specified columns are missing from the dataset.
    """
    # load the dataset
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file does not exist: {input_file}")
    df = pd.read_csv(input_file)

    # save the original dataset if retaining
    original_file = f"{os.path.splitext(output_file)[0]}_original.csv"
    if retain_original:
        os.rename(input_file, original_file)
        print(f"Original dataset retained at: {original_file}")

    # filter on selected columns (specified in .env)
    if settings.FILTER_COLUMNS:
        missing_cols = [col for col in settings.FILTER_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"The following columns are missing from the dataset: {missing_cols}")
    df = df[settings.FILTER_COLUMNS]
    print(f"Shape of dataset after filtering columns: {df.shape}")

    # remove empty rows
    df = df.dropna(how="any")
    print(f"Length of dataset after removing empty rows: {len(df)}")

    # remove duplicate rows
    df = df.drop_duplicates()
    print(f"Length of dataset after removing duplicate rows: {len(df)}")

    # rename columns if enabled
    if rename_cols:
        column_mapping = standardise_column_names(df.columns, y_name)
        df = df.rename(columns=column_mapping)

    # save the processed dataset
    df.to_csv(output_file, index=False)

    return df


def standardise_column_names(
        columns: list,
        y_name: str
        ):
    """
    Generate new column names using a standard naming convention:
    - 'Y' for the target variable.
    - 'x1', 'x2', ..., for predictor variables.

    Args:
        columns (list): List of column names.
        y_name (str): The name of the target variable.

    Returns:
        dict: A mapping from original names to new names.
    """
    if len(columns) == 0:
        raise ValueError("No columns provided for renaming.")
    if y_name not in columns:
        raise ValueError(f"Target column '{y_name}' not found in the provided columns: {columns}")

    column_mapping = {}
    column_mapping[y_name] = "Y" # the target variable
    predictor_columns = [col for col in columns if col != y_name] # predictor variables
    for i, col in enumerate(predictor_columns, start=1):
        column_mapping[col] = f"x{i}"

    return column_mapping


def standardise_class_labels(text_list, mapping):
    """
    Standardise Y variable according to key-value pairs described in a corresponding JSON file.

    JSON Example:
        {
            "old_Y":"new_Y
        }

    Args:
        text_list (list): A list of labels
        mapping (dict): Key-value pairs of text to be remapped (values are the correct form)

    Returns:
        list: A list of corrected labels.
    """
    updated_text = []
    for text in text_list:
        for key, value in mapping.items():
            if key in text:
                text = text.replace(key, value)
        updated_text.append(text)
    return updated_text
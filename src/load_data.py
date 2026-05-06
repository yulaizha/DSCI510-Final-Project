"""
AI use note:
    Basic Python parts such as functions, if-statements, loops, file paths,
    and printing are written in a DSCI 510 course-style format.

    Reading CSV files with pandas is labeled with:
        # AI generated:
"""

import os
import pandas as pd

from config import (
    DATA_FOLDER,
    ALL_ELECTRONICS_CLEANED,
    HOME_ENTERTAINMENT_CLEANED,
    DUMMYJSON_CLEANED,
    AMAZON_BEST_SELLERS_CLEANED
)


# Helper functions
def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def print_dataset_preview(file_label, df):
    print(file_label)
    print("Shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())
    print()
    print("Preview:")
    print(df.head())
    print()
    print("=" * 60)
    print()

def get_final_cleaned_files():
    files = [
        ("All Electronics Cleaned", ALL_ELECTRONICS_CLEANED),
        ("Home Entertainment Cleaned", HOME_ENTERTAINMENT_CLEANED),
        ("DummyJSON Cleaned", DUMMYJSON_CLEANED),
        ("Amazon Best Sellers Cleaned", AMAZON_BEST_SELLERS_CLEANED)
    ]

    return files


# Main program
def main():
    files = get_final_cleaned_files()

    for file_label, file_name in files:
        file_path = os.path.join(DATA_FOLDER, file_name)

        if os.path.exists(file_path):
            df = load_csv_file(file_path)
            print_dataset_preview(file_label, df)
        else:
            print("Missing file:", file_path)
            print()
            print("=" * 60)
            print()

if __name__ == "__main__":
    main()
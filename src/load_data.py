# load_data.py

import os

import pandas as pd

def get_data_folder():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    data_folder = os.path.join(project_folder, "data")
    return data_folder

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
    print("\n" + "=" * 60 + "\n")

def main():
    data_folder = get_data_folder()

    files = [
        ("All Electronics Cleaned", "all_electronics_cleaned_for_final.csv"),
        ("Home Entertainment Cleaned", "home_entertainment_cleaned_for_final.csv"),
        ("DummyJSON Cleaned", "dummyjson_products_cleaned_for_final.csv"),
        ("Amazon Best Sellers Cleaned", "amazon_best_sellers_cleaned_for_final.csv")
    ]

    for file_label, file_name in files:
        file_path = os.path.join(data_folder, file_name)

        if os.path.exists(file_path):
            df = load_csv_file(file_path)
            print_dataset_preview(file_label, df)
        else:
            print("Missing file:", file_path)
            print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
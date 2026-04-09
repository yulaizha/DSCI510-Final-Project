# tests.py

import os
import pandas as pd

from api_fetch import fetch_dummyjson_products


def test_api_fetch():
    print("Running API fetch test...")
    df = fetch_dummyjson_products()

    print("API fetch successful.")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("-" * 60)


def test_existing_files():
    print("Checking whether key project files exist...")

    files_to_check = [
        "data/All_Electronics.csv",
        "data/Home_Entertainment_Systems.csv",
        "data/dummyjson_products.csv",
        "data/amazon_best_sellers_combined.csv",
        "data/final_cleaned_products.csv"
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"Found: {file_path}")
        else:
            print(f"Missing: {file_path}")

    print("-" * 60)


def test_final_cleaned_data():
    print("Reading final cleaned dataset...")

    df = pd.read_csv("data/final_cleaned_products.csv")

    print("Final cleaned dataset loaded successfully.")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("-" * 60)


if __name__ == "__main__":
    test_api_fetch()
    test_existing_files()
    test_final_cleaned_data()
    print("All tests finished.")
"""
AI use note:
    Basic Python parts such as functions, if-statements, loops, imports,
    and printing are written in a DSCI 510 course-style format.

    The schema and numeric validation checks are labeled with:
        # AI generated:
"""

import os
import sys
import pandas as pd


# Add src folder to Python path

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SRC_FOLDER = os.path.join(PROJECT_FOLDER, "src")

if SRC_FOLDER not in sys.path:
    sys.path.append(SRC_FOLDER)

# Import project functions and constants

from api_fetch import fetch_dummyjson_products

from config import (
    DATA_FOLDER,
    RESULTS_FOLDER,
    ALL_ELECTRONICS_CLEANED,
    HOME_ENTERTAINMENT_CLEANED,
    DUMMYJSON_CLEANED,
    AMAZON_BEST_SELLERS_CLEANED,
    DATASET_SUMMARY_OUTPUT,
    SOURCE_SUMMARY_OUTPUT,
    SUBCATEGORY_SUMMARY_OUTPUT,
    CORRELATION_OUTPUT,
    CORRELATION_BY_SOURCE_OUTPUT,
    HYPOTHESIS_TESTS_OUTPUT,
    LINEAR_REGRESSION_OUTPUT,
    VIF_OUTPUT,
    RANDOM_FOREST_RESULTS_OUTPUT,
    RANDOM_FOREST_FEATURE_IMPORTANCE_OUTPUT,
    API_COMPARISON_SUMMARY_OUTPUT,
    BEST_SELLERS_COMPARISON_SUMMARY_OUTPUT,
    WRITTEN_SUMMARY_OUTPUT
)


# Constants from config.py

FINAL_CLEANED_FILES = [
    ALL_ELECTRONICS_CLEANED,
    HOME_ENTERTAINMENT_CLEANED,
    DUMMYJSON_CLEANED,
    AMAZON_BEST_SELLERS_CLEANED
]

EXPECTED_FINAL_COLUMNS = [
    "product_name",
    "price",
    "rating",
    "review_count",
    "category",
    "subcategory",
    "source"
]

EXPECTED_API_COLUMNS = [
    "product_name",
    "price",
    "rating",
    "review_count",
    "category",
    "source"
]

EXPECTED_RESULT_FILES = [
    DATASET_SUMMARY_OUTPUT,
    SOURCE_SUMMARY_OUTPUT,
    SUBCATEGORY_SUMMARY_OUTPUT,
    CORRELATION_OUTPUT,
    CORRELATION_BY_SOURCE_OUTPUT,
    HYPOTHESIS_TESTS_OUTPUT,
    LINEAR_REGRESSION_OUTPUT,
    VIF_OUTPUT,
    RANDOM_FOREST_RESULTS_OUTPUT,
    RANDOM_FOREST_FEATURE_IMPORTANCE_OUTPUT,
    API_COMPARISON_SUMMARY_OUTPUT,
    BEST_SELLERS_COMPARISON_SUMMARY_OUTPUT,
    WRITTEN_SUMMARY_OUTPUT
]


# Helper functions

def print_line():
    print("-" * 60)


def get_data_file_path(file_name):
    return os.path.join(DATA_FOLDER, file_name)


def get_result_file_path(file_name):
    return os.path.join(RESULTS_FOLDER, file_name)


# Tests

def test_api_fetch():
    print("Running API fetch test...")

    df = fetch_dummyjson_products()

    assert df is not None
    assert len(df) > 0

    for column in EXPECTED_API_COLUMNS:
        assert column in df.columns, "API result is missing column: " + column

    print("API fetch test passed.")
    print("Shape:", df.shape)
    print_line()


def test_final_cleaned_files_exist():
    print("Checking whether final cleaned CSV files exist...")

    for file_name in FINAL_CLEANED_FILES:
        file_path = get_data_file_path(file_name)
        assert os.path.exists(file_path), "Missing file: " + file_path
        print("Found:", file_path)

    print("Final cleaned file existence test passed.")
    print_line()


# AI generated:
def test_final_cleaned_data_schema():
    print("Checking final cleaned data schema...")

    for file_name in FINAL_CLEANED_FILES:
        file_path = get_data_file_path(file_name)
        df = pd.read_csv(file_path)

        for column in EXPECTED_FINAL_COLUMNS:
            assert column in df.columns, file_name + " is missing column: " + column

        assert len(df) > 0, file_name + " has no rows"

        print(file_name)
        print("Shape:", df.shape)
        print("Columns OK")

    print("Final cleaned data schema test passed.")
    print_line()


# AI generated:
def test_numeric_columns():
    print("Checking numeric columns...")

    for file_name in FINAL_CLEANED_FILES:
        file_path = get_data_file_path(file_name)
        df = pd.read_csv(file_path)

        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")

        assert df["price"].notna().sum() > 0, file_name + " has no valid price values"
        assert df["rating"].notna().sum() > 0, file_name + " has no valid rating values"

        assert df["price"].min() >= 0, file_name + " has negative price values"
        assert df["rating"].min() >= 0, file_name + " has rating below 0"
        assert df["rating"].max() <= 5, file_name + " has rating above 5"

        # Amazon Best Sellers may have a few missing review_count values.
        valid_review_count = df["review_count"].dropna()
        if len(valid_review_count) > 0:
            assert valid_review_count.min() >= 0, file_name + " has negative review_count values"

        print(file_name, "numeric columns OK")

    print("Numeric column test passed.")
    print_line()


def test_final_result_files_exist():
    print("Checking whether final result files exist...")

    for file_name in EXPECTED_RESULT_FILES:
        file_path = get_result_file_path(file_name)
        assert os.path.exists(file_path), "Missing result file: " + file_path
        print("Found:", file_path)

    print("Final result file existence test passed.")
    print_line()


# Main program

def main():
    test_api_fetch()
    test_final_cleaned_files_exist()
    test_final_cleaned_data_schema()
    test_numeric_columns()
    test_final_result_files_exist()

    print("All tests finished.")


if __name__ == "__main__":
    main()

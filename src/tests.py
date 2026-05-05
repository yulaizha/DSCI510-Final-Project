import os
import pandas as pd

from api_fetch import fetch_dummyjson_products


def get_project_folder():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    return project_folder


def get_data_folder():
    project_folder = get_project_folder()
    data_folder = os.path.join(project_folder, "data")
    return data_folder


def test_api_fetch():
    print("Running API fetch test...")

    df = fetch_dummyjson_products()

    assert df is not None
    assert len(df) > 0

    expected_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "source"
    ]

    for column in expected_columns:
        assert column in df.columns

    print("API fetch test passed.")
    print("Shape:", df.shape)
    print("-" * 60)

def test_final_cleaned_files_exist():
    print("Checking whether final cleaned CSV files exist...")

    data_folder = get_data_folder()

    files_to_check = [
        "all_electronics_cleaned_for_final.csv",
        "home_entertainment_cleaned_for_final.csv",
        "dummyjson_products_cleaned_for_final.csv",
        "amazon_best_sellers_cleaned_for_final.csv"
    ]

    for file_name in files_to_check:
        file_path = os.path.join(data_folder, file_name)
        assert os.path.exists(file_path), "Missing file: " + file_path
        print("Found:", file_path)

    print("Final cleaned file existence test passed.")
    print("-" * 60)


# AI generated:
def test_final_cleaned_data_schema():
    print("Checking final cleaned data schema...")

    data_folder = get_data_folder()

    files_to_check = [
        "all_electronics_cleaned_for_final.csv",
        "home_entertainment_cleaned_for_final.csv",
        "dummyjson_products_cleaned_for_final.csv",
        "amazon_best_sellers_cleaned_for_final.csv"
    ]

    expected_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    for file_name in files_to_check:
        file_path = os.path.join(data_folder, file_name)
        df = pd.read_csv(file_path)

        for column in expected_columns:
            assert column in df.columns, file_name + " is missing column: " + column

        assert len(df) > 0, file_name + " has no rows"

        print(file_name)
        print("Shape:", df.shape)
        print("Columns OK")

    print("Final cleaned data schema test passed.")
    print("-" * 60)


# AI generated:
def test_numeric_columns():
    print("Checking numeric columns...")

    data_folder = get_data_folder()

    files_to_check = [
        "all_electronics_cleaned_for_final.csv",
        "home_entertainment_cleaned_for_final.csv",
        "dummyjson_products_cleaned_for_final.csv",
        "amazon_best_sellers_cleaned_for_final.csv"
    ]

    for file_name in files_to_check:
        file_path = os.path.join(data_folder, file_name)
        df = pd.read_csv(file_path)

        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")

        assert df["price"].notna().sum() > 0, file_name + " has no valid price values"
        assert df["rating"].notna().sum() > 0, file_name + " has no valid rating values"

        assert df["price"].min() >= 0, file_name + " has negative price values"
        assert df["rating"].min() >= 0, file_name + " has rating below 0"
        assert df["rating"].max() <= 5, file_name + " has rating above 5"

        print(file_name, "numeric columns OK")

    print("Numeric column test passed.")
    print("-" * 60)

if __name__ == "__main__":
    test_api_fetch()
    test_final_cleaned_files_exist()
    test_final_cleaned_data_schema()
    test_numeric_columns()

    print("All tests finished.")
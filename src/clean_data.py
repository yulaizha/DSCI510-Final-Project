"""
AI use note:
    Basic Python parts such as imports, variables, functions, if-statements,
    loops, file paths, and printing are written in a DSCI 510 course-style format.

    The data cleaning and standardization logic using pandas is labeled with:
        # AI generated:
"""

import os
import re
import pandas as pd

from config import (
    DATA_FOLDER,
    ALL_ELECTRONICS_RAW,
    HOME_ENTERTAINMENT_RAW,
    DUMMYJSON_RAW,
    DUMMYJSON_RAW_ALT_1,
    DUMMYJSON_RAW_ALT_2,
    AMAZON_BEST_SELLERS_RAW,
    AMAZON_BEST_SELLERS_RAW_ALT_1,
    ALL_ELECTRONICS_CLEANED,
    HOME_ENTERTAINMENT_CLEANED,
    DUMMYJSON_CLEANED,
    AMAZON_BEST_SELLERS_CLEANED,
    API_SOURCE,
    BEST_SELLERS_SOURCE
)


# Helper functions

def clean_text(value):
    if value is None:
        return ""

    value = str(value)
    value = " ".join(value.split())
    return value.strip()


# AI generated:
def clean_number(value):
    """
    Convert values such as "$1,299.99", "4.7 out of 5 stars",
    and "12,962 ratings" into numeric values.
    """
    if value is None:
        return None

    if pd.isna(value):
        return None

    value = str(value).replace(",", "")
    match = re.search(r"\d+\.\d+|\d+", value)

    if match:
        return float(match.group())
    else:
        return None


# AI generated:
def clean_review_count(value):
    """
    Convert review count values into integer-like numeric values.
    """
    number = clean_number(value)

    if number is None:
        return None
    else:
        return int(number)

def find_existing_file(possible_names):
    for file_name in possible_names:
        file_path = os.path.join(DATA_FOLDER, file_name)

        if os.path.exists(file_path):
            return file_path

    return None


def print_cleaning_summary(label, df):
    print()
    print(label)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Preview:")
    print(df.head(5))


# Cleaning All Electronics and Home Entertainment

# AI generated:
def clean_amazon_csv(df, source_name):
    """
    Clean one Kaggle Amazon CSV dataset and return a standardized DataFrame.

    Final columns:
        product_name
        price
        rating
        review_count
        category
        subcategory
        source
    """
    df_clean = df.rename(columns={
        "name": "product_name",
        "discount_price": "price",
        "ratings": "rating",
        "no_of_ratings": "review_count",
        "main_category": "category",
        "sub_category": "subcategory"
    })

    required_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory"
    ]

    for column in required_columns:
        if column not in df_clean.columns:
            df_clean[column] = None

    df_clean = df_clean[required_columns].copy()

    df_clean["product_name"] = df_clean["product_name"].apply(clean_text)
    df_clean["category"] = df_clean["category"].apply(clean_text)
    df_clean["subcategory"] = df_clean["subcategory"].apply(clean_text)

    df_clean["price"] = df_clean["price"].apply(clean_number)
    df_clean["rating"] = df_clean["rating"].apply(clean_number)
    df_clean["review_count"] = df_clean["review_count"].apply(clean_review_count)

    df_clean["source"] = source_name

    df_clean = df_clean.dropna(subset=["product_name", "price", "rating", "review_count"])
    df_clean = df_clean[df_clean["product_name"] != ""]
    df_clean = df_clean[df_clean["product_name"] != "nan"]
    df_clean = df_clean[df_clean["price"] >= 0]
    df_clean = df_clean[(df_clean["rating"] >= 0) & (df_clean["rating"] <= 5)]
    df_clean = df_clean[df_clean["review_count"] >= 0]
    df_clean = df_clean.drop_duplicates(subset=["product_name"], keep="first")

    final_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    df_clean = df_clean[final_columns].reset_index(drop=True)

    return df_clean


def clean_main_amazon_csv_files():
    all_electronics_file = os.path.join(DATA_FOLDER, ALL_ELECTRONICS_RAW)
    home_entertainment_file = os.path.join(DATA_FOLDER, HOME_ENTERTAINMENT_RAW)

    if not os.path.exists(all_electronics_file):
        print("Cannot find file:")
        print(all_electronics_file)
        return None, None

    if not os.path.exists(home_entertainment_file):
        print("Cannot find file:")
        print(home_entertainment_file)
        return None, None

    print("Reading:", all_electronics_file)
    all_electronics_raw = pd.read_csv(all_electronics_file)

    print("Reading:", home_entertainment_file)
    home_entertainment_raw = pd.read_csv(home_entertainment_file)

    # AI generated:
    all_electronics_cleaned = clean_amazon_csv(
        all_electronics_raw,
        "all_electronics_csv"
    )

    home_entertainment_cleaned = clean_amazon_csv(
        home_entertainment_raw,
        "home_entertainment_csv"
    )

    all_output = os.path.join(DATA_FOLDER, ALL_ELECTRONICS_CLEANED)
    home_output = os.path.join(DATA_FOLDER, HOME_ENTERTAINMENT_CLEANED)

    all_electronics_cleaned.to_csv(all_output, index=False)
    home_entertainment_cleaned.to_csv(home_output, index=False)

    print_cleaning_summary("All Electronics cleaned", all_electronics_cleaned)
    print_cleaning_summary("Home Entertainment cleaned", home_entertainment_cleaned)

    print("Saved file:", all_output)
    print("Saved file:", home_output)

    return all_electronics_cleaned, home_entertainment_cleaned


# Cleaning DummyJSON API data

# AI generated:
def clean_dummyjson_data(input_file, output_file):
    """
    Clean DummyJSON API product data.

    DummyJSON is used as an API-based comparison dataset.
    """
    df = pd.read_csv(input_file)

    print()
    print("Reading:", input_file)
    print("Original shape:", df.shape)
    print("Original columns:", list(df.columns))

    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    required_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "source"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["product_name"] = df["product_name"].apply(clean_text)
    df["category"] = df["category"].apply(clean_text)

    df["price"] = df["price"].apply(clean_number)
    df["rating"] = df["rating"].apply(clean_number)
    df["review_count"] = df["review_count"].apply(clean_review_count)

    df = df[df["product_name"] != ""]
    df = df.drop_duplicates(subset=["product_name"], keep="first")

    df = df[df["price"].notna()]
    df = df[df["rating"].notna()]
    df = df[df["review_count"].notna()]
    df = df[df["price"] >= 0]
    df = df[(df["rating"] >= 0) & (df["rating"] <= 5)]
    df = df[df["review_count"] >= 0]

    df["subcategory"] = "DummyJSON Products"
    df["source"] = API_SOURCE

    final_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    df = df[final_columns].reset_index(drop=True)

    df.to_csv(output_file, index=False)

    print_cleaning_summary("DummyJSON cleaned", df)
    print("Saved file:", output_file)

    return df


def clean_dummyjson_file():
    input_file = find_existing_file([
        DUMMYJSON_RAW_ALT_2,
        DUMMYJSON_RAW_ALT_1,
        DUMMYJSON_RAW
    ])

    if input_file is None:
        print("Cannot find a DummyJSON CSV file.")
        print("Expected one of these names:")
        print(DUMMYJSON_RAW_ALT_2)
        print(DUMMYJSON_RAW_ALT_1)
        print(DUMMYJSON_RAW)
        return None

    output_file = os.path.join(DATA_FOLDER, DUMMYJSON_CLEANED)

    print("Input file:", input_file)
    print("Output file:", output_file)

    return clean_dummyjson_data(input_file, output_file)

# Cleaning Amazon Best Sellers webpage data

# AI generated:
def clean_amazon_best_sellers_data(input_file, output_file):
    """
    Clean Amazon Best Sellers webpage scraped data.

    Main changes:
        product_category -> subcategory
        rating_count -> review_count
        category = electronics
        source = amazon_webpage
    """
    df = pd.read_csv(input_file)

    print()
    print("Reading:", input_file)
    print("Original shape:", df.shape)
    print("Original columns:", list(df.columns))

    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    if "product_category" in df.columns:
        df = df.rename(columns={"product_category": "subcategory"})

    if "rating_count" in df.columns:
        df = df.rename(columns={"rating_count": "review_count"})

    required_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "subcategory"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["product_name"] = df["product_name"].apply(clean_text)
    df["subcategory"] = df["subcategory"].apply(clean_text)

    df["price"] = df["price"].apply(clean_number)
    df["rating"] = df["rating"].apply(clean_number)
    df["review_count"] = df["review_count"].apply(clean_review_count)

    df = df[df["product_name"] != ""]
    df = df.drop_duplicates(subset=["product_name"], keep="first")

    df = df[df["price"].notna()]
    df = df[df["rating"].notna()]
    df = df[df["price"] >= 0]
    df = df[(df["rating"] >= 0) & (df["rating"] <= 5)]

    # Keep rows even if review_count is missing.
    df = df[(df["review_count"].isna()) | (df["review_count"] >= 0)]

    df["category"] = "electronics"
    df["source"] = BEST_SELLERS_SOURCE

    final_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    df = df[final_columns].reset_index(drop=True)

    df.to_csv(output_file, index=False)

    print_cleaning_summary("Amazon Best Sellers cleaned", df)
    print("Missing values after cleaning:")
    print(df.isna().sum())
    print("Saved file:", output_file)

    return df

def clean_amazon_best_sellers_file():
    input_file = find_existing_file([
        AMAZON_BEST_SELLERS_RAW_ALT_1,
        AMAZON_BEST_SELLERS_RAW
    ])

    if input_file is None:
        print("Cannot find Amazon Best Sellers scraped CSV file.")
        print("Expected one of these names:")
        print(AMAZON_BEST_SELLERS_RAW_ALT_1)
        print(AMAZON_BEST_SELLERS_RAW)
        return None

    output_file = os.path.join(DATA_FOLDER, AMAZON_BEST_SELLERS_CLEANED)

    print("Input file:", input_file)
    print("Output file:", output_file)

    return clean_amazon_best_sellers_data(input_file, output_file)

# Main program
def main():
    if not os.path.exists(DATA_FOLDER):
        print("Cannot find data folder:")
        print(DATA_FOLDER)
        return

    print("=" * 70)
    print("Starting data cleaning")
    print("=" * 70)

    all_electronics_cleaned, home_entertainment_cleaned = clean_main_amazon_csv_files()
    dummyjson_cleaned = clean_dummyjson_file()
    amazon_best_sellers_cleaned = clean_amazon_best_sellers_file()

    print()
    print("=" * 70)
    print("Cleaning complete")
    print("=" * 70)

    if all_electronics_cleaned is not None:
        print("All Electronics:", all_electronics_cleaned.shape)

    if home_entertainment_cleaned is not None:
        print("Home Entertainment:", home_entertainment_cleaned.shape)

    if dummyjson_cleaned is not None:
        print("DummyJSON:", dummyjson_cleaned.shape)

    if amazon_best_sellers_cleaned is not None:
        print("Amazon Best Sellers:", amazon_best_sellers_cleaned.shape)

if __name__ == "__main__":
    main()
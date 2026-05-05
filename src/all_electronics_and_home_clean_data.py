#!/usr/bin/env python3
"""
all_electronics_and_home_clean_data.py

DSCI 510 Final Project

Purpose:
    Clean the two main Amazon CSV datasets:
    1. All_Electronics.csv
    2. Home_Entertainment_Systems.csv

Input files in data/:
    data/All_Electronics.csv
    data/Home_Entertainment_Systems.csv

Output files in data/:
    data/all_electronics_cleaned_for_final.csv
    data/home_entertainment_cleaned_for_final.csv

How to run from the project folder:
    cd ~/Desktop/DSCI_510_Final_Project
    python3 src/all_electronics_and_home_clean_data.py

AI use note:
    Basic Python parts such as imports, variables, functions, if-statements,
    file paths, and printing are written in a DSCI 510 course-style format.

    The cleaning and standardization logic using pandas is labeled with:
        # AI generated:
"""

# Course-style part:
import os
import re

# AI generated:
import pandas as pd


# ============================================================
# 1. Helper functions
# ============================================================

# AI generated:
def clean_price(value):
    """
    Convert price values such as "$1,299.99" into numeric values.
    """
    if pd.isna(value):
        return None

    value = str(value).replace(",", "")
    match = re.search(r"\d+\.\d+|\d+", value)

    if match:
        return float(match.group())
    else:
        return None


# AI generated:
def clean_rating(value):
    """
    Convert rating values into numeric values.
    """
    if pd.isna(value):
        return None

    match = re.search(r"\d+\.\d+|\d+", str(value))

    if match:
        return float(match.group())
    else:
        return None


# AI generated:
def clean_review_count(value):
    """
    Convert review count values such as "1,234" into integer values.
    """
    if pd.isna(value):
        return None

    value = str(value).replace(",", "")
    match = re.search(r"\d+", value)

    if match:
        return int(match.group())
    else:
        return None


# Course-style part:
def get_data_folder():
    """
    This file is expected to be inside src/.
    The data folder is one level above src/.
    """
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    data_folder = os.path.join(project_folder, "data")
    return data_folder


# AI generated:
def clean_amazon_csv(df, source_name):
    """
    Clean one Amazon CSV dataset and return a standardized DataFrame.

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

    df_clean["product_name"] = df_clean["product_name"].astype(str).str.strip()
    df_clean["category"] = df_clean["category"].astype(str).str.strip()
    df_clean["subcategory"] = df_clean["subcategory"].astype(str).str.strip()

    df_clean["price"] = df_clean["price"].apply(clean_price)
    df_clean["rating"] = df_clean["rating"].apply(clean_rating)
    df_clean["review_count"] = df_clean["review_count"].apply(clean_review_count)

    df_clean["source"] = source_name

    # Remove missing or invalid values.
    df_clean = df_clean.dropna(subset=["product_name", "price", "rating", "review_count"])
    df_clean = df_clean[df_clean["product_name"] != ""]
    df_clean = df_clean[df_clean["product_name"] != "nan"]
    df_clean = df_clean[df_clean["price"] >= 0]
    df_clean = df_clean[(df_clean["rating"] >= 0) & (df_clean["rating"] <= 5)]
    df_clean = df_clean[df_clean["review_count"] >= 0]

    # Remove duplicate product names within this source.
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


# ============================================================
# 2. Main program
# ============================================================

# Course-style part:
def main():
    data_folder = get_data_folder()

    all_electronics_file = os.path.join(data_folder, "All_Electronics.csv")
    home_entertainment_file = os.path.join(data_folder, "Home_Entertainment_Systems.csv")

    if not os.path.exists(all_electronics_file):
        print("Cannot find file:")
        print(all_electronics_file)
        return

    if not os.path.exists(home_entertainment_file):
        print("Cannot find file:")
        print(home_entertainment_file)
        return

    print("Reading:", all_electronics_file)
    df1 = pd.read_csv(all_electronics_file)

    print("Reading:", home_entertainment_file)
    df2 = pd.read_csv(home_entertainment_file)

    # AI generated:
    df1_clean = clean_amazon_csv(df1, "all_electronics_csv")
    df2_clean = clean_amazon_csv(df2, "home_entertainment_csv")

    # Course-style part:
    all_output = os.path.join(data_folder, "all_electronics_cleaned_for_final.csv")
    home_output = os.path.join(data_folder, "home_entertainment_cleaned_for_final.csv")

    df1_clean.to_csv(all_output, index=False)
    df2_clean.to_csv(home_output, index=False)

    final_df = pd.concat(
        [df1_clean, df2_clean],
        ignore_index=True
    )

    print()
    print("df1_clean shape:", df1_clean.shape)
    print("df2_clean shape:", df2_clean.shape)
    print("combined shape:", final_df.shape)
    print()
    print("Final columns:")
    print(final_df.columns.tolist())
    print()
    print("Preview:")
    print(final_df.head(10))
    print()
    print("Saved file:", all_output)
    print("Saved file:", home_output)


# Course-style part:
if __name__ == "__main__":
    main()

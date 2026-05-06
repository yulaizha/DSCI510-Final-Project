"""
AI use note:
    Basic Python parts such as functions, if-statements, file paths, and printing
    are written in a DSCI 510 course-style format.

    The API request, JSON parsing, and DataFrame standardization logic are labeled with:
        # AI generated:
"""

import os
import requests
import pandas as pd

from config import (
    DATA_FOLDER,
    DUMMYJSON_API_URL,
    DUMMYJSON_RAW,
    API_SOURCE
)

# API fetch function

# AI generated:
def fetch_dummyjson_products():
    """
    Fetch product data from DummyJSON API and return a cleaned DataFrame.

    Final columns:
        product_name
        price
        rating
        review_count
        category
        source
    """
    response = requests.get(DUMMYJSON_API_URL)
    response.raise_for_status()

    data = response.json()
    products = data["products"]

    df = pd.DataFrame(products)

    clean_df = pd.DataFrame({
        "product_name": df["title"],
        "price": df["price"],
        "rating": df["rating"],
        "review_count": df["reviews"].apply(len),
        "category": df["category"],
        "source": API_SOURCE
    })

    return clean_df


# Save function

def save_dummyjson_products():
    """
    Fetch DummyJSON API data and save it to the data folder.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    output_file = os.path.join(DATA_FOLDER, DUMMYJSON_RAW)

    df = fetch_dummyjson_products()
    df.to_csv(output_file, index=False)

    print("DummyJSON API data saved successfully.")
    print("Output file:", output_file)
    print("Shape:", df.shape)
    print()
    print("Preview:")
    print(df.head())

    return df


# Main program

def main():
    save_dummyjson_products()

if __name__ == "__main__":
    main()
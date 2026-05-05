import os
import re
import pandas as pd

# Helper functions

def clean_text(value):
    """
    Clean text by removing extra spaces.
    """
    if value is None:
        return ""

    value = str(value)
    value = " ".join(value.split())
    return value.strip()


def clean_number(value):
    if value is None:
        return None

    value = str(value).replace(",", "")
    match = re.search(r"\d+\.\d+|\d+", value)

    if match:
        return float(match.group())
    else:
        return None


def find_input_file(data_folder):
    possible_names = [
        "amazon_best_sellers_web_scraped(1).csv",
        "amazon_best_sellers_web_scraped.csv"
    ]

    for file_name in possible_names:
        file_path = os.path.join(data_folder, file_name)

        if os.path.exists(file_path):
            return file_path

    return None

# Main cleaning function

# AI generated:
def clean_amazon_best_sellers_data(input_file, output_file):
    """
    Clean Amazon Best Sellers webpage scraped data.

    Cleaning steps:
    1. Read the CSV file.
    2. Standardize column names.
    3. Rename product_category to subcategory.
    4. Rename rating_count to review_count.
    5. Clean text columns.
    6. Convert price, rating, and review_count to numeric values.
    7. Remove duplicated product names.
    8. Add category = "electronics".
    9. Add source = "amazon_webpage".
    10. Remove columns not used in final statistical analysis.
    11. Save the cleaned CSV file into the data folder.
    """
    df = pd.read_csv(input_file)

    print("Original shape:", df.shape)
    print("Original columns:", list(df.columns))

    # Standardize column names.
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    # Rename columns to match the two cleaned Amazon CSV files.
    if "product_category" in df.columns:
        df = df.rename(columns={"product_category": "subcategory"})

    if "rating_count" in df.columns:
        df = df.rename(columns={"rating_count": "review_count"})

    # Make sure required columns exist.
    required_columns = ["product_name", "price", "rating", "review_count", "subcategory"]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # Clean text columns.
    df["product_name"] = df["product_name"].apply(clean_text)
    df["subcategory"] = df["subcategory"].apply(clean_text)

    # Clean numeric columns.
    df["price"] = df["price"].apply(clean_number)
    df["rating"] = df["rating"].apply(clean_number)
    df["review_count"] = df["review_count"].apply(clean_number)

    # Remove rows without product names.
    df = df[df["product_name"] != ""]

    # Remove duplicated product names.
    df = df.drop_duplicates(subset=["product_name"], keep="first")

    # Keep reasonable values.
    df = df[df["price"].notna()]
    df = df[df["rating"].notna()]
    df = df[df["price"] >= 0]
    df = df[(df["rating"] >= 0) & (df["rating"] <= 5)]

    # Keep review_count as missing if it is missing.
    # There are only a small number of missing review_count values in this file.
    # Later analysis code can drop missing values only when review_count is needed.
    df = df[(df["review_count"].isna()) | (df["review_count"] >= 0)]

    # Add category and source to match the final project data structure.
    df["category"] = "electronics"
    df["source"] = "amazon_webpage"

    # Reorder columns to match the two cleaned Amazon CSV files.
    final_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    df = df[final_columns]

    # Save cleaned file in the data folder.
    df.to_csv(output_file, index=False)

    print("Cleaned shape:", df.shape)
    print("Missing values after cleaning:")
    print(df.isna().sum())
    print("Cleaned file saved to:", output_file)

    print()
    print("Preview:")
    print(df.head(10))

# Main program
def main():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    data_folder = os.path.join(project_folder, "data")

    if not os.path.exists(data_folder):
        print("Cannot find data folder:")
        print(data_folder)
        return

    input_file = find_input_file(data_folder)

    if input_file is None:
        print("Cannot find the Amazon Best Sellers scraped CSV file in the data folder.")
        print("Expected one of these names:")
        print("amazon_best_sellers_web_scraped(1).csv")
        print("amazon_best_sellers_web_scraped.csv")
        return

    output_file = os.path.join(data_folder, "amazon_best_sellers_cleaned_for_final.csv")

    print("Input file:", input_file)
    print("Output file:", output_file)
    print()

    clean_amazon_best_sellers_data(input_file, output_file)


if __name__ == "__main__":
    main()
import os
import re
import pandas as pd


# Helper functions
def clean_text(value):
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
        "dummyjson_products(2).csv",
        "dummyjson_products(1).csv",
        "dummyjson_products.csv"
    ]

    for file_name in possible_names:
        file_path = os.path.join(data_folder, file_name)

        if os.path.exists(file_path):
            return file_path

    return None

# Main cleaning function
# AI generated:
def clean_dummyjson_data(input_file, output_file):
    df = pd.read_csv(input_file)

    print("Original shape:", df.shape)
    print("Original columns:", list(df.columns))

    # Standardize column names.
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    # Make sure required columns exist.
    required_columns = ["product_name", "price", "rating", "review_count", "category", "source"]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # Clean text columns.
    df["product_name"] = df["product_name"].apply(clean_text)
    df["category"] = df["category"].apply(clean_text)

    # Clean numeric columns.
    df["price"] = df["price"].apply(clean_number)
    df["rating"] = df["rating"].apply(clean_number)
    df["review_count"] = df["review_count"].apply(clean_number)

    # Remove rows without product names.
    df = df[df["product_name"] != ""]

    # Remove duplicate product names.
    df = df.drop_duplicates(subset=["product_name"], keep="first")

    df = df[df["price"].notna()]
    df = df[df["rating"].notna()]
    df = df[df["review_count"].notna()]
    df = df[df["price"] >= 0]
    df = df[(df["rating"] >= 0) & (df["rating"] <= 5)]
    df = df[df["review_count"] >= 0]

    df["subcategory"] = "DummyJSON Products"

    # Standardize source name.
    df["source"] = "dummyjson_api"

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

    # Save cleaned file
    df.to_csv(output_file, index=False)

    print("Cleaned shape:", df.shape)
    print("Cleaned file saved to:", output_file)

    print()
    print("Preview:")
    print(df.head(10))


# Main program
def main():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_folder, "data")
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    data_folder = os.path.join(project_folder, "data")

    if not os.path.exists(data_folder):
        print("Cannot find data folder:")
        print(data_folder)
        return

    input_file = find_input_file(data_folder)

    if input_file is None:
        print("Cannot find a DummyJSON CSV file in the data folder.")
        print("Expected one of these names:")
        print("dummyjson_products(2).csv")
        print("dummyjson_products(1).csv")
        print("dummyjson_products.csv")
        return

    output_file = os.path.join(data_folder, "dummyjson_products_cleaned_for_final.csv")

    print("Input file:", input_file)
    print("Output file:", output_file)
    print()

    clean_dummyjson_data(input_file, output_file)


if __name__ == "__main__":
    main()
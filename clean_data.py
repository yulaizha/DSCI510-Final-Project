# clean_data.py

import pandas as pd
import re

def clean_price(value):
    if pd.isna(value):
        return None
    value = str(value).replace(",", "")
    match = re.search(r"\d+\.\d+|\d+", value)
    return float(match.group()) if match else None

def clean_rating(value):
    if pd.isna(value):
        return None
    match = re.search(r"\d+\.\d+|\d+", str(value))
    return float(match.group()) if match else None

def clean_review_count(value):
    if pd.isna(value):
        return None
    value = str(value).replace(",", "")
    match = re.search(r"\d+", value)
    return int(match.group()) if match else None

# Load datasets
df1 = pd.read_csv("data/All_Electronics.csv")
df2 = pd.read_csv("data/Home_Entertainment_Systems.csv")
df3 = pd.read_csv("data/dummyjson_products.csv")
df4 = pd.read_csv("data/amazon_best_sellers_combined.csv")

# All Electronics
df1_clean = df1.rename(columns={
    "name": "product_name",
    "discount_price": "price",
    "ratings": "rating",
    "no_of_ratings": "review_count",
    "main_category": "category",
    "sub_category": "subcategory"
})

df1_clean = df1_clean[[
    "product_name", "price", "rating", "review_count", "category", "subcategory"
]].copy()

df1_clean["price"] = df1_clean["price"].apply(clean_price)
df1_clean["rating"] = df1_clean["rating"].apply(clean_rating)
df1_clean["review_count"] = df1_clean["review_count"].apply(clean_review_count)
df1_clean["source"] = "all_electronics_csv"

# Home Entertainment Systems
df2_clean = df2.rename(columns={
    "name": "product_name",
    "discount_price": "price",
    "ratings": "rating",
    "no_of_ratings": "review_count",
    "main_category": "category",
    "sub_category": "subcategory"
})

df2_clean = df2_clean[[
    "product_name", "price", "rating", "review_count", "category", "subcategory"
]].copy()

df2_clean["price"] = df2_clean["price"].apply(clean_price)
df2_clean["rating"] = df2_clean["rating"].apply(clean_rating)
df2_clean["review_count"] = df2_clean["review_count"].apply(clean_review_count)
df2_clean["source"] = "home_entertainment_csv"

# Dummyjson Products
df3_clean = df3.copy()

if "subcategory" not in df3_clean.columns:
    df3_clean["subcategory"] = None

df3_clean = df3_clean[[
    "product_name", "price", "rating", "review_count", "category", "subcategory", "source"
]].copy()

df3_clean["price"] = df3_clean["price"].apply(clean_price)
df3_clean["rating"] = df3_clean["rating"].apply(clean_rating)
df3_clean["review_count"] = df3_clean["review_count"].apply(clean_review_count)

# Amazon Best Seller
df4_clean = df4.copy()

df4_clean = df4_clean[[
    "product_name", "price", "rating", "review_count", "category", "subcategory", "source"
]].copy()

df4_clean["price"] = df4_clean["price"].apply(clean_price)
df4_clean["rating"] = df4_clean["rating"].apply(clean_rating)
df4_clean["review_count"] = df4_clean["review_count"].apply(clean_review_count)

# Combine
final_df = pd.concat(
    [df1_clean, df2_clean, df3_clean, df4_clean],
    ignore_index=True
)

final_df = final_df.drop_duplicates(subset=["product_name", "source"]).reset_index(drop=True)

# Summary
print("df1_clean shape:", df1_clean.shape)
print("df2_clean shape:", df2_clean.shape)
print("df3_clean shape:", df3_clean.shape)
print("df4_clean shape:", df4_clean.shape)
print("final_df shape:", final_df.shape)
print("\nFinal columns:")
print(final_df.columns.tolist())
print("\nPreview:")
print(final_df.head(10))

final_df.to_csv("data/final_cleaned_products.csv", index=False)
print("\nSaved file: data/final_cleaned_products.csv")
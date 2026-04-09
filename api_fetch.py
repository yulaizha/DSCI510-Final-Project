# api_fetch.py

import requests
import pandas as pd

def fetch_dummyjson_products():
    url = "https://dummyjson.com/products?limit=0"
    response = requests.get(url)
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
        "source": "dummyjson_api"
    })

    return clean_df

if __name__ == "__main__":
    df = fetch_dummyjson_products()
    print(df.head())
    print("Shape:", df.shape)
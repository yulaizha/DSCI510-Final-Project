# load_data.py

import pandas as pd

file1 = "data/All_Electronics.csv"
file2 = "data/Home_Entertainment_Systems.csv"
file3 = "data/dummyjson_products.csv"
file4 = "data/amazon_best_sellers_combined.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)

print("All_Electronics.csv")
print(df1.columns.tolist())
print(df1.head())
print("\n" + "=" * 60 + "\n")

print("Home_Entertainment_Systems.csv")
print(df2.columns.tolist())
print(df2.head())
print("\n" + "=" * 60 + "\n")

print("dummyjson_products.csv")
print(df3.columns.tolist())
print(df3.head())
print("\n" + "=" * 60 + "\n")

print("amazon_best_sellers_combined.csv")
print(df4.columns.tolist())
print(df4.head())
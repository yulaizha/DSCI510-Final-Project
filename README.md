# DSCI 510 Final Project Progress

## Project Title
Online Product Ratings and Pricing Analysis for Amazon Electronics Products

## Project Overview
This project analyzes the relationship between product prices, customer ratings, and review counts in Amazon-related electronics products. The goal is to explore how pricing and customer feedback may relate to product popularity and performance in the online retail market.

## Data Sources
The project currently uses four data sources:

1. `All_Electronics.csv`
2. `Home_Entertainment_Systems.csv`
3. `dummyjson_products.csv` (API-based source)
4. `amazon_best_sellers_combined.csv` (Amazon Best Sellers webpage data)

These datasets were cleaned and combined into one final dataset:  
`final_cleaned_products.csv`

## Current Progress
So far, the project has completed the following tasks:

- Organized the project folder structure
- Loaded two original CSV datasets
- Added one API-based data source using DummyJSON
- Built a scraper for Amazon Best Sellers pages
- Collected and merged webpage data from three Amazon subcategory pages
- Cleaned and standardized all datasets into a unified format
- Created a final cleaned dataset with 18,016 records

## Project Files
- `api_fetch.py` – fetches product data from the DummyJSON API
- `amazon_scrape.py` – collects Amazon Best Sellers webpage data
- `load_data.py` – loads and previews the datasets
- `clean_data.py` – cleans and combines all datasets
- `tests.py` – runs project tests

## How to Run
Install required packages first:

```bash
pip install -r requirements.txt
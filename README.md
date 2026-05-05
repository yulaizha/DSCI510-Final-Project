# DSCI 510 Final Project

## Project Title

Online Product Ratings and Pricing Analysis for Amazon Electronics Products

## Project Overview

This project analyzes online product data from Amazon-related electronics datasets, Amazon Best Sellers web pages, and the DummyJSON API. The main goal is to explore the relationship between product price, customer rating, review count, product source, and product category.

The project starts with several raw data sources, cleans and standardizes them into a common format, and then performs exploratory data analysis, statistical testing, regression modeling, and machine learning analysis. The final analysis helps answer whether price and review count are strongly related to product rating, and whether different data sources show different product patterns.

## Research Questions

This project focuses on the following questions:

1. What is the relationship between product price and customer rating?
2. What is the relationship between review count and customer rating?
3. Do different product data sources show different rating and price patterns?
4. Can price, review count, source, and subcategory be used to predict customer rating?

## Data Sources

This project uses four main data sources:

1. `All_Electronics.csv`  
   A CSV dataset containing Amazon electronics product information.

2. `Home_Entertainment_Systems.csv`  
   A CSV dataset containing Amazon home entertainment product information.

3. DummyJSON API  
   An API-based product dataset collected from DummyJSON.

4. Amazon Best Sellers Web Pages  
   Web-scraped product data from Amazon Best Sellers electronics-related pages.

The final project uses cleaned versions of these datasets. The raw `data/` folder is not included in this repository because it contains local data files. Users need to create a `data/` folder and place the required CSV files inside before running the scripts.

## Project Structure

```text
DSCI510-Final-Project/
│
├── README.md
├── requirements.txt
├── .gitignore
├── Final_Presentation_Yulai_Zhang.pdf
│
├── doc/
│   └── project documents and reports
│
├── src/
│   ├── api_fetch.py
│   ├── amazon_web_scraper_with_rating_v3.py
│   ├── all_electronics_and_home_clean_data.py
│   ├── clean_amazon_best_sellers.py
│   ├── clean_dummyjson_products.py
│   ├── load_data.py
│   ├── final_analysis.py
│   └── tests.py
│
├── data/
│   └── local input and cleaned CSV files
│
└── results/
    └── generated analysis tables, plots, and model outputs
```

The `data/` and `results/` folders are ignored by GitHub through `.gitignore`.

## Required Packages

The required Python packages are listed in `requirements.txt`.

To install them, run:

```bash
pip install -r requirements.txt
```

The main packages used in this project are:

```text
pandas
numpy
matplotlib
scipy
statsmodels
scikit-learn
requests
beautifulsoup4
lxml
```

## How to Run the Project

Run the scripts from the main project folder.

First, go to the project folder:

```bash
cd ~/Desktop/DSCI_510_Final_Project
```

Then run the scripts in this order:

```bash
python3 src/api_fetch.py
python3 src/amazon_web_scraper_with_rating_v3.py
python3 src/all_electronics_and_home_clean_data.py
python3 src/clean_amazon_best_sellers.py
python3 src/clean_dummyjson_products.py
python3 src/load_data.py
python3 src/final_analysis.py
python3 src/tests.py
```

## Description of Python Files

### `api_fetch.py`

This script collects product data from the DummyJSON API. It extracts product name, price, rating, review count, category, and source information.

### `amazon_web_scraper_with_rating_v3.py`

This script scrapes Amazon Best Sellers electronics-related pages. It collects product name, product category, price, rating, rating count, best seller rank, and source URL.

### `all_electronics_and_home_clean_data.py`

This script cleans the two original Amazon CSV datasets:

- `All_Electronics.csv`
- `Home_Entertainment_Systems.csv`

It standardizes column names and creates cleaned CSV files for the final analysis.

### `clean_amazon_best_sellers.py`

This script cleans the Amazon Best Sellers web-scraped dataset. It standardizes columns, cleans numeric values, removes duplicates, and saves a cleaned CSV file.

### `clean_dummyjson_products.py`

This script cleans the DummyJSON API product dataset. It standardizes columns, checks numeric values, removes invalid rows, and saves a cleaned CSV file.

### `load_data.py`

This script loads and previews the cleaned datasets. It is mainly used to check whether the cleaned files have the expected columns and rows.

### `final_analysis.py`

This is the main final analysis script. It combines the cleaned datasets and performs:

- dataset summary analysis
- source-level comparison
- subcategory-level summary
- price and rating visualization
- Pearson and Spearman correlation analysis
- hypothesis testing
- multiple linear regression
- VIF analysis
- regression diagnostic plots
- Random Forest regression
- API vs Amazon source comparison
- written final summary generation

### `tests.py`

This script tests whether the API fetch works, whether the cleaned CSV files exist, whether the final cleaned files have the correct schema, and whether numeric columns are valid.

## Main Analysis Methods

The final analysis includes both statistical and machine learning methods.

The exploratory analysis summarizes price, rating, review count, source, and subcategory patterns. Since price and review count are right-skewed, the final analysis also uses log transformations.

The correlation analysis uses both Pearson correlation and Spearman correlation. Pearson correlation is used for linear relationships, while Spearman correlation is useful for rank-based relationships and skewed variables.

The hypothesis testing section compares different groups of products, such as Amazon CSV data, Amazon Best Sellers web data, and DummyJSON API data. Welch's t-test and Mann-Whitney U test are used for group comparisons.

The regression section uses multiple linear regression to examine whether log price, log review count, and source are related to product rating. VIF is also used to check multicollinearity.

The machine learning section uses Random Forest regression to predict product rating based on log price, log review count, source, and subcategory.

## Expected Outputs

The project generates cleaned CSV files in the `data/` folder and analysis outputs in the `results/` folder.

Examples of generated outputs include:

```text
final_combined_products_final.csv
dataset_summary_final.csv
source_summary_final.csv
subcategory_summary_final.csv
correlation_results_final.csv
correlation_by_source_final.csv
hypothesis_tests_final.csv
linear_regression_summary_final.txt
vif_results_final.csv
random_forest_results_final.csv
random_forest_feature_importance_final.csv
written_summary_final.txt
```

The project also generates several PNG visualizations, including:

```text
price_distribution_final.png
rating_distribution_final.png
price_vs_rating_final.png
reviewcount_vs_rating_final.png
average_price_by_source_final.png
average_rating_by_source_final.png
product_count_by_source_final.png
log_price_by_source_final.png
rating_by_source_final.png
regression_residuals_vs_fitted_final.png
regression_residual_histogram_final.png
regression_qq_plot_final.png
random_forest_feature_importance_final.png
```

## Testing

To run the project tests, use:

```bash
python3 src/tests.py
```

The tests check:

1. Whether the DummyJSON API fetch returns valid data.
2. Whether the cleaned CSV files exist.
3. Whether the cleaned files have the required columns.
4. Whether price, rating, and review count are valid numeric columns.

## AI Use Note

AI tools were used to help improve parts of the project code structure, data cleaning logic, analysis workflow, and debugging process. Basic Python structure, file organization, and project logic were reviewed and adapted by the student. AI-generated or AI-assisted sections were marked in the Python files when appropriate.

## Limitations

This project has several limitations. First, the Amazon web scraping results may change over time because Amazon pages are dynamic and may block or limit automated scraping. Second, the datasets come from different sources, so their product coverage and data collection methods are not exactly the same. Third, customer rating is affected by many factors that are not included in this project, such as brand reputation, product quality, shipping experience, and customer expectations. Because of this, the regression and machine learning models may have limited predictive power.

## Conclusion

This project shows that online product rating patterns are more complex than a simple price-rating relationship. Price and review count provide useful information, but they cannot fully explain customer rating. The comparison across Amazon CSV data, Amazon Best Sellers web data, and DummyJSON API data also shows that different data sources can have different product patterns. Overall, this project demonstrates a complete data science workflow, including data collection, data cleaning, exploratory analysis, statistical testing, regression modeling, machine learning, and result interpretation.

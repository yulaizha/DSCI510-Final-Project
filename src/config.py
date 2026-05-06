import os

# Project folders
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_FOLDER, "data")
RESULTS_FOLDER = os.path.join(PROJECT_FOLDER, "results")
DOCS_FOLDER = os.path.join(PROJECT_FOLDER, "docs")


# Raw data file names
ALL_ELECTRONICS_RAW = "All_Electronics.csv"
HOME_ENTERTAINMENT_RAW = "Home_Entertainment_Systems.csv"

DUMMYJSON_RAW = "dummyjson_products.csv"
DUMMYJSON_RAW_ALT_1 = "dummyjson_products(1).csv"
DUMMYJSON_RAW_ALT_2 = "dummyjson_products(2).csv"

AMAZON_BEST_SELLERS_RAW = "amazon_best_sellers_web_scraped.csv"
AMAZON_BEST_SELLERS_RAW_ALT_1 = "amazon_best_sellers_web_scraped(1).csv"


# Cleaned data file names
ALL_ELECTRONICS_CLEANED = "all_electronics_cleaned_for_final.csv"
HOME_ENTERTAINMENT_CLEANED = "home_entertainment_cleaned_for_final.csv"
DUMMYJSON_CLEANED = "dummyjson_products_cleaned_for_final.csv"
AMAZON_BEST_SELLERS_CLEANED = "amazon_best_sellers_cleaned_for_final.csv"

FINAL_COMBINED_OUTPUT = "final_combined_products_final.csv"


# API constants
DUMMYJSON_API_URL = "https://dummyjson.com/products?limit=0"


# Amazon web scraping constants
PAGES_PER_CATEGORY = 2
TARGET_ROWS = 300

# AI generated:
# These URLs are Amazon Best Sellers category pages used for web scraping.
AMAZON_CATEGORY_URLS = [
    {
        "product_category": "Electronics",
        "base_url": "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics"
    },
    {
        "product_category": "Cell Phones & Accessories",
        "base_url": "https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless"
    },
    {
        "product_category": "Computers & Accessories",
        "base_url": "https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc"
    },
    {
        "product_category": "Camera & Photo",
        "base_url": "https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Products/zgbs/electronics/502394"
    },
    {
        "product_category": "Headphones & Earbuds",
        "base_url": "https://www.amazon.com/Best-Sellers-Electronics-Headphones-Earbuds/zgbs/electronics/172541"
    },
    {
        "product_category": "Televisions & Video Products",
        "base_url": "https://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011"
    }
]


# Source labels and groups
SOURCE_LABELS = {
    "all_electronics_csv": "All Electronics CSV",
    "home_entertainment_csv": "Home Entertainment CSV",
    "amazon_webpage": "Amazon Best Sellers Web",
    "dummyjson_api": "DummyJSON API"
}

MAIN_AMAZON_SOURCES = ["all_electronics_csv", "home_entertainment_csv"]
AMAZON_SOURCES = ["all_electronics_csv", "home_entertainment_csv", "amazon_webpage"]
API_SOURCE = "dummyjson_api"
BEST_SELLERS_SOURCE = "amazon_webpage"

# Result file names
DATASET_SUMMARY_OUTPUT = "dataset_summary_final.csv"
SOURCE_SUMMARY_OUTPUT = "source_summary_final.csv"
SUBCATEGORY_SUMMARY_OUTPUT = "subcategory_summary_final.csv"

CORRELATION_OUTPUT = "correlation_results_final.csv"
CORRELATION_BY_SOURCE_OUTPUT = "correlation_by_source_final.csv"
HYPOTHESIS_TESTS_OUTPUT = "hypothesis_tests_final.csv"

LINEAR_REGRESSION_OUTPUT = "linear_regression_summary_final.txt"
VIF_OUTPUT = "vif_results_final.csv"

RANDOM_FOREST_RESULTS_OUTPUT = "random_forest_results_final.csv"
RANDOM_FOREST_FEATURE_IMPORTANCE_OUTPUT = "random_forest_feature_importance_final.csv"

API_COMPARISON_SUMMARY_OUTPUT = "api_comparison_summary_final.csv"
BEST_SELLERS_COMPARISON_SUMMARY_OUTPUT = "best_sellers_comparison_summary_final.csv"
WRITTEN_SUMMARY_OUTPUT = "written_summary_final.txt"

# Plot file names
PRICE_DISTRIBUTION_PLOT = "price_distribution_final.png"
RATING_DISTRIBUTION_PLOT = "rating_distribution_final.png"
PRICE_VS_RATING_PLOT = "price_vs_rating_final.png"
REVIEWCOUNT_VS_RATING_PLOT = "reviewcount_vs_rating_final.png"

AVERAGE_PRICE_BY_SOURCE_PLOT = "average_price_by_source_final.png"
AVERAGE_RATING_BY_SOURCE_PLOT = "average_rating_by_source_final.png"
PRODUCT_COUNT_BY_SOURCE_PLOT = "product_count_by_source_final.png"

LOG_PRICE_BY_SOURCE_PLOT = "log_price_by_source_final.png"
RATING_BY_SOURCE_PLOT = "rating_by_source_final.png"

REGRESSION_RESIDUALS_VS_FITTED_PLOT = "regression_residuals_vs_fitted_final.png"
REGRESSION_RESIDUAL_HISTOGRAM_PLOT = "regression_residual_histogram_final.png"
REGRESSION_QQ_PLOT = "regression_qq_plot_final.png"

RANDOM_FOREST_FEATURE_IMPORTANCE_PLOT = "random_forest_feature_importance_final.png"
API_COMPARISON_AVERAGE_RATING_PLOT = "api_comparison_average_rating_final.png"
BEST_SELLERS_AVERAGE_RATING_PLOT = "best_sellers_average_rating_final.png"


# Model constants
TEST_SIZE = 0.2
RANDOM_STATE = 42
RANDOM_FOREST_N_ESTIMATORS = 100
RANDOM_FOREST_MAX_DEPTH = 10
SIGNIFICANCE_LEVEL = 0.05
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from config import (
    DATA_FOLDER,
    RESULTS_FOLDER,
    PROJECT_FOLDER,
    ALL_ELECTRONICS_CLEANED,
    HOME_ENTERTAINMENT_CLEANED,
    AMAZON_BEST_SELLERS_CLEANED,
    DUMMYJSON_CLEANED,
    FINAL_COMBINED_OUTPUT,
    SOURCE_LABELS,
    MAIN_AMAZON_SOURCES,
    AMAZON_SOURCES,
    API_SOURCE,
    BEST_SELLERS_SOURCE,
    DATASET_SUMMARY_OUTPUT,
    SOURCE_SUMMARY_OUTPUT,
    SUBCATEGORY_SUMMARY_OUTPUT,
    CORRELATION_OUTPUT,
    CORRELATION_BY_SOURCE_OUTPUT,
    HYPOTHESIS_TESTS_OUTPUT,
    LINEAR_REGRESSION_OUTPUT,
    VIF_OUTPUT,
    RANDOM_FOREST_RESULTS_OUTPUT,
    RANDOM_FOREST_FEATURE_IMPORTANCE_OUTPUT,
    API_COMPARISON_SUMMARY_OUTPUT,
    BEST_SELLERS_COMPARISON_SUMMARY_OUTPUT,
    WRITTEN_SUMMARY_OUTPUT,
    PRICE_DISTRIBUTION_PLOT,
    RATING_DISTRIBUTION_PLOT,
    PRICE_VS_RATING_PLOT,
    REVIEWCOUNT_VS_RATING_PLOT,
    AVERAGE_PRICE_BY_SOURCE_PLOT,
    AVERAGE_RATING_BY_SOURCE_PLOT,
    PRODUCT_COUNT_BY_SOURCE_PLOT,
    LOG_PRICE_BY_SOURCE_PLOT,
    RATING_BY_SOURCE_PLOT,
    REGRESSION_RESIDUALS_VS_FITTED_PLOT,
    REGRESSION_RESIDUAL_HISTOGRAM_PLOT,
    REGRESSION_QQ_PLOT,
    RANDOM_FOREST_FEATURE_IMPORTANCE_PLOT,
    API_COMPARISON_AVERAGE_RATING_PLOT,
    BEST_SELLERS_AVERAGE_RATING_PLOT,
    TEST_SIZE,
    RANDOM_STATE,
    RANDOM_FOREST_N_ESTIMATORS,
    RANDOM_FOREST_MAX_DEPTH,
    SIGNIFICANCE_LEVEL
)

# File paths and constants from config.py
ALL_ELECTRONICS_FILE = os.path.join(DATA_FOLDER, ALL_ELECTRONICS_CLEANED)
HOME_ENTERTAINMENT_FILE = os.path.join(DATA_FOLDER, HOME_ENTERTAINMENT_CLEANED)
AMAZON_BEST_SELLERS_FILE = os.path.join(DATA_FOLDER, AMAZON_BEST_SELLERS_CLEANED)
DUMMYJSON_FILE = os.path.join(DATA_FOLDER, DUMMYJSON_CLEANED)
FINAL_COMBINED_FILE = os.path.join(DATA_FOLDER, FINAL_COMBINED_OUTPUT)

# Basic helper functions
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print("Missing file:")
        print(file_path)
        return False
    else:
        return True


def clean_source_name(source_name):
    if source_name in SOURCE_LABELS:
        return SOURCE_LABELS[source_name]
    else:
        return str(source_name)


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

def save_text(text, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)


# Data loading and basic cleaning
def load_one_dataset(file_path, expected_source):
    df = pd.read_csv(file_path)

    expected_columns = [
        "product_name",
        "price",
        "rating",
        "review_count",
        "category",
        "subcategory",
        "source"
    ]

    for column in expected_columns:
        if column not in df.columns:
            df[column] = np.nan

    df = df[expected_columns].copy()

    df["source"] = expected_source

    return df

def load_all_final_datasets():
    required_files = [
        ALL_ELECTRONICS_FILE,
        HOME_ENTERTAINMENT_FILE,
        AMAZON_BEST_SELLERS_FILE,
        DUMMYJSON_FILE
    ]

    all_files_exist = True

    for file_path in required_files:
        if check_file_exists(file_path) == False:
            all_files_exist = False

    if all_files_exist == False:
        raise FileNotFoundError("At least one required data file is missing.")

    all_electronics = load_one_dataset(ALL_ELECTRONICS_FILE, "all_electronics_csv")
    home_entertainment = load_one_dataset(HOME_ENTERTAINMENT_FILE, "home_entertainment_csv")
    amazon_best_sellers = load_one_dataset(AMAZON_BEST_SELLERS_FILE, "amazon_webpage")
    dummyjson = load_one_dataset(DUMMYJSON_FILE, "dummyjson_api")

    df = pd.concat(
        [all_electronics, home_entertainment, amazon_best_sellers, dummyjson],
        ignore_index=True
    )

    return df

# AI generated:
def clean_combined_dataset(df):
    df = df.copy()

    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["subcategory"] = df["subcategory"].astype(str).str.strip()
    df["source"] = df["source"].astype(str).str.strip()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")

    df = df[df["product_name"] != ""]
    df = df[df["product_name"] != "nan"]

    df = df[df["price"].notna()]
    df = df[df["rating"].notna()]

    df = df[df["price"] >= 0]
    df = df[(df["rating"] >= 0) & (df["rating"] <= 5)]

    df = df[(df["review_count"].isna()) | (df["review_count"] >= 0)]

    df["source_label"] = df["source"].apply(clean_source_name)

    df["data_role"] = "other"

    df.loc[df["source"].isin(MAIN_AMAZON_SOURCES), "data_role"] = "main_amazon_csv"
    df.loc[df["source"] == BEST_SELLERS_SOURCE, "data_role"] = "amazon_best_sellers_web"
    df.loc[df["source"] == API_SOURCE, "data_role"] = "dummyjson_api"

    df["log_price"] = np.log1p(df["price"])

    df["log_review_count"] = np.where(
        df["review_count"].notna(),
        np.log1p(df["review_count"]),
        np.nan
    )

    df = df.drop_duplicates(subset=["product_name", "source"], keep="first")

    return df


# Presentation-stage summary and visualizations

# AI generated:
def save_dataset_summary(df):
    analysis_df = df.dropna(subset=["price", "rating", "review_count"]).copy()

    summary_data = {
        "metric": [
            "number_of_products",
            "number_of_sources",
            "number_of_subcategories",
            "mean_price",
            "median_price",
            "max_price",
            "mean_rating",
            "median_rating",
            "mean_review_count",
            "median_review_count",
            "price_rating_correlation",
            "reviewcount_rating_correlation"
        ],
        "value": [
            len(analysis_df),
            analysis_df["source"].nunique(),
            analysis_df["subcategory"].nunique(),
            round(analysis_df["price"].mean(), 2),
            round(analysis_df["price"].median(), 2),
            round(analysis_df["price"].max(), 2),
            round(analysis_df["rating"].mean(), 2),
            round(analysis_df["rating"].median(), 2),
            round(analysis_df["review_count"].mean(), 2),
            round(analysis_df["review_count"].median(), 2),
            round(analysis_df["price"].corr(analysis_df["rating"]), 4),
            round(analysis_df["review_count"].corr(analysis_df["rating"]), 4)
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    output_path = os.path.join(RESULTS_FOLDER, DATASET_SUMMARY_OUTPUT)
    summary_df.to_csv(output_path, index=False)

    return summary_df


# AI generated:
def save_source_summary(df):
    analysis_df = df.dropna(subset=["price", "rating", "review_count"]).copy()

    source_summary = analysis_df.groupby(["source", "source_label", "data_role"]).agg(
        product_count=("product_name", "count"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        price_q1=("price", lambda x: x.quantile(0.25)),
        price_q3=("price", lambda x: x.quantile(0.75)),
        mean_rating=("rating", "mean"),
        median_rating=("rating", "median"),
        mean_review_count=("review_count", "mean"),
        median_review_count=("review_count", "median")
    ).reset_index()

    numeric_columns = [
        "mean_price",
        "median_price",
        "price_q1",
        "price_q3",
        "mean_rating",
        "median_rating",
        "mean_review_count",
        "median_review_count"
    ]

    for column in numeric_columns:
        source_summary[column] = source_summary[column].round(2)

    output_path = os.path.join(RESULTS_FOLDER, SOURCE_SUMMARY_OUTPUT)
    source_summary.to_csv(output_path, index=False)

    return source_summary


# AI generated:
def save_subcategory_summary(df):
    """
    Save summary statistics by subcategory.
    """
    analysis_df = df.dropna(subset=["price", "rating", "review_count"]).copy()

    subcategory_summary = analysis_df.groupby(["subcategory", "source_label"]).agg(
        product_count=("product_name", "count"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("rating", "mean"),
        median_rating=("rating", "median"),
        mean_review_count=("review_count", "mean"),
        median_review_count=("review_count", "median")
    ).reset_index()

    subcategory_summary = subcategory_summary.sort_values(
        by="product_count",
        ascending=False
    )

    for column in [
        "mean_price",
        "median_price",
        "mean_rating",
        "median_rating",
        "mean_review_count",
        "median_review_count"
    ]:
        subcategory_summary[column] = subcategory_summary[column].round(2)

    output_path = os.path.join(RESULTS_FOLDER, SUBCATEGORY_SUMMARY_OUTPUT)
    subcategory_summary.to_csv(output_path, index=False)

    return subcategory_summary

# AI generated:
def plot_price_distribution(df):
    price_limit = df["price"].quantile(0.99)
    plot_df = df[df["price"] <= price_limit].copy()

    plt.figure(figsize=(8, 5))
    plt.hist(plot_df["price"], bins=30, edgecolor="black")
    plt.title("Price Distribution (up to 99th percentile)")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, PRICE_DISTRIBUTION_PLOT))
    plt.close()

# AI generated:
def plot_rating_distribution(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["rating"], bins=20, edgecolor="black")
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, RATING_DISTRIBUTION_PLOT))
    plt.close()


# AI generated:
def plot_price_vs_rating(df):
    price_limit = df["price"].quantile(0.99)
    plot_df = df[df["price"] <= price_limit].copy()

    plt.figure(figsize=(8, 5))
    plt.scatter(plot_df["price"], plot_df["rating"], alpha=0.4)
    plt.title("Price vs Rating (up to 99th percentile)")
    plt.xlabel("Price")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, PRICE_VS_RATING_PLOT))
    plt.close()

# AI generated:
def plot_reviewcount_vs_rating(df):
    plot_df = df.dropna(subset=["review_count"]).copy()
    plot_df = plot_df[plot_df["review_count"] > 0]

    plt.figure(figsize=(8, 5))
    plt.scatter(plot_df["review_count"], plot_df["rating"], alpha=0.4)
    plt.xscale("log")
    plt.title("Review Count vs Rating")
    plt.xlabel("Review Count (log scale)")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, REVIEWCOUNT_VS_RATING_PLOT))
    plt.close()


# AI generated:
def plot_average_price_by_source(source_summary):
    plt.figure(figsize=(9, 5))
    plt.bar(source_summary["source_label"], source_summary["mean_price"], edgecolor="black")
    plt.title("Average Price by Source")
    plt.xlabel("Source")
    plt.ylabel("Average Price")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, AVERAGE_PRICE_BY_SOURCE_PLOT))
    plt.close()


# AI generated:
def plot_average_rating_by_source(source_summary):
    plt.figure(figsize=(9, 5))
    plt.bar(source_summary["source_label"], source_summary["mean_rating"], edgecolor="black")
    plt.title("Average Rating by Source")
    plt.xlabel("Source")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, AVERAGE_RATING_BY_SOURCE_PLOT))
    plt.close()


# AI generated:
def plot_product_count_by_source(source_summary):
    plt.figure(figsize=(9, 5))
    plt.bar(source_summary["source_label"], source_summary["product_count"], edgecolor="black")
    plt.title("Product Count by Source")
    plt.xlabel("Source")
    plt.ylabel("Number of Products")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, PRODUCT_COUNT_BY_SOURCE_PLOT))
    plt.close()


# AI generated:
def plot_log_price_by_source(df):
    analysis_df = df.dropna(subset=["log_price"]).copy()
    source_labels = list(analysis_df["source_label"].unique())

    data = []

    for label in source_labels:
        values = analysis_df[analysis_df["source_label"] == label]["log_price"]
        data.append(values)

    plt.figure(figsize=(10, 5))
    plt.boxplot(data, labels=source_labels)
    plt.title("Log Price by Source")
    plt.xlabel("Source")
    plt.ylabel("Log Price")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, LOG_PRICE_BY_SOURCE_PLOT))
    plt.close()


# AI generated:
def plot_rating_by_source(df):
    analysis_df = df.dropna(subset=["rating"]).copy()
    source_labels = list(analysis_df["source_label"].unique())

    data = []

    for label in source_labels:
        values = analysis_df[analysis_df["source_label"] == label]["rating"]
        data.append(values)

    plt.figure(figsize=(10, 5))
    plt.boxplot(data, labels=source_labels)
    plt.title("Rating by Source")
    plt.xlabel("Source")
    plt.ylabel("Rating")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, RATING_BY_SOURCE_PLOT))
    plt.close()


# Correlation analysis
# AI generated:
def run_correlation_analysis(df):
    """
    Run Pearson and Spearman correlations among main numeric variables.
    Pearson measures linear relationship.
    Spearman measures rank-based relationship and is useful for skewed data.
    """
    analysis_df = df.dropna(
        subset=["price", "rating", "review_count", "log_price", "log_review_count"]
    ).copy()

    variables = [
        "price",
        "rating",
        "review_count",
        "log_price",
        "log_review_count"
    ]

    results = []

    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            variable_1 = variables[i]
            variable_2 = variables[j]

            pearson_result = stats.pearsonr(analysis_df[variable_1], analysis_df[variable_2])
            spearman_result = stats.spearmanr(analysis_df[variable_1], analysis_df[variable_2])

            results.append({
                "variable_1": variable_1,
                "variable_2": variable_2,
                "pearson_correlation": round(pearson_result.statistic, 4),
                "pearson_p_value": pearson_result.pvalue,
                "spearman_correlation": round(spearman_result.statistic, 4),
                "spearman_p_value": spearman_result.pvalue
            })

    corr_df = pd.DataFrame(results)

    output_path = os.path.join(RESULTS_FOLDER, CORRELATION_OUTPUT)
    corr_df.to_csv(output_path, index=False)

    return corr_df


# AI generated:
def run_correlation_by_source(df):
    """
    Run selected correlations by source.
    This helps compare whether the relationship is consistent across data sources.
    """
    results = []

    for source in df["source"].unique():
        source_df = df[df["source"] == source].dropna(
            subset=["log_price", "rating", "log_review_count"]
        ).copy()

        if len(source_df) >= 3:
            price_rating = stats.spearmanr(source_df["log_price"], source_df["rating"])
            reviews_rating = stats.spearmanr(source_df["log_review_count"], source_df["rating"])

            results.append({
                "source": source,
                "source_label": clean_source_name(source),
                "n": len(source_df),
                "spearman_log_price_rating": round(price_rating.statistic, 4),
                "p_value_log_price_rating": price_rating.pvalue,
                "spearman_log_review_count_rating": round(reviews_rating.statistic, 4),
                "p_value_log_review_count_rating": reviews_rating.pvalue
            })

    corr_source_df = pd.DataFrame(results)

    output_path = os.path.join(RESULTS_FOLDER, CORRELATION_BY_SOURCE_OUTPUT)
    corr_source_df.to_csv(output_path, index=False)

    return corr_source_df

# Hypothesis testing
# AI generated:
def interpret_p_value(p_value, alpha=SIGNIFICANCE_LEVEL):
    """
    Interpret a p-value using alpha = 0.05.
    """
    if p_value < alpha:
        return "Reject H0: statistically significant difference"
    else:
        return "Fail to reject H0: no statistically significant difference"


# AI generated:
def welch_t_test(group_1, group_2, variable, group_1_name, group_2_name, test_name):
    """
    Run Welch's two-sample t-test for a numeric variable.
    Welch's test does not assume equal variance.
    """
    x = group_1[variable].dropna()
    y = group_2[variable].dropna()

    if len(x) < 2 or len(y) < 2:
        return {
            "test_name": test_name,
            "variable": variable,
            "group_1": group_1_name,
            "group_2": group_2_name,
            "group_1_n": len(x),
            "group_2_n": len(y),
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "Not enough data"
        }

    result = stats.ttest_ind(x, y, equal_var=False, nan_policy="omit")

    return {
        "test_name": test_name,
        "variable": variable,
        "group_1": group_1_name,
        "group_2": group_2_name,
        "group_1_n": len(x),
        "group_2_n": len(y),
        "group_1_mean": round(x.mean(), 4),
        "group_2_mean": round(y.mean(), 4),
        "statistic": result.statistic,
        "p_value": result.pvalue,
        "interpretation": interpret_p_value(result.pvalue)
    }


# AI generated:
def mann_whitney_test(group_1, group_2, variable, group_1_name, group_2_name, test_name):
    """
    Run Mann-Whitney U test as a non-parametric group comparison.
    This is useful when the variable is skewed.
    """
    x = group_1[variable].dropna()
    y = group_2[variable].dropna()

    if len(x) < 2 or len(y) < 2:
        return {
            "test_name": test_name,
            "variable": variable,
            "group_1": group_1_name,
            "group_2": group_2_name,
            "group_1_n": len(x),
            "group_2_n": len(y),
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "Not enough data"
        }

    result = stats.mannwhitneyu(x, y, alternative="two-sided")

    return {
        "test_name": test_name,
        "variable": variable,
        "group_1": group_1_name,
        "group_2": group_2_name,
        "group_1_n": len(x),
        "group_2_n": len(y),
        "group_1_median": round(x.median(), 4),
        "group_2_median": round(y.median(), 4),
        "statistic": result.statistic,
        "p_value": result.pvalue,
        "interpretation": interpret_p_value(result.pvalue)
    }


# AI generated:
def run_hypothesis_tests(df):
    """
    Run final-stage hypothesis tests.

    Test set 1:
        All Electronics CSV vs Home Entertainment CSV

    Test set 2:
        Main Amazon CSV sources vs Amazon Best Sellers Web

    Test set 3:
        Amazon sources vs DummyJSON API
    """
    results = []

    all_electronics = df[df["source"] == "all_electronics_csv"].copy()
    home_entertainment = df[df["source"] == "home_entertainment_csv"].copy()

    main_amazon = df[df["source"].isin(MAIN_AMAZON_SOURCES)].copy()
    best_sellers = df[df["source"] == BEST_SELLERS_SOURCE].copy()

    amazon_data = df[df["source"].isin(AMAZON_SOURCES)].copy()
    dummyjson = df[df["source"] == API_SOURCE].copy()

    comparisons = [
        (
            all_electronics,
            home_entertainment,
            "All Electronics CSV",
            "Home Entertainment CSV",
            "Main CSV source comparison"
        ),
        (
            main_amazon,
            best_sellers,
            "Main Amazon CSV Data",
            "Amazon Best Sellers Web",
            "Best Sellers comparison"
        ),
        (
            amazon_data,
            dummyjson,
            "Amazon Data Sources",
            "DummyJSON API",
            "API comparison"
        )
    ]

    variables = ["log_price", "rating", "log_review_count"]

    for comparison in comparisons:
        group_1 = comparison[0]
        group_2 = comparison[1]
        group_1_name = comparison[2]
        group_2_name = comparison[3]
        comparison_name = comparison[4]

        for variable in variables:
            results.append(
                welch_t_test(
                    group_1,
                    group_2,
                    variable,
                    group_1_name,
                    group_2_name,
                    comparison_name + " - Welch t-test"
                )
            )

            results.append(
                mann_whitney_test(
                    group_1,
                    group_2,
                    variable,
                    group_1_name,
                    group_2_name,
                    comparison_name + " - Mann-Whitney U test"
                )
            )

    test_df = pd.DataFrame(results)

    output_path = os.path.join(RESULTS_FOLDER, HYPOTHESIS_TESTS_OUTPUT)
    test_df.to_csv(output_path, index=False)

    return test_df

# Multiple linear regression
# AI generated:
def run_linear_regression(df):
    """
    Run multiple linear regression.

    Dependent variable:
        rating

    Predictors:
        log_price
        log_review_count
        source dummy variables

    This model checks whether price, review count, and data source are associated
    with customer rating.
    """
    model_df = df.dropna(
        subset=["rating", "log_price", "log_review_count", "source"]
    ).copy()

    model_df = model_df[["rating", "log_price", "log_review_count", "source"]]

    model_df = pd.get_dummies(
        model_df,
        columns=["source"],
        drop_first=True
    )

    y = model_df["rating"]
    X = model_df.drop(columns=["rating"])

    X = X.astype(float)
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    regression_text = str(model.summary())

    output_path = os.path.join(RESULTS_FOLDER, LINEAR_REGRESSION_OUTPUT)
    save_text(regression_text, output_path)

    return model, X, y


# AI generated:
def save_vif_results(X):
    """
    Calculate VIF to check multicollinearity among regression predictors.
    """
    vif_rows = []

    for i in range(X.shape[1]):
        vif_rows.append({
            "variable": X.columns[i],
            "VIF": variance_inflation_factor(X.values, i)
        })

    vif_df = pd.DataFrame(vif_rows)

    output_path = os.path.join(RESULTS_FOLDER, VIF_OUTPUT)
    vif_df.to_csv(output_path, index=False)

    return vif_df


# AI generated:
def save_regression_diagnostic_plots(model):
    """
    Save plots for checking regression assumptions.

    1. Residuals vs fitted values
    2. Histogram of residuals
    3. Q-Q plot of residuals
    """
    fitted_values = model.fittedvalues
    residuals = model.resid

    plt.figure(figsize=(8, 5))
    plt.scatter(fitted_values, residuals, alpha=0.4)
    plt.axhline(y=0, linestyle="--")
    plt.title("Regression Diagnostic: Residuals vs Fitted Values")
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, REGRESSION_RESIDUALS_VS_FITTED_PLOT))
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(residuals, bins=40, edgecolor="black")
    plt.title("Regression Diagnostic: Histogram of Residuals")
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, REGRESSION_RESIDUAL_HISTOGRAM_PLOT))
    plt.close()

    sm.qqplot(residuals, line="45", fit=True)
    plt.title("Regression Diagnostic: Q-Q Plot of Residuals")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, REGRESSION_QQ_PLOT))
    plt.close()


# Random Forest regression model
# AI generated:
def run_random_forest_model(df):
    """
    Run a Random Forest regression model to predict rating.

    Target:
        rating

    Features:
        log_price
        log_review_count
        source
        subcategory

    This is included as an advanced ML model. The result may not be very strong
    because ratings are concentrated near 4.0, but it gives a useful comparison
    with the linear regression model.
    """
    model_df = df.dropna(
        subset=["rating", "log_price", "log_review_count", "source", "subcategory"]
    ).copy()

    model_df = model_df[
        ["rating", "log_price", "log_review_count", "source", "subcategory"]
    ]

    X = model_df.drop(columns=["rating"])
    y = model_df["rating"]

    X = pd.get_dummies(
        X,
        columns=["source", "subcategory"],
        drop_first=True
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    rf_model = RandomForestRegressor(
        n_estimators=RANDOM_FOREST_N_ESTIMATORS,
        random_state=RANDOM_STATE,
        max_depth=RANDOM_FOREST_MAX_DEPTH
    )

    rf_model.fit(X_train, y_train)

    predictions = rf_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = math.sqrt(mean_squared_error(y_test, predictions))
    r_squared = r2_score(y_test, predictions)

    results = {
        "model": "Random Forest Regression",
        "target": "rating",
        "number_of_rows_used": len(model_df),
        "test_size": len(y_test),
        "MAE": mae,
        "RMSE": rmse,
        "R_squared": r_squared
    }

    results_df = pd.DataFrame([results])

    output_path = os.path.join(RESULTS_FOLDER, RANDOM_FOREST_RESULTS_OUTPUT)
    results_df.to_csv(output_path, index=False)

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "importance": rf_model.feature_importances_
    })

    feature_importance = feature_importance.sort_values(
        by="importance",
        ascending=False
    )

    feature_output_path = os.path.join(RESULTS_FOLDER, RANDOM_FOREST_FEATURE_IMPORTANCE_OUTPUT)
    feature_importance.to_csv(feature_output_path, index=False)

    top_features = feature_importance.head(15)

    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"], top_features["importance"], edgecolor="black")
    plt.title("Random Forest Feature Importance - Top 15")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, RANDOM_FOREST_FEATURE_IMPORTANCE_PLOT))
    plt.close()

    return results_df, feature_importance


# Special source comparisons
# AI generated:
def save_api_comparison(df):
    """
    Compare Amazon data sources with DummyJSON API data.

    This ensures the API dataset is clearly used in the final project.
    """
    comparison_df = df.copy()

    comparison_df["comparison_group"] = "Other"

    comparison_df.loc[
        comparison_df["source"].isin(AMAZON_SOURCES),
        "comparison_group"
    ] = "Amazon Sources"

    comparison_df.loc[
        comparison_df["source"] == API_SOURCE,
        "comparison_group"
    ] = "DummyJSON API"

    comparison_df = comparison_df[
        comparison_df["comparison_group"].isin(["Amazon Sources", "DummyJSON API"])
    ]

    comparison_df = comparison_df.dropna(subset=["price", "rating", "review_count"])

    api_summary = comparison_df.groupby("comparison_group").agg(
        product_count=("product_name", "count"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("rating", "mean"),
        median_rating=("rating", "median"),
        mean_review_count=("review_count", "mean"),
        median_review_count=("review_count", "median")
    ).reset_index()

    for column in [
        "mean_price",
        "median_price",
        "mean_rating",
        "median_rating",
        "mean_review_count",
        "median_review_count"
    ]:
        api_summary[column] = api_summary[column].round(2)

    output_path = os.path.join(RESULTS_FOLDER, API_COMPARISON_SUMMARY_OUTPUT)
    api_summary.to_csv(output_path, index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(api_summary["comparison_group"], api_summary["mean_rating"], edgecolor="black")
    plt.title("Average Rating: Amazon Sources vs DummyJSON API")
    plt.xlabel("Comparison Group")
    plt.ylabel("Average Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, API_COMPARISON_AVERAGE_RATING_PLOT))
    plt.close()

    return api_summary


# AI generated:
def save_best_sellers_comparison(df):
    """
    Compare main Amazon CSV data with Amazon Best Sellers web-scraped data.
    """
    comparison_df = df.copy()

    comparison_df["comparison_group"] = "Other"

    comparison_df.loc[
        comparison_df["source"].isin(MAIN_AMAZON_SOURCES),
        "comparison_group"
    ] = "Main Amazon CSV Data"

    comparison_df.loc[
        comparison_df["source"] == BEST_SELLERS_SOURCE,
        "comparison_group"
    ] = "Amazon Best Sellers Web"

    comparison_df = comparison_df[
        comparison_df["comparison_group"].isin(
            ["Main Amazon CSV Data", "Amazon Best Sellers Web"]
        )
    ]

    comparison_df = comparison_df.dropna(subset=["price", "rating", "review_count"])

    best_summary = comparison_df.groupby("comparison_group").agg(
        product_count=("product_name", "count"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("rating", "mean"),
        median_rating=("rating", "median"),
        mean_review_count=("review_count", "mean"),
        median_review_count=("review_count", "median")
    ).reset_index()

    for column in [
        "mean_price",
        "median_price",
        "mean_rating",
        "median_rating",
        "mean_review_count",
        "median_review_count"
    ]:
        best_summary[column] = best_summary[column].round(2)

    output_path = os.path.join(RESULTS_FOLDER, BEST_SELLERS_COMPARISON_SUMMARY_OUTPUT)
    best_summary.to_csv(output_path, index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(best_summary["comparison_group"], best_summary["mean_rating"], edgecolor="black")
    plt.title("Average Rating: Main Amazon CSV vs Best Sellers Web")
    plt.xlabel("Comparison Group")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, BEST_SELLERS_AVERAGE_RATING_PLOT))
    plt.close()

    return best_summary

# Written summary helper
# AI generated:
def create_written_summary(df, dataset_summary, source_summary, rf_results):
    """
    Create a short written summary that can help with README or final report.
    """
    analysis_df = df.dropna(subset=["price", "rating", "review_count"]).copy()

    product_count = len(analysis_df)
    source_count = analysis_df["source"].nunique()

    mean_price = analysis_df["price"].mean()
    median_price = analysis_df["price"].median()

    mean_rating = analysis_df["rating"].mean()
    median_rating = analysis_df["rating"].median()

    mean_reviews = analysis_df["review_count"].mean()
    median_reviews = analysis_df["review_count"].median()

    rf_r2 = rf_results["R_squared"].iloc[0]

    text = f"""
DSCI 510 Final Analysis Summary

The final analysis uses four cleaned datasets: All Electronics CSV, Home Entertainment
CSV, Amazon Best Sellers web-scraped data, and DummyJSON API data. After cleaning,
the analysis dataset contains {product_count} products from {source_count} sources.

The overall mean price is {mean_price:.2f}, while the median price is {median_price:.2f}.
This confirms that product price is strongly right-skewed. The overall mean rating is
{mean_rating:.2f}, and the median rating is {median_rating:.2f}, showing that most
ratings are concentrated near the high end of the 0-5 scale. The mean review count is
{mean_reviews:.2f}, while the median review count is {median_reviews:.2f}, which also
shows a right-skewed pattern.

Compared with the presentation-stage analysis, this final stage adds log transformation,
Pearson and Spearman correlation analysis, hypothesis testing, multiple linear regression,
regression diagnostics, and a Random Forest regression model. DummyJSON is used as
an API-based comparison dataset, while Amazon Best Sellers is used as a supplementary
web-scraped source for best-selling products.

The Random Forest model R-squared is {rf_r2:.4f}. If this value is low, it suggests that
price, review count, source, and subcategory alone cannot strongly predict customer
rating. This is still a useful result because customer rating may depend on many other
factors, such as brand reputation, product quality, customer expectations, and product
description details.
"""

    output_path = os.path.join(RESULTS_FOLDER, WRITTEN_SUMMARY_OUTPUT)
    save_text(text, output_path)

    return text

# Main pipeline
def main():
    print_section("Starting Final Analysis")

    create_folder(RESULTS_FOLDER)

    print("Project folder:", PROJECT_FOLDER)
    print("Data folder:", DATA_FOLDER)
    print("Results folder:", RESULTS_FOLDER)

    print_section("Step 1: Loading four final cleaned datasets")
    raw_df = load_all_final_datasets()
    print("Combined raw shape:", raw_df.shape)
    print("Columns:", list(raw_df.columns))

    print_section("Step 2: Cleaning combined dataset and creating log variables")
    df = clean_combined_dataset(raw_df)
    print("Cleaned combined shape:", df.shape)
    print("Sources:")
    print(df["source_label"].value_counts())

    df.to_csv(FINAL_COMBINED_FILE, index=False)
    print("Final combined dataset saved to:")
    print(FINAL_COMBINED_FILE)

    print_section("Step 3: Presentation-stage summary and plots")
    dataset_summary = save_dataset_summary(df)
    source_summary = save_source_summary(df)
    subcategory_summary = save_subcategory_summary(df)

    plot_price_distribution(df)
    plot_rating_distribution(df)
    plot_price_vs_rating(df)
    plot_reviewcount_vs_rating(df)
    plot_average_price_by_source(source_summary)
    plot_average_rating_by_source(source_summary)
    plot_product_count_by_source(source_summary)

    print("Presentation-stage summaries and plots completed.")

    print_section("Step 4: Final-stage source and distribution plots")
    plot_log_price_by_source(df)
    plot_rating_by_source(df)

    print("Final-stage source comparison plots completed.")

    print_section("Step 5: Correlation analysis")
    correlation_results = run_correlation_analysis(df)
    correlation_by_source = run_correlation_by_source(df)
    print(correlation_results)
    print(correlation_by_source)

    print_section("Step 6: Hypothesis testing")
    hypothesis_results = run_hypothesis_tests(df)
    print(hypothesis_results)

    print_section("Step 7: Multiple linear regression and diagnostics")
    regression_model, X, y = run_linear_regression(df)
    vif_results = save_vif_results(X)
    save_regression_diagnostic_plots(regression_model)
    print(regression_model.summary())
    print(vif_results)

    print_section("Step 8: Random Forest regression model")
    rf_results, feature_importance = run_random_forest_model(df)
    print(rf_results)
    print(feature_importance.head(15))

    print_section("Step 9: API and Best Sellers comparison")
    api_summary = save_api_comparison(df)
    best_sellers_summary = save_best_sellers_comparison(df)
    print(api_summary)
    print(best_sellers_summary)

    print_section("Step 10: Written summary")
    written_summary = create_written_summary(
        df,
        dataset_summary,
        source_summary,
        rf_results
    )
    print(written_summary)

    print_section("Analysis complete")
    print("All results were saved to:")
    print(RESULTS_FOLDER)

if __name__ == "__main__":
    main()

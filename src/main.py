"""
AI use note:
    This file mainly uses course-style Python: imports, functions, print
    statements, and calling functions from other project files.
"""

import os
import sys
def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

def run_pipeline():
    print_section("DSCI 510 Final Project Pipeline Started")

    from api_fetch import save_dummyjson_products
    from clean_data import main as clean_data_main
    from final_analysis import main as final_analysis_main
    from tests import main as tests_main

    print_section("Step 1: Fetch DummyJSON API data")
    save_dummyjson_products()

    print_section("Step 2: Clean all datasets")
    clean_data_main()

    print_section("Step 3: Run final analysis")
    final_analysis_main()

    print_section("Step 4: Run tests")
    tests_main()

    print_section("Pipeline finished successfully")


def main():
    run_pipeline()


if __name__ == "__main__":
    main()
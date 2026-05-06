"""
amazon_web_scraper_with_rating_v3.py

DSCI 510 Final Project

AI use note:
    Basic Python parts such as imports, variables, functions, if-statements,
    loops, file paths, and printing are written in a DSCI 510 course-style format.

    HTML selector logic, web scraping parsing logic, and BeautifulSoup extraction
    sections are labeled with:
        # AI generated:
"""

import os
import time
import random
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

from config import (
    DATA_FOLDER,
    AMAZON_BEST_SELLERS_RAW,
    AMAZON_CATEGORY_URLS,
    PAGES_PER_CATEGORY,
    TARGET_ROWS
)


# Request settings
# AI generated:
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# Helper functions
def get_text_safe(tag):
    if tag is None:
        return None
    else:
        return tag.get_text(strip=True)


def clean_price(value):
    if value is None:
        return None

    value = str(value).replace(",", "")
    match = re.search(r"\d+\.\d+|\d+", value)

    if match:
        return float(match.group())
    else:
        return None

def clean_rating(value):
    if value is None:
        return None

    match = re.search(r"\d+\.\d+|\d+", str(value))

    if match:
        return float(match.group())
    else:
        return None

def clean_rating_count(value):
    if value is None:
        return None

    match = re.search(r"[\d,]+", str(value))

    if match:
        return int(match.group().replace(",", ""))
    else:
        return None

def clean_rank(value):
    if value is None:
        return None

    match = re.search(r"\d+", str(value))

    if match:
        return int(match.group())
    else:
        return None


# HTML parsing functions
# AI generated:
def find_product_blocks(soup):
    """
    Find product blocks from an Amazon Best Sellers page.
    Amazon page structure can change, so several selectors are tried.
    """
    blocks = soup.select("div.zg-grid-general-faceout")

    if len(blocks) == 0:
        blocks = soup.select("div.p13n-sc-uncoverable-faceout")

    if len(blocks) == 0:
        blocks = soup.select("div[data-asin]")

    return blocks


# AI generated:
def find_product_title(item):
    """
    Extract product title from one product block.
    """
    title_tag = (
        item.select_one("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        or item.select_one("div._cDEzb_p13n-sc-css-line-clamp-4_2q2cc")
        or item.select_one("span.a-size-medium")
        or item.select_one("span.a-size-base-plus")
        or item.select_one("img[alt]")
    )

    if title_tag is None:
        return None

    if title_tag.name == "img":
        return title_tag.get("alt")
    else:
        return get_text_safe(title_tag)


# AI generated:
def find_price(item):
    """
    Extract product price from one product block.
    """
    price_tag = (
        item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z")
        or item.select_one("span.a-price span.a-offscreen")
        or item.select_one("span.a-offscreen")
        or item.select_one("span.a-size-base.a-color-price")
    )

    return get_text_safe(price_tag)


# AI generated:
def find_rating(item):
    """
    Extract product rating from one product block.
    """
    rating_tag = (
        item.select_one("span.a-icon-alt")
        or item.select_one("i.a-icon-star-small span.a-icon-alt")
        or item.select_one("i.a-icon-star span.a-icon-alt")
        or item.select_one("span[aria-label*='out of 5 stars']")
    )

    if rating_tag is not None:
        rating_text = get_text_safe(rating_tag)
        if rating_text is not None and "out of 5 stars" in rating_text:
            return rating_text

    possible_tags = item.select("[aria-label]")

    for tag in possible_tags:
        label = tag.get("aria-label")
        if label is not None and "out of 5 stars" in label:
            return label

    return None


# AI generated:
def find_rating_count(item):
    """
    Extract product rating count from one product block.
    """
    count_candidates = []

    tags = item.select("a.a-size-small, span.a-size-small, span.a-size-base")

    for tag in tags:
        text = get_text_safe(tag)
        if text is not None:
            count_candidates.append(text)

    for text in count_candidates:
        if re.fullmatch(r"\d{1,3}(,\d{3})+|\d{3,}", text):
            return text

    return None


# AI generated:
def find_rank(item):
    """
    Extract product best seller rank from one product block.
    """
    rank_tag = item.select_one("span.zg-bdg-text")

    if rank_tag is not None:
        return get_text_safe(rank_tag)

    text = get_text_safe(item)

    if text is not None:
        match = re.search(r"#\s*\d+", text)
        if match:
            return match.group()

    return None


# AI generated:
def build_page_url(base_url, page_number):
    """
    Build page URL for a Best Sellers page.
    """
    if page_number == 1:
        return base_url
    else:
        return base_url + "?_encoding=UTF8&pg=" + str(page_number)


# AI generated:
def get_soup(url):
    """
    Request one webpage and convert it to BeautifulSoup object.
    """
    response = requests.get(url, headers=HEADERS, timeout=20)

    print("URL:", url)
    print("Status code:", response.status_code)

    response.raise_for_status()

    return BeautifulSoup(response.text, "lxml")


# Scraping function
# AI generated:
def scrape_one_page(url, product_category):
    """
    Scrape one Amazon Best Sellers page.
    """
    soup = get_soup(url)
    product_blocks = find_product_blocks(soup)

    print("Matched product blocks:", len(product_blocks))

    rows = []

    for item in product_blocks:
        product_name = find_product_title(item)
        price = find_price(item)
        rating = find_rating(item)
        rating_count = find_rating_count(item)
        rank = find_rank(item)

        if product_name is not None and len(product_name) > 5:
            row = {
                "product_name": product_name,
                "product_category": product_category,
                "rating": clean_rating(rating),
                "rating_count": clean_rating_count(rating_count),
                "price": clean_price(price),
                "best_seller_rank": clean_rank(rank),
                "source_url": url
            }
            rows.append(row)

    return rows


def remove_duplicates(rows):
    """
    Remove duplicate product rows based on product name.
    """
    unique_rows = []
    seen_names = []

    for row in rows:
        name = str(row["product_name"]).lower().strip()

        if name not in seen_names:
            seen_names.append(name)
            unique_rows.append(row)

    return unique_rows


def keep_usable_rows(rows):
    usable_rows = []

    for row in rows:
        if row["product_name"] is not None and row["price"] is not None:
            usable_rows.append(row)

    return usable_rows

# Main program
def main():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    all_rows = []

    for category_info in AMAZON_CATEGORY_URLS:
        product_category = category_info["product_category"]
        base_url = category_info["base_url"]

        for page_number in range(1, PAGES_PER_CATEGORY + 1):
            url = build_page_url(base_url, page_number)

            try:
                page_rows = scrape_one_page(url, product_category)
                print(product_category, "page", page_number, "rows:", len(page_rows))
                all_rows = all_rows + page_rows

            except Exception as error:
                print("Error:", error)

            print("-" * 60)
            time.sleep(random.uniform(2, 5))

    print("Rows before cleaning:", len(all_rows))

    unique_rows = remove_duplicates(all_rows)
    usable_rows = keep_usable_rows(unique_rows)

    print("Rows after removing duplicates:", len(unique_rows))
    print("Rows after keeping usable rows:", len(usable_rows))

    df = pd.DataFrame(usable_rows)

    if len(df) > TARGET_ROWS:
        df = df.head(TARGET_ROWS)

    output_file = os.path.join(DATA_FOLDER, AMAZON_BEST_SELLERS_RAW)

    df.to_csv(output_file, index=False)

    print()
    print("Finished.")
    print("Final shape:", df.shape)
    print("CSV saved to:", output_file)
    print()
    print(df.head(10))

if __name__ == "__main__":
    main()
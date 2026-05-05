import os
import time
import random
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Settings
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

CATEGORY_URLS = [
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

PAGES_PER_CATEGORY = 2
TARGET_ROWS = 300

# File path helper
def get_project_folder():
    """
    This file is expected to be inside src/.
    The project folder is one level above src/.
    """
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(current_folder)
    return project_folder

def get_data_folder():
    """
    Return the data folder in the main project folder.
    """
    project_folder = get_project_folder()
    data_folder = os.path.join(project_folder, "data")

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    return data_folder


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


# AI generated:
def find_product_blocks(soup):
    blocks = soup.select("div.zg-grid-general-faceout")

    if len(blocks) == 0:
        blocks = soup.select("div.p13n-sc-uncoverable-faceout")

    if len(blocks) == 0:
        blocks = soup.select("div[data-asin]")

    return blocks


# AI generated:
def find_product_title(item):
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
    price_tag = (
        item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z")
        or item.select_one("span.a-price span.a-offscreen")
        or item.select_one("span.a-offscreen")
        or item.select_one("span.a-size-base.a-color-price")
    )

    return get_text_safe(price_tag)


# AI generated:
def find_rating(item):
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
    if page_number == 1:
        return base_url
    else:
        return base_url + "?_encoding=UTF8&pg=" + str(page_number)


# AI generated:
def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    print("URL:", url)
    print("Status code:", response.status_code)

    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


# Scraping function

# AI generated:
def scrape_one_page(url, product_category):
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
    data_folder = get_data_folder()
    all_rows = []

    for category_info in CATEGORY_URLS:
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

    output_file = os.path.join(data_folder, "amazon_best_sellers_web_scraped.csv")

    df.to_csv(output_file, index=False)

    print()
    print("Finished.")
    print("Final shape:", df.shape)
    print("CSV saved to:", output_file)
    print()
    print(df.head(10))

if __name__ == "__main__":
    main()
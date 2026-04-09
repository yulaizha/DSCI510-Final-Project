import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

URLS = [
    (
        "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_electronics_0",
        "electronics"
    ),
    (
        "https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_nav_wireless_0",
        "cell_phones_accessories"
    ),
    (
        "https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_nav_pc_0",
        "computers_accessories"
    )
]


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    print(f"URL: {url}")
    print("Status code:", response.status_code)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def extract_text_safe(tag):
    return tag.get_text(strip=True) if tag else None


def clean_price(value):
    if pd.isna(value) or value is None:
        return None
    match = re.search(r"\d+\.\d+|\d+", str(value).replace(",", ""))
    return float(match.group()) if match else None


def clean_rating(value):
    if pd.isna(value) or value is None:
        return None
    match = re.search(r"\d+\.\d+|\d+", str(value))
    return float(match.group()) if match else None


def clean_review_count(value):
    if pd.isna(value) or value is None:
        return None
    match = re.search(r"[\d,]+", str(value))
    return int(match.group().replace(",", "")) if match else None


def scrape_amazon_bestsellers_page(url, subcategory):
    soup = get_soup(url)
    products = []

    items = soup.select("div.zg-grid-general-faceout")
    if not items:
        items = soup.select("div.p13n-sc-uncoverable-faceout")
    if not items:
        items = soup.select("div.p13n-gridRow div")
    if not items:
        items = soup.select("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")

    print("Number of matched blocks:", len(items))

    if items and "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1" in str(items[0].get("class", [])):
        for title_tag in items:
            title = extract_text_safe(title_tag)
            if title:
                products.append({
                    "product_name": title,
                    "price": None,
                    "rating": None,
                    "review_count": None,
                    "category": "electronics",
                    "subcategory": subcategory,
                    "source": "amazon_webpage"
                })
        return pd.DataFrame(products)

    for item in items:
        title_tag = (
            item.select_one("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
            or item.select_one("span.a-size-medium")
            or item.select_one("div[title]")
            or item.select_one("img[alt]")
        )

        price_tag = (
            item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z")
            or item.select_one("span.a-size-base.a-color-price")
            or item.select_one("span.a-offscreen")
        )

        rating_tag = (
            item.select_one("span.a-icon-alt")
            or item.select_one("span[aria-label*='out of 5 stars']")
        )

        review_count_tag = (
            item.select_one("span.a-size-small")
            or item.select_one("a.a-size-small")
        )

        title = extract_text_safe(title_tag)

        if title_tag and title_tag.name == "img":
            title = title_tag.get("alt")

        price = extract_text_safe(price_tag)
        rating = extract_text_safe(rating_tag)
        review_count = extract_text_safe(review_count_tag)

        if title:
            products.append({
                "product_name": title,
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "category": "electronics",
                "subcategory": subcategory,
                "source": "amazon_webpage"
            })

    df = pd.DataFrame(products)

    if not df.empty:
        df = df.drop_duplicates(subset=["product_name"]).reset_index(drop=True)

    return df


if __name__ == "__main__":
    all_dfs = []

    for url, subcategory in URLS:
        try:
            df = scrape_amazon_bestsellers_page(url, subcategory)
            print(f"{subcategory} shape before cleaning:", df.shape)

            if not df.empty:
                df["price"] = df["price"].apply(clean_price)
                df["rating"] = df["rating"].apply(clean_rating)
                df["review_count"] = df["review_count"].apply(clean_review_count)

            print(df.head(5))
            print(f"{subcategory} shape after cleaning:", df.shape)
            print("=" * 60)

            all_dfs.append(df)

            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error for {subcategory}: {e}")
            print("=" * 60)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df = final_df.drop_duplicates(subset=["product_name", "subcategory"]).reset_index(drop=True)

        print("Final shape:", final_df.shape)
        print(final_df.head(10))

        final_df.to_csv("data/amazon_best_sellers_combined.csv", index=False)
        print("CSV file saved: data/amazon_best_sellers_combined.csv")
    else:
        print("No data collected.")
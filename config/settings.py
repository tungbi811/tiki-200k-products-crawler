from pathlib import Path
import pandas as pd

FOLDER = Path("data/tiki_products_2")
FOLDER.mkdir(exist_ok=True)

FAILED_FILE = FOLDER / "failed_products.json"

API = "https://api.tiki.vn/product-detail/api/v1/products/{}"

CONCURRENCY = 4
BATCH_SIZE = 1000
RATE_PER_SEC = 4

MAX_429_RETRIES = 5
BACKOFF_BASE_SECONDS = 1.0
BACKOFF_MAX_SECONDS = 30.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ProductCrawler/1.0)",
    "Accept": "application/json",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8",
    "Referer": "https://tiki.vn/"
}

product_list = pd.read_csv("data/product_list.csv")

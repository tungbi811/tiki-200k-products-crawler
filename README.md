# Tiki Product Crawler

A high-performance **Python crawler** for collecting large-scale product data from **Tiki.vn**.

This project is designed to download information for **~200,000 products**, store the results as **JSON files**, and optimize data-fetching time using concurrency and batching techniques.

---

## 📌 Project Objectives

* Crawl product details from Tiki using public APIs
* Process a large list of product IDs (~200k)
* Store data in multiple `.json` files (≈1000 products per file)
* Normalize and clean product descriptions
* Optimize crawling speed and stability

---

## 📦 Data Fields Collected

For each product, the crawler collects:

* `id`
* `name`
* `url_key`
* `price`
* `description` (normalized)
* `images` (image URLs)

---

## 🔗 Data Sources

* **Product ID list**
  [https://1drv.ms/u/s!AukvlU4z92FZgp4xIlzQ4giHVa5Lpw?e=qDXctn](https://1drv.ms/u/s!AukvlU4z92FZgp4xIlzQ4giHVa5Lpw?e=qDXctn)

* **Product detail API (example)**
  [https://api.tiki.vn/product-detail/api/v1/products/138083218](https://api.tiki.vn/product-detail/api/v1/products/138083218)

> ⚠️ This project uses publicly accessible endpoints and is intended for **learning and internal data processing purposes only**.

---

## 🏗 Project Structure

```
tiki-product-crawler/
│
├── crawler/
│   ├── fetcher.py        # API requests & retry logic
│   ├── parser.py         # Data parsing & normalization
│   ├── writer.py         # JSON batching & file writing
│   └── utils.py          # Helpers (logging, timing, etc.)
│
├── scripts/
│   └── run_crawler.py    # Main execution script
│
├── data/                 # Output JSON files (ignored by git)
├── logs/                 # Log files (ignored by git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/your-username/tiki-product-crawler.git
cd tiki-product-crawler

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python scripts/run_crawler.py
```

The crawler will:

1. Load product IDs
2. Fetch product details concurrently
3. Normalize descriptions
4. Save results into JSON files (1000 products per file)

---

## 🚀 Performance Optimization

Techniques used to reduce crawling time:

* Concurrent requests (ThreadPool / AsyncIO)
* Request retry & timeout handling
* Batch-based file writing
* Minimal in-memory footprint

Designed to be **scalable and fault-tolerant** for long-running jobs.

---

## 🧹 Description Normalization

Product descriptions are cleaned by:

* Removing HTML tags
* Normalizing whitespace
* Standardizing encoding (UTF-8)
* Stripping redundant metadata

---

## 🛡 Notes & Disclaimer

* This project is **not affiliated with Tiki.vn**
* Do **not** use this crawler to violate terms of service
* Recommended for **data engineering practice** only

---

## 📄 License

MIT License

---

## ✨ Future Improvements

* Async HTTP with aiohttp
* Proxy rotation
* Incremental crawling
* Data validation schema
* Export to Parquet / CSV

---

Happy crawling 🚀

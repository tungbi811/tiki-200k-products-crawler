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

## 🧹 Description Normalization

Product descriptions are cleaned by:

* Removing HTML tags
* Normalizing whitespace
* Standardizing encoding (UTF-8)
* Stripping redundant metadata
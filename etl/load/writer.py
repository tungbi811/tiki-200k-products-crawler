import json
import asyncio
from pathlib import Path
from config.settings import *
from config.config import load_config
import psycopg2
from loader import load_batch
from utils.insert import insert_products_and_images

failed_products = {}
failed_lock = asyncio.Lock()

def write_json_sync(path: Path, payload: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

async def record_failed_product(product_id: int, status: int):
    async with failed_lock:
        failed_products.setdefault(status, []).append(product_id)

async def save_failed_products():
    if not failed_products:
        return

    payload = {
        "total_failed": sum(len(v) for v in failed_products.values()),
        "by_status": failed_products
    }

    await asyncio.to_thread(write_json_sync, FAILED_FILE, payload)
    print(f"[SAVED] failed_products.json ({payload['total_failed']} items)")


async def save_batch(batch_id: int, products: list):
    payload = {
        "batch_id": batch_id,
        "product_count": len(products),
        "products": products
    }
    path = FOLDER / f"batch_{batch_id:04d}.json"
    await asyncio.to_thread(write_json_sync, path, payload)

def write_to_db():
    config = load_config()

    with psycopg2.connect(**config) as conn:
        for path in sorted(Path("data/tiki_products").glob("batch_*.json")):
            product_list, image_list = load_batch(path)

            insert_products_and_images(product_list, image_list)

            print(f"[DB] loaded {path.name}")
import json
import asyncio
from pathlib import Path
from config import FOLDER, FAILED_FILE

failed_products = {}
failed_lock = asyncio.Lock()

def write_json_sync(path: Path, payload: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_processed_ids():
    processed = set()
    for path in FOLDER.glob("batch_*.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for p in data.get("products", []):
                    if "id" in p:
                        processed.add(p["id"])
        except Exception as e:
            print(f"[WARN] Failed to read {path}: {e}")
    return processed


def load_failed_products():
    if not FAILED_FILE.exists():
        return {}

    try:
        with open(FAILED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                int(status): list(map(int, ids))
                for status, ids in data.get("by_status", {}).items()
            }
    except Exception as e:
        print(f"[WARN] Failed to load failed_products.json: {e}")
        return {}


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

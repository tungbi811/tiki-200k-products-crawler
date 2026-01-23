import json
from config.settings import *

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
    
def load_batch(filepath):
    product_list = []
    image_list = []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for p in data.get("products", []):
        product_list.append([
            p["id"],
            p["name"],
            p["url_key"],
            p["price"],
            p["description"],
        ])

        for image in p.get("images", []):
            image_list.append([
                p["id"],
                image
            ])

    return product_list, image_list
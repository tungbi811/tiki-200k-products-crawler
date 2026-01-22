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
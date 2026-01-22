import re

def normalize_description(desc: str) -> str:
    if not desc:
        return ""
    desc = re.sub(r"<[^>]+>", "", desc)
    desc = re.sub(r"\s+", " ", desc)
    return desc.strip()


def normalize_product(data: dict) -> dict:
    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "url_key": data.get("url_key"),
        "price": data.get("price"),
        "description": normalize_description(data.get("description")),
        "images": [
            img.get("base_url")
            for img in (data.get("images") or [])
            if isinstance(img, dict) and "base_url" in img
        ],
    }

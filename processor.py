import asyncio
from api import fetch_product
from normalizer import normalize_product

async def process_batch(product_ids, session, sem):
    tasks = [fetch_product(session, pid, sem) for pid in product_ids]
    results = await asyncio.gather(*tasks)

    return [
        normalize_product(data)
        for data in results
        if data is not None
    ]

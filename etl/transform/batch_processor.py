import asyncio
from etl.extract.crawler import fetch_product
from etl.transform.normalizer import normalize_product

async def process_batch(product_ids, session, sem):
    tasks = [fetch_product(session, pid, sem) for pid in product_ids]
    results = await asyncio.gather(*tasks)

    return [
        normalize_product(data)
        for data in results
        if data is not None
    ]

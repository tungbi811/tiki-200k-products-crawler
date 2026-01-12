import asyncio
import aiohttp
import time

from config import (
    CONCURRENCY,
    BATCH_SIZE,
    RATE_PER_SEC,
    product_list
)
from api import init_rate_limiter
from processor import process_batch
from storage import (
    load_processed_ids,
    load_failed_products,
    save_batch,
    save_failed_products,
    failed_products
)
from exceptions import TooManyRequests


async def main():
    init_rate_limiter(RATE_PER_SEC)

    sem = asyncio.Semaphore(CONCURRENCY)

    processed_ids = load_processed_ids()
    failed_products.update(load_failed_products())

    failed_ids = {pid for ids in failed_products.values() for pid in ids}
    all_ids = set(product_list["id"].tolist())

    run_queue = list(all_ids - processed_ids - failed_ids)
    print(f"[QUEUE] total to fetch: {len(run_queue)}")

    batch = []
    batch_id = 1
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(run_queue), BATCH_SIZE):
            product_ids = run_queue[i:i + BATCH_SIZE]
            batch.extend(await process_batch(product_ids, session, sem))

            if len(batch) >= 1000:
                await save_batch(batch_id, batch)
                await save_failed_products()

                print(
                    f"Saved batch {batch_id:04d} "
                    f"({len(batch)} products) "
                    f"in {time.time() - start_time:.1f}s"
                )

                batch.clear()
                batch_id += 1
                start_time = time.time()

        await save_batch(batch_id, batch)
        await save_failed_products()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except TooManyRequests as e:
        print(f"[STOPPED] {e}")

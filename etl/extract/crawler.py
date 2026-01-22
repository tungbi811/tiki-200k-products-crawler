import asyncio
import random

from config.settings import *
from utils.exceptions import TooManyRequests
from etl.load.writer import record_failed_product
from utils.rate_limiter import RateLimiter

rate_limiter = None

def init_rate_limiter(rate_per_sec: int):
    global rate_limiter
    rate_limiter = RateLimiter(rate_per_sec)

async def _backoff_sleep(attempt: int):
    """
    Exponential backoff with jitter
    """
    delay = min(
        BACKOFF_BASE_SECONDS * (2 ** attempt),
        BACKOFF_MAX_SECONDS
    )
    jitter = random.uniform(0, delay * 0.1)
    await asyncio.sleep(delay + jitter)


async def fetch_product(session, product_id, sem):
    url = API.format(product_id)

    for attempt in range(MAX_429_RETRIES + 1):
        await rate_limiter.wait()

        async with sem:
            async with session.get(url, headers=HEADERS) as resp:
                if resp.status == 200:
                    return await resp.json()

                if resp.status == 429:
                    if attempt >= MAX_429_RETRIES:
                        print(
                            f"[429] Max retries exceeded for {product_id}"
                        )
                        raise TooManyRequests(
                            f"429 persisted after {MAX_429_RETRIES} retries"
                        )

                    print(
                        f"[429] {product_id} → retry {attempt + 1}/"
                        f"{MAX_429_RETRIES}"
                    )
                    await _backoff_sleep(attempt)
                    continue

                # non-retriable errors
                await record_failed_product(product_id, resp.status)
                print(f"FAILED {product_id} → HTTP {resp.status}")
                return None

    return None

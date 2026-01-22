import asyncio
from utils.exceptions import TooManyRequests
from pipeline.product_pipeline import run

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except TooManyRequests as e:
        print(f"[STOPPED] {e}")

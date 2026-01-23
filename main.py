import asyncio
from utils.exceptions import TooManyRequests
from pipeline.product_pipeline import run
from utils.create_tables import create_tables
from utils.insert import load_all_batches
from etl.load.writer import write_to_db

if __name__ == "__main__":
    try:
        asyncio.run(run())
        write_to_db()
    except TooManyRequests as e:
        print(f"[STOPPED] {e}")

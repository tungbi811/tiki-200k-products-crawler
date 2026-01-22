import asyncio
import time

class RateLimiter:
    def __init__(self, rate_per_sec: int):
        self._interval = 1 / rate_per_sec
        self._last = 0
        self._lock = asyncio.Lock()

    async def wait(self):
        async with self._lock:
            now = time.monotonic()
            delta = now - self._last
            if delta < self._interval:
                await asyncio.sleep(self._interval - delta)
            self._last = time.monotonic()

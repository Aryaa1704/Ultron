import asyncio
import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.responses import JSONResponse


class InMemoryRateLimiter:
    def __init__(self, requests_per_window: int = 120, window_seconds: int = 60) -> None:
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def __call__(self, request: Request, call_next):
        if request.url.path == "/healthz":
            return await call_next(request)

        identifier = self._resolve_identifier(request)
        now = time.monotonic()
        boundary = now - self.window_seconds

        async with self._lock:
            history = self._requests[identifier]
            while history and history[0] < boundary:
                history.popleft()

            if len(history) >= self.requests_per_window:
                retry_after = max(1, int(self.window_seconds - (now - history[0])))
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Please retry later."},
                    headers={"Retry-After": str(retry_after)},
                )

            history.append(now)

        return await call_next(request)

    @staticmethod
    def _resolve_identifier(request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        if request.client and request.client.host:
            return request.client.host
        return "unknown"

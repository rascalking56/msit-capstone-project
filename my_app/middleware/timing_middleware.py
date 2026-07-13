import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from my_app.utils.logger import log_info


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = round((time.time() - start) * 1000, 2)  # ms
        log_info(f"Request time: {request.method} {request.url} took {duration} ms")

        response.headers["X-Process-Time-ms"] = str(duration)
        return response

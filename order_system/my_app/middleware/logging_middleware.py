from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from my_app.utils.logger import log_info


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log_info(f"Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        log_info(f"Response status: {response.status_code} for {request.method} {request.url}")

        return response

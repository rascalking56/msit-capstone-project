from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from my_app.utils.logger import log_error


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception as e:
            log_error(f"Unhandled error: {str(e)} at {request.method} {request.url}")

            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "An unexpected error occurred.",
                    "details": str(e)
                }
            )

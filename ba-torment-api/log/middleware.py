from starlette.middleware.base import BaseHTTPMiddleware
from .logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            logger.info(
                "Incoming request",
                extra={
                    "req": { 
                        "method": request.method, 
                        "url": str(request.url), 
                        "agent": request.headers.get("User-Agent"), 
                        "ip": request.headers.get("X-Real-IP") 
                    },
                    "res": { 
                        "status_code": response.status_code
                    },
                },
            )
            return response
        except Exception as e:
            logger.error(
                "Internal server error",
                extra={
                    "req": { 
                        "method": request.method, 
                        "url": str(request.url), 
                        "agent": request.headers.get("User-Agent"), 
                        "ip": request.headers.get("X-Real-IP") 
                    },
                    "error": str(e),
                },

            )
            raise
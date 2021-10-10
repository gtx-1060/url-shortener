from fastapi import Response, Request

from app.data.db.db import SyncSessionLocal


class DatabaseSessionMiddleware:
    async def __call__(self, request: Request, call_next):
        response = Response('{"detail": "Internal server error"}', status_code=500)
        try:
            request.state.db = SyncSessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

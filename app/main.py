 import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import utils
from app.config import HOST, PORT
from app.middleware.database_session_middleware import DatabaseSessionMiddleware
from app.routers.schorturl_router import router as url_router
from app.routers.auth_router import router as auth_router

app = FastAPI()
app.middleware('http')(DatabaseSessionMiddleware())
app.include_router(url_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost', "http://127.0.0.1:3005"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def start():
    uvicorn.run('app.main:app', host=HOST)


if __name__ == "__main__":
    start()

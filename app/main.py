import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import utils

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost', "http://127.0.0.1:3005"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event('startup')
def on_start():
    utils.load_env_variables()


def start():
    uvicorn.run('app.main:app', host="127.0.0.1")


if __name__ == "__main__":
    start()

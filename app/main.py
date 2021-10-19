import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.env_variables_loader import env_variables
from app.middleware.database_session_middleware import DatabaseSessionMiddleware
from app.routers.schort_url_router import router as url_router
from app.routers.auth_router import router as auth_router
from app.services.schedule_service import myscheduler
from app.services.url_lifecycle_service import start_expire_tracking
from app.services.url_shorter_sevice import UrlShorter

app = FastAPI()
app.middleware('http')(DatabaseSessionMiddleware())
app.include_router(url_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=env_variables["ALLOW_ORIGINS"].split(" "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UrlShorter()


@app.on_event("startup")
def on_start():
    myscheduler.start()
    start_expire_tracking(myscheduler)


@app.on_event("shutdown")
def on_start():
    myscheduler.stop()


def start():
    uvicorn.run('app.main:app', host=env_variables["HOST"], port=int(env_variables["PORT"]))


if __name__ == "__main__":
    start()

# fmt: off
from fastapi import FastAPI
from routers import adsb, test
# fmt: on

app = FastAPI(docs_url="/", redoc_url=None)
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

app.include_router(adsb.router)
app.include_router(test.router)
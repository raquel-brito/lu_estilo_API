import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import os

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0  # Ajuste a taxa de amostragem conforme necessário
)

from fastapi import FastAPI
from app.api.v1.routes import api_router
from app.startup import create_initial_admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Lu Estilo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SentryAsgiMiddleware)

app.include_router(api_router, prefix="/api/v1")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
async def startup_event():
    await create_initial_admin()

@app.get("/debug-sentry")
async def trigger_error():
    division_by_zero = 1 / 0
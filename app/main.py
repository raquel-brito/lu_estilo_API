import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    dsn="https://80339ee9bb46069fe6e11337f4279ff8@o4509382887538688.ingest.us.sentry.io/4509382907592704",
    traces_sample_rate=1.0  # taxa para performance (pode ajustar depois)
)

from fastapi import FastAPI
from app.api.v1.routes import api_router
from app.startup import create_initial_admin

app = FastAPI(title="Lu Estilo API")

app.add_middleware(SentryAsgiMiddleware)


@app.get("/")
async def root():
    return {"message": "API Funcionando!"}

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await create_initial_admin()

@app.get("/debug-sentry")
async def trigger_error():
    division_by_zero = 1 / 0
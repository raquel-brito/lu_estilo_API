from fastapi import FastAPI
from app.api.v1.routes import api_router
from app.startup import create_initial_admin


app = FastAPI(title="Lu Estilo API")

@app.get("/")
async def root():
    return {"message": "API Funcionando!"}

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await create_initial_admin()
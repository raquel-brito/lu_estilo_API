from fastapi import FastAPI
from app.api.v1.routes import api_router

app = FastAPI(title="Lu Estilo API")

@app.get("/")
async def root():
    return {"message": "API Funcionando!"}

app.include_router(api_router, prefix="/api/v1")
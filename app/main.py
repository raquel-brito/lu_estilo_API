from fastapi import FastAPI


app = FastAPI(title="Lu Estilo API")
@app.get("/")
async def root():
    return {"message": "API Funcionando!"}

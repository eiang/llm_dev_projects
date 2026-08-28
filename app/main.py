from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(title="AI Backend Learning API")

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "AI Backend API is running"}



     

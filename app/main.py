from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import tasks

# Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Backend Learning API")

app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "AI Backend API is running"}

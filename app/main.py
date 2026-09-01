from fastapi import FastAPI

from app.routers import ai, tasks

# Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Backend Learning API")

app.include_router(tasks.router)
app.include_router(ai.router)



@app.get("/")
def root():
    return {"message": "AI Backend API is running"}

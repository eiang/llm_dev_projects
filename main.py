from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    length: int
    preview: str


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(length=len(request.text), preview=request.text[:20])
        

from fastapi import FastAPI
from apis import ai

app = FastAPI()
app.include_router(ai.router, prefix="/ai", tags=["ai"])
@app.get("/")

def read_root():
    return "Welcome to SummarAIze"


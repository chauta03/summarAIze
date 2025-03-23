from contextlib import asynccontextmanager
from fastapi import FastAPI
from apis import ai, users, meetings
from db.db_manager import sessionmanager
from db.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="SummarAIze server")
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])

@app.get("/")
def read_root():
    return "Welcome to SummarAIze"


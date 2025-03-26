
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis import ai, users, meetings
from db.db_manager import sessionmanager
from db.models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

# Create the app
app = FastAPI(lifespan=lifespan, title="SummarAIze server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])

@app.get("/")
def read_root():
    return "Welcome to SummarAIze"

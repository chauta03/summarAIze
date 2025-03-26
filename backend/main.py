import sys
import audioop
sys.modules['pyaudioop'] = audioop

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ⬅️ Add this
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

# ⬇️ Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server origin
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

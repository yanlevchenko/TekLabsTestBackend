from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import meetings, users
from schemas.models import HealthResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=meetings.router, prefix="/meetings")
app.include_router(router=users.router, prefix="/users")


@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Ok")


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controllers.StocksController import stocks_router
from database import init_db


app = FastAPI(
    title="Stock api",
    description="Get stock data with epic statistics",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def index():
    return {"message": "Api is running"}

app.include_router(stocks_router, prefix="/api/v1")

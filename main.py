from fastapi import FastAPI
from dtypes import APIResponse, HttpStatus
from controller import StayController
import os

if os.getenv("ENV", "dev") == "dev":
    from dotenv import load_dotenv
    load_dotenv()
    print("Running in dev mode\nLoading .env file")

app = FastAPI(
    title="Bnb Clone Stay Service",
    description="A simple service to manage stays",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Abhiram B.S.N.",
        "email": "abhirambsn@gmail.com",
        "url": "https://abhirambsn.com"
    }
)

app.include_router(StayController)


@app.get("/")
async def root_healthz():
    return APIResponse(
        status=HttpStatus.OK,
        data=None,
        message="ok"
    ).to_dict()


@app.get("/healthz")
async def healthz():
    return APIResponse(
        status=HttpStatus.OK,
        data=None,
        message="ok"
    ).to_dict()



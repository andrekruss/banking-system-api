import os
from beanie import init_beanie
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.database.models.account import Account
from src.database.models.payment import Payment
from src.database.models.user import User
from src.routers.auth_router import auth_router
from src.routers.payment_router import payment_router
from src.routers.user_router import user_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    client = AsyncIOMotorClient(os.getenv("CONNECTION_STRING"))
    database = client[os.getenv("DB_NAME")]

    # db models MUST be listed here
    await init_beanie(database=database, document_models=[User, Account, Payment])

    print("Connected to DB!")
    yield
    print("Shutting down app...")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(payment_router)

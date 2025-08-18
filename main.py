from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from sqlmodel import SQLModel, Field, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    content: Optional[str] = Field(default=None)




DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True)


app = FastAPI()

@app.get("/")
async def home():
    return RedirectResponse(url="/hello", status_code=303)


@app.get("/hello")
async def hello():
    return {"response" : "HELLO WORLD"}

@app.get("/db")
async def db():
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))
        return JSONResponse(status_code=200, content={"message": "Database is present"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Database is not present", "error": str(e)})
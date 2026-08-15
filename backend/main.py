from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Base, SessionLocal, engine, get_db
from model import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as database_session:
        existing_user = database_session.scalar(select(User).limit(1))

        if existing_user is None:
            database_session.add(
                User(
                    name="Zakarea Alkashef",
                    email="zak@example.com",
                )
            )
            database_session.commit()

    yield 

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}



@app.get("/users", response_model=list[UserResponse])
def get_users(
    database_session: Annotated[Session, Depends(get_db)],
) -> list[User]:
    statement = select(User).order_by(User.id)
    return list(database_session.scalars(statement).all())


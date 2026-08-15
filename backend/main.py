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

import logging

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("uvicorn.error")

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
    logger.info("Database tables initialized")

    sample_users = [
        {
            "name": "Zakarea Alkashef",
            "email": "zak@example.com",
        },
        {
            "name": "Sara Ahmad",
            "email": "sara@example.com",
        },
        {
            "name": "Adam Khalil",
            "email": "adam@example.com",
        },
    ]

    with SessionLocal() as database_session:
        existing_emails = set(
            database_session.scalars(select(User.email)).all()
        )

        users_to_create = [
            User(name=user["name"], email=user["email"])
            for user in sample_users
            if user["email"] not in existing_emails
        ]

        if users_to_create:
            database_session.add_all(users_to_create)
            database_session.commit()

            logger.info(
                "Created %d sample users",
                len(users_to_create),
            )

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    ],
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
    
    try:
        statement = select(User).order_by(User.id)
        users = list(database_session.scalars(statement).all())

        logger.info("Fetched %d users", len(users))
        return users

    except SQLAlchemyError as error:
        logger.exception("Failed to fetch users")

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch users",
        ) from error


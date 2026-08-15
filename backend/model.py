from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, func

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key = True)

  name: Mapped[str] = mapped_column(
    String(100),
    nullable=False
  )

  email: Mapped[str] = mapped_column(
    String(255),
    unique= True,
    index = True,
    nullable= False
  )

  created_at: Mapped[DateTime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
  )

  updated_at: Mapped[DateTime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False
  )
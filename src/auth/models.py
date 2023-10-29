from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(length=150), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
            String(length=1024), nullable=False
        )
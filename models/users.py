from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class UserProfile(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[Optional[str]]

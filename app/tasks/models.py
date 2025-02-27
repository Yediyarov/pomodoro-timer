from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey

class Task(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]
    type: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
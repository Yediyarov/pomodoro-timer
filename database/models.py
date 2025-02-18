from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from typing import Any, Optional



class Base(DeclarativeBase):
    id: Any
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Task(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]
    type: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
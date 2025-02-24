from sqlalchemy.orm import DeclarativeBase, declared_attr
from typing import Any

class Base(DeclarativeBase):
    id: Any
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
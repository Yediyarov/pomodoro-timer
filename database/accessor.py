from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from settings import settings


engine = create_engine(
    settings.get_db_url,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db_session() -> Session:
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise


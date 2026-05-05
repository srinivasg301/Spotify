from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=Session)


def get_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

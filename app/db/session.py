from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import engine

# Create session factory with proper configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # This prevents expired object issues
)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Provides automatic session cleanup and error handling.
    
    Usage:
        with get_db() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error occurred: {str(e)}")
    finally:
        db.close()

def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @app.get("/")
        def read_items(db: Session = Depends(get_db_session)):
            ...
    """
    with get_db() as db:
        yield db 
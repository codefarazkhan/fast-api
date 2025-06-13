from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import engine

# Create session factory with proper configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # This prevents expired object issues
)

def get_db_session():
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @app.get("/")
        def read_items(db: Session = Depends(get_db_session)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error occurred: {str(e)}")
    finally:
        db.close()
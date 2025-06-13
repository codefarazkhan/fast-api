from app.db.database import SessionLocal

# ✅ Shared DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

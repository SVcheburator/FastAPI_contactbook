from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add your own PostgreSQL database info here:
db_username = ...
db_password = ...
db_name = ...


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_username}:{db_password}@localhost:5432/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# NEVER (x100) password should be opened to internet!!!!
__id = os.getenv('MARIADB_USER_ID')
__pw = os.getenv('MARIADB_USER_PASSWORD')
__host=os.getenv('MARIADB_HOST')
__db = os.getenv('MARIADB_DB')
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{__id}:{__pw}@{__host}/{__db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

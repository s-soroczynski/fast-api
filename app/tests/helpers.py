from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

from app.utils import get_db
from app.main import app
from app.database import Base
from app.constants import ACCESS_TOKEN_EXPIRE_DAYS
from app.default.utils import create_access_token


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)



def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def clear_table_db(name: str):
    Base.metadata.tables[name].drop(bind=engine)

def clear_test_db():
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
test_client = TestClient(app)

def create_test_token(email: str = 'test_email') -> str: 
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return 'Bearer ' + access_token
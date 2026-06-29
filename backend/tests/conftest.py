import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User

# SQLite test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_taskflow.db"

# Create testing engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    # Seed default test users
    admin = User(
        name="Test Admin",
        email="testadmin@example.com",
        password_hash=get_password_hash("AdminPass123!"),
        role="admin"
    )
    developer = User(
        name="Test Developer",
        email="testdev@example.com",
        password_hash=get_password_hash("DevPass123!"),
        role="developer"
    )
    db.add(admin)
    db.add(developer)
    db.commit()
    db.close()
    
    yield
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    # Remove sqlite file
    if os.path.exists("./test_taskflow.db"):
        os.remove("./test_taskflow.db")

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def admin_headers(db):
    user = db.query(User).filter(User.email == "testadmin@example.com").first()
    token = create_access_token(subject=user.id)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def dev_headers(db):
    user = db.query(User).filter(User.email == "testdev@example.com").first()
    token = create_access_token(subject=user.id)
    return {"Authorization": f"Bearer {token}"}

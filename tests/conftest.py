from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.base import Base
from api.main import app
from api.db.database_config import get_db
from api.models.role_model import Role

SQLALCHEMY_DB_URL = "sqlite:///tests/test.db"
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_roles(client, session):
    role_user = {"name": "USER"}
    role_admin = {"name": "ADMIN"}
    session.add_all([Role(**role_user), Role(**role_admin)])
    session.commit()
    return session.query(Role).all()
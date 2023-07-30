from typing import List, Type
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from api.db.base import Base
from api.main import app
from api.db.database_config import get_db
from api.models.role_model import Role
from api.models.user_model import User
from api.models.workspace_model import Workspace
from api.security.token_schemas import Token
from api.security.oauth2 import create_access_token
from api.security.password import HashPassword

SQLALCHEMY_DB_URL = "sqlite:///tests/test.db"
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> TestSessionLocal:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session: TestClient) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_roles(client: TestClient, session: Session) -> List[Type[Role]]:
    role_user = {"name": "USER"}
    role_admin = {"name": "ADMIN"}
    role_moderator = {"name": "MODERATOR"}
    session.add_all(
        [
            Role(**role_user),
            Role(**role_admin),
            Role(**role_moderator)
        ])
    session.commit()
    return session.query(Role).all()


@pytest.fixture(scope="session")
def test_password():
    return "password1A#"


@pytest.fixture(scope="session")
def hashed_password(test_password):
    hash_password = HashPassword()
    return hash_password.get_hashed_password(test_password)


@pytest.fixture
def test_users(client: TestClient, session: Session, test_roles: List[Role], hashed_password: str) -> List[Type[User]]:
    user_user = {"email": "user@email.com",
                 "password": hashed_password,
                 "first_name": "user_first",
                 "last_name": "user_last"}

    user_admin = {"email": "admin@email.com",
                  "password": hashed_password,
                  "first_name": "admin_first",
                  "last_name": "admin_last"}

    session.add_all([User(**user_user), User(**user_admin)])
    session.commit()

    user = session.query(User).filter_by(id=1).first()
    user.roles.append(session.query(Role).filter_by(name=test_roles[0].name).first())
    session.commit()

    admin = session.query(User).filter_by(id=2).first()
    admin.roles.append(session.query(Role).filter_by(name=test_roles[0].name).first())
    admin.roles.append(session.query(Role).filter_by(name=test_roles[1].name).first())
    admin.roles.append(session.query(Role).filter_by(name=test_roles[2].name).first())
    session.commit()

    return session.query(User).all()


@pytest.fixture
def authorized_admin_client(client: TestClient, test_users: List[User]) -> TestClient:
    token: Token = create_access_token(data={"email": test_users[1].email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.access_token}"
    }
    return client


@pytest.fixture
def authorized_user_client(client: TestClient, test_users: List[User]) -> TestClient:
    token: Token = create_access_token(data={"email": test_users[0].email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.access_token}"
    }
    return client


@pytest.fixture
def test_admin_workspaces(session, test_users):
    admin_workspaces = [
        Workspace(title="First Admin workspace", owner_id=test_users[1].id, members=test_users),
        Workspace(title="Second Admin workspace", owner_id=test_users[1].id, members=test_users)
    ]

    session.add_all(admin_workspaces)
    session.commit()
    return session.query(Workspace).filter_by(owner_id=test_users[1].id)

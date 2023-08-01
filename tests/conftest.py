from typing import List, Type
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
def client(session: TestSessionLocal) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_roles(client: TestClient, session: TestSessionLocal) -> List[Type[Role]]:
    roles = [
        Role(name="USER"),
        Role(name="ADMIN"),
        Role(name="MODERATOR"),
    ]
    session.add_all(roles)
    session.commit()
    return session.query(Role).all()


@pytest.fixture(scope="session")
def test_password():
    return "password1A#"


@pytest.fixture(scope="session")
def hashed_password(test_password) -> str:
    hash_password = HashPassword()
    return hash_password.get_hashed_password(test_password)


@pytest.fixture
def test_users(client: TestClient,
               session: TestSessionLocal,
               test_roles: List[Role],
               hashed_password: str) -> List[Type[User]]:

    user: User = User(email="user@email.com",
                      password=hashed_password,
                      first_name="user_first",
                      last_name="user_last",
                      roles=[test_roles[0]])

    admin: User = User(email="admin@email.com",
                       password=hashed_password,
                       first_name="admin_first",
                       last_name="admin_last",
                       roles=test_roles)

    session.add_all([user, admin])
    session.commit()
    return session.query(User).all()


@pytest.fixture
def test_admin_user(test_users) -> Type[User]:
    return test_users[1]


@pytest.fixture
def test_simple_user(test_users) -> Type[User]:
    return test_users[0]


@pytest.fixture
def authorized_admin_client(client: TestClient, test_admin_user: User) -> TestClient:
    token: Token = create_access_token(data={"email": test_admin_user.email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.access_token}"
    }
    return client


@pytest.fixture
def authorized_user_client(client: TestClient, test_simple_user: User) -> TestClient:
    token: Token = create_access_token(data={"email": test_simple_user.email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.access_token}"
    }
    return client


@pytest.fixture
def test_workspaces(session: TestSessionLocal, test_admin_user: User, test_simple_user: User) -> List[Type[Workspace]]:
    workspaces: List[Workspace] = [
        Workspace(title="C++ Workspace", owner_id=test_admin_user.id, members=[test_admin_user, test_simple_user]),
        Workspace(title="Python Project Workspace", owner_id=test_admin_user.id, members=[test_admin_user]),
        Workspace(title="Ruby Project Workspace", owner_id=test_simple_user.id, members=[test_simple_user]),
    ]

    session.add_all(workspaces)
    session.commit()
    return session.query(Workspace).all()


@pytest.fixture
def test_admin_workspaces(test_workspaces: List[Type[Workspace]]) -> List[Type[Workspace]]:
    admin_workspaces: List[Type[Workspace]] = [workspace for workspace in test_workspaces if workspace.owner_id == 2]
    return admin_workspaces


@pytest.fixture
def test_user_workspaces(test_workspaces: List[Type[Workspace]]) -> List[Type[Workspace]]:
    user_workspaces: List[Type[Workspace]] = [workspace for workspace in test_workspaces if workspace.owner_id == 1]
    return user_workspaces

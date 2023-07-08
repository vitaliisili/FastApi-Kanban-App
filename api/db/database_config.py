from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config.env_config import settings as cfg
from api.db.base import Base

SQLALCHEMY_DB_URL = f'postgresql://{cfg.db_username}:{cfg.db_password}@{cfg.db_hostname}:{cfg.db_port}/{cfg.db_name}'
engine = create_engine(SQLALCHEMY_DB_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()




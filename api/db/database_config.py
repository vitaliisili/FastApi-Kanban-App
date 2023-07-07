from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config.env_config import settings as cfg
from api.models import user_model, role_model

SQLALCHEMY_DB_URL = f'postgresql://{cfg.db_username}:{cfg.db_password}@{cfg.db_hostname}:{cfg.db_port}/{cfg.db_name}'
engine = create_engine(SQLALCHEMY_DB_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

user_model.Base.metadata.create_all(bind=engine)
role_model.Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()




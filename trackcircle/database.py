from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import trackcircle.config

engine = create_engine(trackcircle.config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
            autoflush=False, bind=engine))
            
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import trackcircle.models
    Base.metadata.create_all(bind=engine)
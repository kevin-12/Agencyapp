from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import postgresql

#create path for database
dbstring="DATABASE_URL"
engine = create_engine(dbstring)

db_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
#initialize database
def init_db(): 

    import app.model
    Base.metadata.create_all(bind=engine)

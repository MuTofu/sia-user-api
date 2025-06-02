
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL_DB = 'mysql+pymysql://cahya:admin@host.docker.internal:3306/User'

URL_DB = 'mysql+pymysql://cahya:admin@127.0.0.1:3307/User'



engine = create_engine(URL_DB)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
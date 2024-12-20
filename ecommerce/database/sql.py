from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

"""
Postgres
"""

URI = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"

"""
SQLITE
"""

engine = create_engine(
    URI,  
    pool_size=5,          
    max_overflow=10,      
    pool_timeout=30,      
    pool_recycle=1800     
)


Base = declarative_base()
Session = sessionmaker(bind=engine)

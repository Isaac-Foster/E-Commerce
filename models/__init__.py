from fastapi import FastAPI
from sqlalchemy import text

from database.sql import engine, Base, Session
from models import admin, user


def init_post(): 
    print("criando tables")
    Base.metadata.create_all(engine)
    with Session() as session:
        session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        session.commit()


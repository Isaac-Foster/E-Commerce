from fastapi import FastAPI
from sqlalchemy import text

from ecommerce.database.sql import Base, Session, engine
from ecommerce.models import admin, products, user


def init_post():
    Base.metadata.create_all(engine)

    with Session() as session:
        session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        session.commit()


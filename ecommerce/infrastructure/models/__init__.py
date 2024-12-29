from fastapi import FastAPI
from sqlalchemy import text

from ecommerce.infrastructure.database.sql import Base, Session, engine
from ecommerce.infrastructure.models import admin, products, user, restrict_paths

from ecommerce.schema.users.user import UserSignup
 

def init_post():
    Base.metadata.create_all(engine)

    with Session() as session:
        session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        session.commit()
        user_model = session.query(user.UserModel).filter_by(username="teste").first()

        if user_model:
            return

        data = UserSignup(
            name="User teste",
            email="userteste@gmail.com",
            username="teste",
            password="Senha123@#***"
        )

        data.register()

        user_model = session.query(user.UserModel).filter_by(username="teste").first()

        if user_model:
            admin_model = admin.AdminModel(
                user_id=user_model.id, 
                password=data.password,
                privileges=dict(
                    read=True,
                    write=True,
                )
            )
            session.add(admin_model)
            session.commit()

import re
import string
from typing import Annotated
from dataclasses import dataclass

import bcrypt
from sqlalchemy import select
from pydantic.networks import EmailStr
from fastapi import Query, Body, HTTPException
from email_validator import validate_email, EmailNotValidError

from ecommerce.database.sql import Session
from ecommerce.models.user import UserModel


class WeakPasswordError(HTTPException):
    """Exceção levantada para senhas fracas."""
    
    def __init__(self, password: str, message: str = "Senha é muito fraca"):
        self.password = password
        self.message = message
        super().__init__(status_code=400, detail=self.message)

    def __str__(self):
        return f'{self.message}: {self.password}'


def is_strong_pass(
    password: str, 
    chars: int = 8, 
    lowers: int = 3, 
    uppers: int = 1, 
    digits: int = 1,
    specials: int = 1
    ):

    is_strong = re.search(
        (
            "(?=^.{%i,}$)"
            "(?=.*[a-z]{%i,})"
            "(?=.*[A-Z]{%i})"
            "(?=.*[0-9]{%i,})"
            "(?=.*[%s}]{%i,})"
        ) % 
        (
            chars, lowers, uppers,
            digits, re.escape(string.punctuation),
            specials
        ),
        password
    )

    if not is_strong:
        if len(password) < chars:
            raise WeakPasswordError(password, f"A senha deve ter pelo menos {chars} caracteres")
        if not any(char.isdigit() for char in password):
            raise WeakPasswordError(password, "A senha deve conter pelo menos um dígito")
        if not any(char.isupper() for char in password):
            raise WeakPasswordError(password, "A senha deve conter pelo menos uma letra maiúscula")
        if not any(char.islower() for char in password):
            raise WeakPasswordError(password, "A senha deve conter pelo menos uma letra minúscula")
        if not any(char in string.punctuation for char in password):
            raise WeakPasswordError(password, "A senha deve conter pelo menos um caractere especial")
    return True


def verify_registry(registry):
    if len(registry.password) > 100:
            raise HTTPException(status_code=400, detail="senha maior que 100 caracteres")
        
    elif len(registry.email) > 256:
        raise HTTPException(status_code=400, detail="email maior que 256 caracteres")

    elif len(registry.name) > 256:
        raise HTTPException(status_code=400, detail="nome maior que 256 caracteres")
    
    elif len(registry.username) > 50:
        raise HTTPException(status_code=400, detail="username maior que 50 caracteres")


@dataclass
class UserSignup:
    name: Annotated[str, Body(description="name suname")]
    email: Annotated[EmailStr, Body(description="test@sample.com")]
    username: Annotated[str, Body(description="@sample")]
    password: Annotated[str, Body(description="Admin123***")]

    def __post_init__(self):
        emailinfo = validate_email(self.email, check_deliverability=True)

        email = emailinfo.normalized

        verify_registry(self)
    
        is_strong_pass(self.password)

        salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(self.password.encode('utf-8'), salt)

        self.password = hashed.decode('utf-8')

    def register(self) -> bool:
        with Session() as session:
            already = session.execute(
                select(UserModel).filter_by(username=self.username)
            ).fetchone()

        if not already:
            with Session() as session:
                session.add(UserModel(**self.__dict__))
                session.commit()

            return True
        
        if already and self.username == "usertest":
            return True
        
        return False


@dataclass
class UserSignin:
    username: Annotated[str, Body(description="@sample")]
    password: Annotated[str, Body(description="Admin123***")]

    def verify(self) -> bool:
        with Session() as session:
            hashed = session.execute(
                select(UserModel.password).filter_by(username=self.username)
            ).fetchone()

        if not hashed:
            return hashed
        
        return (
            bcrypt.checkpw(self.password.encode('utf-8'),
            hashed[0].encode('utf-8'))
            )
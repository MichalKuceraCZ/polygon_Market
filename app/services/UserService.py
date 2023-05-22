from datetime import datetime

import asyncpg
from sqlmodel import Session, select
from sqlalchemy import exc

from app.auth.password import verify_password, get_password_hash
from app.exceptions.EmailDuplicationException import EmailDuplicationException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.models.User import User
from app.models.UserPassword import UserPassword
from app.requests.LoginRequest import LoginRequest
from app.requests.UserCreateRequest import UserCreateRequest
from app.responses.GetByUsernameResponse import GetByUsernameResponse


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: UserCreateRequest):
        try:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                birthdate=datetime.strptime(data.birthdate, "%Y-%m-%d").date(),
                username=data.username,
                passwords=[UserPassword(value=get_password_hash(data.password))],
            )

            self.session.add(new_user)
            await self.session.commit()

            return new_user
        except (exc.IntegrityError, asyncpg.exceptions.UniqueViolationError):
            raise EmailDuplicationException(f"Email [{data.email}] already exists")
        except Exception as e:
            raise Exception(e)

    async def get_by_username(self, username: str) -> GetByUsernameResponse:
        query = (
            select(User.user_id, User.username, User.email, UserPassword.value.label("password"))
            .join(UserPassword)
            .where(User.username == username)
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.first()

    async def login(self, data: LoginRequest):
        user = await self.get_by_username(data.username)

        if not user:
            raise UserNotFoundException("Username or password is invalid")

        if not verify_password(data.password, user.password):
            raise UserNotFoundException("Username or password is invalid")

        return user

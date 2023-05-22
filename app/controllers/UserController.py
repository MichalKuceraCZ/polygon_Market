from fastapi import Depends, Response, status, Body, APIRouter, HTTPException
import json
from sqlalchemy.orm.exc import NoResultFound

from app.auth.token import create_access_token
from app.deps import get_user_service
from app.exceptions.EmailDuplicationException import EmailDuplicationException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.requests.LoginRequest import LoginRequest
from app.requests.UserCreateRequest import UserCreateRequest
from app.services.UserService import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/", response_class=Response, status_code=status.HTTP_201_CREATED)
async def create_user(*, user_service: UserService = Depends(get_user_service),
                      request: UserCreateRequest = Body()):
    try:
        await user_service.create_user(request)
        return Response(status_code=status.HTTP_201_CREATED)
    except EmailDuplicationException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": str(e),
            "code": "EMAIL_DUPLICATION",
            "status_code": status.HTTP_409_CONFLICT,
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        })


@user_router.post("/login")
async def login(*, user_service: UserService = Depends(get_user_service),
                request: LoginRequest = Body()):
    try:
        user = await user_service.login(request)

        access_token = create_access_token(
            data={"sub": user.username}
        )

        return Response(status_code=status.HTTP_200_OK,
                        content=json.dumps({"access_token": access_token, "token_type": "bearer"}))
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        })

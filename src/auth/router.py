from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from database import AsyncSessionLocal
from .models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from config import SECRET, ALGORITHM

# python-jose[cryptography]
# passlib[bcrypt]
# python-multipart

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

templates = Jinja2Templates(directory='templates')

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2AuthorizationCodeBearer(authorizationUrl='/auth/login', tokenUrl='/auth/token')


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    tiken_type: str


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/login')
async def get_login_page(request:Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request:CreateUserRequest):
    create_user_model = User(
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    await db.commit()


@router.post('/token')
async def login_for_access_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Could not validate user...')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}


async def authenticate_user(username: str, password: str, db: db_dependency):
    # user = db.query(User).filter(User.username == username).first()
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)
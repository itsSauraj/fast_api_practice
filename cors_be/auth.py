from datetime import datetime, timedelta, timezone
from typing import Annotated
import uuid

import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import UUID4

from passlib.context import CryptContext

from cors_be.models import Token, TokenData, User, UserInDB, UserUpdate

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from cors_be.database import get_user_by_email, create_user, get_user_by_id, update_user, prune_user_data


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Auth:

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(password):
        return pwd_context.hash(password)
    
    def get_user(db, username):
        for user in db:
            if user["email"] == username:
                return user
        return None
    
    def get_usr_by_id(user_id: UUID4):
        user = get_user_by_id(user_id)
        return user
    
    def register_user(user: User):
        user = UserInDB(**user.dict())
        user.id = str(uuid.uuid4())
        user.created_at = datetime.now(timezone.utc)
        user.password = Auth.hash_password(user.password)
        created_user = create_user(user)
        return created_user
    
    def update_user(user_id: UUID4, updated_data: UserUpdate):
        updated_data.password = Auth.hash_password(updated_data.password)
        update = update_user(user_id, updated_data)
        return update
    
    
    def delete_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        
        deleted_user = prune_user_data(email=token_data.username)
        return deleted_user

        

    def authenticate_user(username: str, password: str):
        user = get_user_by_email(email=username)
        
        if not user:
            return False
        if not Auth.verify_password(password, user.password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        
        user = get_user_by_email(email=token_data.username)
        
        if user is None:
            raise credentials_exception
        return user

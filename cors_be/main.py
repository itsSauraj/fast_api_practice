import time, uuid
from datetime import datetime, timedelta, timezone

from typing import Annotated

from pydantic import UUID4

from cors_be.auth import Auth as auth, ACCESS_TOKEN_EXPIRE_MINUTES
from cors_be.post import Post as postCRUD

from cors_be.models import Token, UserInDB, Post, UserUpdate

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware


description = "FASTAPI WITH CORS, SQLITE, OAUTH2, JWT and SQLALCHEMY"

app = FastAPI(
    title="FastAPI Tutorial",
    description=description,
    version="1.0.0",    
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "itsSauraj",
        "url": "https://example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "Apache-2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


items = {"message": "This is a test message. For cros CORS."}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Process-Name"] = "Middleware"
    response.headers["X-Process-Created-From"] = "FastAPI-Tutorial"
    return response
    

origins = [
  "http://localhost:8000",
  "http://localhost:5173",
]    

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}
  
@app.get("/username")
async def read_username(token: Annotated[str, Depends(oauth2_schema)]):
    user = await auth.get_current_user(token)
    return {"username": user.name}
  
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/register")
async def register_user(user: UserInDB):
    register = auth.register_user(user)
    auth_user = auth.authenticate_user(user.email, user.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.patch("/user/{user_id}")
def update_user(user_id: UUID4, updated_data: UserUpdate, token: Annotated[str, Depends(oauth2_schema)]):
    user = auth.update_user(user_id, updated_data)
    return {"user_email": user}


@app.delete("/user")
async def delete_user(token: Annotated[str, Depends(oauth2_schema)]):
    deleted_user = auth.delete_user(token)
    return deleted_user


@app.get("/posts")
async def read_posts(page: int = 1, limit: int = 10):
    posts = postCRUD.get_posts(page, limit)
    return posts

@app.get("/posts/u/{user_id}")
async def read_posts(user_id: str, page: int = 1, limit: int = 10):
    '''
    Example of geting posts of a user using user_id and filters
    '''
    posts = await postCRUD.get_users_post(page=page, limit=limit, user_id=user_id)
    return posts

@app.get("/posts/u2/{user_id}")
async def read_posts_2(user_id: str, page: int = 1, limit: int = 10):
    '''
    Example of geting posts of a user using Correlations and using SQLAlchemy Session
    '''
    posts = await postCRUD.get_users_post_(page=page, limit=limit, user_id=user_id)
    return posts

@app.get("/my_posts")
async def my_posts(token: Annotated[str, Depends(oauth2_schema)], page: int = 1, limit: int = 10):
    ''' 
    Example of geting posts of a user using after they have logged in using Correlations and using SQLAlchemy Session 
    '''
    user = await auth.get_current_user(token)
    posts = await postCRUD.get_users_post_(page=page, limit=limit, user_id=user.id)
    return posts

@app.post("/post/create")
async def create_post(token: Annotated[str, Depends(oauth2_schema)], post: Post):
    user = await auth.get_current_user(token)
    
    post.id = str(uuid.uuid4())
    post.author_id = user.id
    post.created_at = datetime.now(timezone.utc)
    
    created_post = postCRUD.create(post=post)
    return created_post

@app.get("/post/{post_id}")
async def read_post(post_id: str):   
    post = await postCRUD.get_post(post_id)
    
    context = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
    }
    
    return context

@app.delete("/post/{post_id}")
async def delete_post(post_id: str, token: Annotated[str, Depends(oauth2_schema)]):
    user = await auth.get_current_user(token)    
    deleted_post = await postCRUD.delete_post(post_id, user.id)
    return deleted_post
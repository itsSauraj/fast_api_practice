from pydantic import BaseModel
from typing import List
from datetime import datetime

from pydantic import UUID4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
import uuid

class DBBaseModel(DeclarativeBase):
    created_at: Mapped[str] = mapped_column(default=datetime.now)

class ModifiedBaseModel(BaseModel):
    created_at: datetime | None = None

class User(ModifiedBaseModel):
    id: UUID4 | None = None
    name: str
    email: str

class UserInDB(User):
    password: str
    
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

    
class Post(ModifiedBaseModel):
    id: str | None = None
    title: str
    content: str
    author_id: int | None = None
    

# class DBUserModal(DBBaseModel):
#     __tablename__ = "user_account"

#     created_at: Mapped[str] = mapped_column(default=datetime.now)
#     id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
#     name: Mapped[str] = mapped_column()
#     email: Mapped[str] = mapped_column(unique=True)
#     password: Mapped[str] = mapped_column()

#     posts: Mapped[List["DBPostModal"]] = relationship("DBPostModal", back_populates="author")

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r})"


# class DBPostModal(DBBaseModel):
#     __tablename__ = "posts"

#     id: Mapped[str] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column()
#     content: Mapped[str] = mapped_column()
#     author_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), default=None, nullable=False) 

#     author: Mapped["DBUserModal"] = relationship("DBUserModal", back_populates="posts")

#     def __repr__(self) -> str:
#         return f"Post(id={self.id!r}, title={self.title!r})"

class DBUserModal(DBBaseModel):
    __tablename__ = "user_account"

    created_at: Mapped[str] = mapped_column(default=datetime.now)
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    posts: Mapped[List["DBPostModal"]] = relationship("DBPostModal", back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class DBPostModal(DBBaseModel):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    author_id: Mapped[str] = mapped_column(ForeignKey("user_account.id"), nullable=False)  # Ensure the type matches

    author: Mapped["DBUserModal"] = relationship("DBUserModal", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"
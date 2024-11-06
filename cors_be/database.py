from sqlalchemy import create_engine, text, insert, select, update, delete, func
from sqlalchemy.orm import Session, selectinload

from pydantic import UUID4

from cors_be.models import DBBaseModel, DBUserModal, DBPostModal

engine = create_engine("sqlite+pysqlite:///cors.db", echo=True)
DBBaseModel.metadata.create_all(engine)


def get_user_by_email(email: str):
    with engine.connect() as conn:
        query = select(DBUserModal).where(DBUserModal.email == email)
        result = conn.execute(query, {"email": email})
    return result.first()

def get_user_by_id(user_id: UUID4):
    with engine.connect() as conn:
        query = select(DBUserModal).where(DBUserModal.id == str(user_id))       
        result = conn.execute(query, {"id": user_id})
    return result.first()
  
def create_user(user: DBUserModal):
    with Session(engine) as session:
        query = insert(DBUserModal).values(**user.dict())
        result = session.execute(query)
        session.commit()
    return result

def update_user(user_id: UUID4, updated_data: DBUserModal):
    with Session(engine) as session:
        query = update(DBUserModal).where(DBUserModal.id == str(user_id)).values(**updated_data.dict())
        result = session.execute(query)
        session.commit()
    return result

def prune_user_data(email : str):
    with Session(engine) as session:
        
        user = get_user_by_email(email)
        
        delete_user_post_query = delete(DBPostModal).where(DBPostModal.author_id == user.id)
        post_result = session.execute(delete_user_post_query)
                
        query = delete(DBUserModal).where(DBUserModal.email == email)
        user_result = session.execute(query)
        session.commit()
        
        response = {
            "user_deleted": user_result.rowcount,
            "posts_deleted":  post_result.rowcount
        }
        
    return response

def get_user_count():
    with engine.connect() as conn:
        query = select(func.count(DBUserModal.id))
        result = conn.execute(query)
    return result.fetchone()[0]


def create_post(post: DBPostModal):
    with Session(engine) as session:
        query = insert(DBPostModal).values(**post.dict())
        result = session.execute(query)
        session.commit()
    return result

def get_posts(page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    with engine.connect() as conn:
        query = select(DBPostModal).offset(offset).limit(limit)
        result = conn.execute(query)
        posts = post_json(result.all())
    return posts

def get_post(post_id: UUID4):
    with engine.begin() as conn:
        query = select(DBPostModal).where(DBPostModal.id == post_id)
        result = conn.execute(query, {"id": post_id})
    return result.first()

def delete_post(post_id: UUID4, user_id: UUID4):
    
    with Session(engine) as session:
        
        post = get_post(post_id)
        if post.author_id != user_id:
            return "You are not authorized to delete this post"
        
        query = delete(DBPostModal).where(DBPostModal.id == str(post_id))
        result = session.execute(query)
        session.commit()
    return result

def get_users_post(user_id: str, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    with engine.connect() as conn:
        # query = select(DBPostModal).where(DBPostModal.author_id == user_id).offset(offset).limit(limit)
        query = select(DBPostModal).offset(offset).limit(limit).filter(DBPostModal.author_id == user_id)
        result = conn.execute(query)
        posts = post_json(result.all())
    return posts

def get_users_post_(user_id: str, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    with Session(engine) as session:
        query = session.query(DBUserModal).filter(DBUserModal.id == user_id)
        result = query.first()
        if result and result.posts:
            paginated_posts = result.posts[offset:offset + limit]
            posts = post_json(paginated_posts)
    return posts

def post_json(posts):
    return [{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
    } for post in posts]
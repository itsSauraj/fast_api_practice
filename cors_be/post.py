from cors_be.auth import Auth as auth
from cors_be.database import create_post, get_posts, get_users_post, get_post, get_users_post_, delete_post

from cors_be.models import Post

class Post:
  
  def create(post: Post):
    fetched_post = create_post(post)
    print(fetched_post)
    return fetched_post
  
  
  def get_posts(page: int = 1, limit: int = 10):
    posts = get_posts(page, limit)
    return posts
  
  async def get_post(post_id: str):
    post = get_post(post_id=post_id)
    return post
  
  async def get_users_post(user_id: str, page: int = 1, limit: int = 10):
    posts = get_users_post(page=page, limit=limit, user_id=user_id)
    return posts
  
  async def get_users_post_(user_id: str, page: int = 1, limit: int = 10):
    post = get_users_post_(page=page, limit=limit, user_id=user_id)
    return post
  
  async def delete_post(post_id: str, user_id: str):
    post = delete_post(post_id, user_id)
    return post
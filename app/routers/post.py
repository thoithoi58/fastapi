from fastapi import Response , HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List
from ..schema import Post, PostRespone

router = APIRouter()


@router.get("/posts", response_model=List[PostRespone])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostRespone)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()    
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/posts/{id}", response_model=PostRespone)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    
    return post

@router.delete("/posts/{id}")
def delete_post(id: int, status_code = status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=PostRespone)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts 
    # SET title = %s, content = %s, published=%s
    # WHERE id = %s
    # RETURNING *""", (post.title, post.content, post.published, id))
    # post_ = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_ = post_query.first()

    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    post_query.update(post.dict())
    db.commit()

    return post_query.first()
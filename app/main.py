from typing import Optional, List
from fastapi import FastAPI, Response, HTTPException, status, Depends 
from fastapi.params import Body

from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .schema import Post, PostRespone
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schema import Post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
                                user = 'postgres', password = '123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        time.sleep(2)
        print("Connection fail with error:", error)


@app.get("/")
async def root():
    return {"message": "Helaaalo World"}

@app.get("/posts", response_model=List[PostRespone])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostRespone)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()    
    # conn.commit()
    print(post)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/{id}", response_model=PostRespone)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    
    return post

@app.delete("/posts/{id}")
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

@app.put("/posts/{id}", response_model=PostRespone)
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
from typing import Optional, List
from fastapi import FastAPI, Response, HTTPException, status, Depends 
from fastapi.params import Body

from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app import utils
from . import models

from .database import engine, get_db
from .schema import Post

from .routers import post, user

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

app.include_router(post.router)
app.include_router(user.router)



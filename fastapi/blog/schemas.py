from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True

## for response model which is totally new :
class ShowBlog(BaseModel):
    # DM is only title
    title: str
    class Config():
        orm_mode = True

'''

## for response model which inherits DM 
class ShowBlog(Blog):
    # DM are :
    # title and body
    class Config():
        orm_mode = True
        
'''

## for user creation :

class User(BaseModel):
    name: str
    email: str
    password: str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

## extended class to get creator of blogs
class BlogUser(ShowBlog):
    creator: ShowUser

## extended class to get all blogs of created
class BlogsByUser(ShowUser):
    blogs : List

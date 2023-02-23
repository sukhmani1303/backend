from fastapi import APIRouter, Depends,status
from main import database,schemas
from typing import List
from sqlalchemy.orm import Session
from repository import blog
from main import oauth2

get_db = database.get_db

router = APIRouter(
    prefix = '/blog',
    tags = ['blogs']
)

@router.get('/')
def all(db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED) 
def create(request: schemas.Blog, db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)): 
    return blog.create_new(db, request)

@router.get('/{id}',status_code=200, response_model=List[schemas.ShowBlog])
def show(id,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return blog.view(db, id)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_blog(id,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(db, id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request: schemas.Blog,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(db,id,request)


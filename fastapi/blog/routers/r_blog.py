from fastapi import APIRouter, Depends,status,HTTPException
from main import database, models,schemas
from typing import List
from sqlalchemy.orm import Session

get_db = database.get_db

router = APIRouter()

@router.post('/blog', status_code = status.HTTP_201_CREATED ,tags = ['blog']) 
def create(request: schemas.Blog, db : Session = Depends(get_db)): 
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog' ,tags = ['blog'])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/blog/{id}',status_code=200, response_model=List[schemas.ShowBlog] ,tags = ['blog'])
def show(id,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).all()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"blog with id = {id} not found !")
    return blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT ,tags = ['blog'])
def del_blog(id,db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED ,tags = ['blog'])
def update_blog(id,request: schemas.Blog,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"blog with id {id} not found !")
    blog.update({'title' : request.title, 'body' : request.body})
    db.commit()
    return 'updated !'


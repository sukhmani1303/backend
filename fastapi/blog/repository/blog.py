from sqlalchemy.orm import Session
from main import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create_new(db:Session, request:schemas.Blog):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(db:Session, id:int):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = f"The Blog with id {id} not found")
    blogs.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

def view(db: Session, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).all()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"blog with id = {id} not found !")
    return blog

def update(db:Session, id:int, request: schemas.Blog):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"blog with id {id} not found !")
    blog.update({'title' : request.title, 'body' : request.body})
    db.commit()
    return 'updated !'
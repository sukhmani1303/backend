from fastapi import FastAPI, Depends, status, Response, HTTPException
import uvicorn
from database import engine, SessionLocal

# professionally we create a new python file to store all BaseModel Classes
import schemas, models # here, schemas is the py file

app = FastAPI()

### creating Tables ###

models.Base.metadata.create_all(engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Create Operation ###

from sqlalchemy.orm import Session

@app.post('/blog', status_code = status.HTTP_201_CREATED) # here, we can set status codes using 'status'
def create(request: schemas.Blog, db : Session = Depends(get_db)): # we use "file_name.class" to fetch class data
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    # for returning the row :
    db.refresh(new_blog)
    return new_blog


### read data from DataBase ###

@app.get('/blog1') # simple get all
def all(db : Session = Depends(get_db)):
    
    # we can fetch all records using .all() function from Blog table in models
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog2/{id}') # get with conditions
def show(id, response : Response,db : Session = Depends(get_db)):
    
    # we can fetch all records using .all() function from Blog table in models
    blog = db.query(models.Blog).filter(models.Blog.id == id).all()
    # we can use .first() to fetch the first occurance only or .all() for all

    # we can add condition to check response errors
    if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'detail' : f"blog with id = {id} not found !"}

        # we can aslo use HTTPException of FastAPI for ease:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"blog with id = {id} not found !")

    return blog


### Delete Operation ###

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_blog(id,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'


### Update Operation ###

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request: schemas.Blog,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"blog with id {id} not found !")
    
    # both the below methods work for updation using request body

    blog.update({'title' : request.title, 'body' : request.body})
    # blog.update(request.dict())


    db.commit()
    return 'updated !'


### Other MySQL Function ###
# https://docs.sqlalchemy.org/en/14/core/sqlelement.html

# Examples :
'''
limit function :

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
    
##############################
    
groupby function and count function :

from sqlalchemy import func
def get_items(db: Session, skip: int = 0, limit: int = 100):
    db.query(models.Item.column, func.count(models.Item.column)).group_by(models.Item.column).all()

##############################
    
first function :

user = db.query(User).first()

##############################

orderby function :

from sqlalchemy import desc
stmt = select(users_table).order_by(desc(users_table.c.name))

'''

### Response Models ###

# it basically dictates the format of response
# we have to create a class in schemas and use it as
# response_model to get response as its data members only
# For Eg: it class has 2 Data-Members (title and body) then
# the response even if it contains title, body and id will
# only return title and body

# if we deal with DB, we need to add :
# class Config():
#    orm_mode = True
# inside the class in schemas

# in the following example we are requesting a response involving DB
# in the format of ShowBlog as we created ShowBlog class in schemas

# We must use the following and declare the model as List
from typing import List

# Declare the request model in path :
@app.get('/blog22/{id}',status_code=200, response_model=List[schemas.ShowBlog])
def show(id, response : Response,db : Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).all()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"blog with id = {id} not found !")

    return blog

# Now we can simply make changes in the data-members of response model class and modify the response format


### CREATE USER ###

@app.post('/user')
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    new_usr = models.User(name = request.name, password = request.password, email = request.email)
    db.add(new_usr)
    db.commit()
    # for returning the row :
    db.refresh(new_usr)
    return new_usr

## Hashing the Password ##

# FastAPI asks us to use passlib for hashing
# for encryption, it has several steps :

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user_safe')
def create_user(request: schemas.User, db : Session = Depends(get_db)):

    # we create the encrypted pass by passing original password in the function of pwd_content obj
    hashed_pass = pwd_context.hash(request.password)

    new_usr = models.User(name = request.name, password = hashed_pass, email = request.email)

# ## We genrally create hasing.py file which contains all classes for cryption/encryption etc

#     from hashing import Hash

#     new_usr = models.User(name = request.name, password = Hash.bcrypt(request.password), email = request.email) 


    db.add(new_usr)
    db.commit()
    # for returning the row :
    db.refresh(new_usr)
    return new_usr



if __name__ == '__main__':
    uvicorn.run(app, host = "127.0.0.1", port = 8050)
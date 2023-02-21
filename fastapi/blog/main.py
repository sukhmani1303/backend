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


if __name__ == '__main__':
    uvicorn.run(app, host = "127.0.0.1", port = 8050)
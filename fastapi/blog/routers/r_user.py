from fastapi import APIRouter, Depends, HTTPException, status
from main import database, models, schemas
from typing import List
from sqlalchemy.orm import Session
from main.hashing import Hash

get_db = database.get_db

router = APIRouter()

@router.get('/user/{id}', response_model=List[schemas.ShowUser] ,tags = ['user'])
def usr_details(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not found !")
    return user

@router.post('/user' ,tags = ['user'])
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    new_usr = models.User(name = request.name, password = Hash.bcrypt(request.password), email = request.email)
    db.add(new_usr)
    db.commit()
    # for returning the row :
    db.refresh(new_usr)
    return new_usr

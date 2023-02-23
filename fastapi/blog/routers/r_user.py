from fastapi import APIRouter, Depends
from main import database,schemas
from typing import List
from sqlalchemy.orm import Session
from repository import user
from main import oauth2

get_db = database.get_db

router = APIRouter(
    prefix = '/user',
    tags = ['users']
)

@router.get('/{id}', response_model=List[schemas.ShowUser] )
def usr_details(id:int, db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return user.view(db, id)

@router.post('/')
def create_user(request: schemas.User, db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return user.create(db, request)

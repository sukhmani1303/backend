from fastapi import APIRouter, Depends
from main import database, models
from typing import List
from sqlalchemy.orm import Session


router = APIRouter()

@router.get('/blog1')
def all(db : Session = Depends(database.get_db)):
    
    # we can fetch all records using .all() function from Blog table in models
    blogs = db.query(models.Blog).all()
    return blogs
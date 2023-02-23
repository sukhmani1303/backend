from fastapi import APIRouter, Depends, HTTPException, status
from main import database,schemas,models
from sqlalchemy.orm import Session
from main.hashing import Hash

router = APIRouter(
    tags = ['authentication']
)

get_db = database.get_db

@router.post('/login')
def login(request: schemas.login, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "You are not registered !")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    
    return user
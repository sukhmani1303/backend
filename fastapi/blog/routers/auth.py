from fastapi import APIRouter, Depends, HTTPException, status
from main import database,schemas,models
from sqlalchemy.orm import Session
from main.hashing import Hash
from main import tokenlib
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ['authentication']
)

get_db = database.get_db

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "You are not registered !")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokenlib.create_access_token(
        data={"sub": user.email}
        # , expires_delta=token.access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}